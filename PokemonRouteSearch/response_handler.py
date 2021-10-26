from sys import exit
from textwrap import dedent
from PokeAPI_wrapper.api_wrapper import *


class ResponseHandler:
    def __init__(self):
        self.input_prompt = ''
        self.response = ''
        self.valid_responses = []
        self.valid_search = False
        self.help_text = ''
        self.context = ''

    def get_response(self):
        """User input prompt based on input_prompt attr and responds to help. lower() to sanitize input.
        Empty string has to be checked or else API will return 200 and break the logic.
        """

        self.response = input(f'{self.input_prompt}').lower()

        if self.response == 'help':
            print(dedent(self.help_text))
            self.get_response()
        elif self.response == '':
            print('Please enter a response.')
            self.get_response()
        elif self.response == 'quit':
            exit()
        else:
            return

    def validate_response(self):
        """Checks if user input is in valid_responses attr and informs user of valid options if not."""

        if self.response in self.valid_responses:
            self.valid_search = True
            return
        else:
            print("Please input a valid response. Valid responses are: ",
                  f"{', '.join(item for item in self.valid_responses)} \n")
            self.get_response()
        return

    def handle_response(self):
        raise Exception('ResponseHandler.handle_response() should be overwritten in subclasses but was instead called')

    def process_query(self):
        """Runs class's methods together in one function call"""

        self.get_response()
        while not self.valid_search:
            self.validate_response()
        return self.handle_response()


class SearchType(ResponseHandler):
    def __init__(self):
        super().__init__()
        self.input_prompt = "Would you like to use Route Search(RS), Pokemon Search(PS), quit, or help?"
        self.valid_responses = ['rs', 'route search', 'ps', 'pokemon search', 'quit', 'help']
        self.help_text = '''\
        
                            Valid responses are rs, ps, quit, and help. 
                            RS or route search returns all routes that a pokemon appears in. 
                            PS or pokemon search returns all pokemon that appear within a particular route.
                            Quit exits the program.
                        '''

    def handle_response(self):
        """Returns search type class based on user input. Added exception in case of bad validation"""

        if self.response in ['ps', 'pokemon search']:
            return FindPokemonInLocation()
        elif self.response in ['rs', 'route search']:
            return FindLocationOfPokemon()
        else:
            raise Exception('Unexpected search type in self.response')


class FindLocationOfPokemon(ResponseHandler):
    """Object for handling user input, API wrapper calls to PokemonLocationSearch, and output formatting. """
    def __init__(self):
        super().__init__()
        self.help_text = '''\
        
                        This is the Pokemon Search Mode.
                        You can enter a pokemon's name and find what routes it is located in.
                        Enter filter if you would like to limit search to a specific game/generation/console.
                        Enter clear filter if you would like to remove a previous filter.
                        Quit exits the program
                    '''
        self.input_prompt = "Please enter a Pokemon name, filter, clear filter, or quit"
        self.filter_by_game = ''
        self.filter_by_generation = ''
        self.filter_by_console = ''
        self.search = None

    def validate_response(self):
        while True:
            try:
                self.response = '-'.join(self.response.split())
                self.search = PokemonLocationSearch(self.response)
                self.search.create_query_url()
                self.search.query_api()
                self.valid_search = True
                break
            except QueryApiStatusCode404Error:
                print(f'API was unable to find your search of {self.response}')
                self.get_response()

    def handle_response(self):
        self.search.decode_json()
        print(f"{self.response} was found in {len(self.search.location_list)} locations")

        for location in self.search.location_list:
            [print(f"At {location.location_area} in {version.version} via {version.methods}")
             for version in location.version_details]


class FindPokemonInLocation(ResponseHandler):
    """Object for handling user input, API wrapper calls to LocationPokemonSearch, and output formatting. """
    def __init__(self):
        super().__init__()
        self.help_text = '''\
        
                        This is the Route Search Mode.
                        You must enter the Region followed by location name (e.g. Hoenn Route 112).
                        Enter filter if you would like to limit search to a specific encounter type (e.g. fishing).
                        Enter clear filter if you would like to remove a previous filter.
                        Quit exits the program
                    '''
        self.input_prompt = "Please enter RegionName RouteName, filter, clear filter, or quit"
        self.filter_by_encounter_method = ''
        self.location = None
        self.region = None
        self.search = None

    def get_response(self):
        """Checks for help,'', quit. Attempts to get region and location and formats location to be passed into url"""
        self.response = input(f'{self.input_prompt}').lower()

        if self.response == 'help':
            print(dedent(self.help_text))
            self.get_response()
        elif self.response == '':
            print('Please enter a response.')
            self.get_response()
        elif self.response == 'quit':
            exit()
        else:
            pass

        self.region, *self.location = self.response.split()
        self.location = '-'.join(self.location)

        if not self.location:
            print("You must enter the Region followed by the location's name (e.g. Johto Sprout Tower")
            self.get_response()

    def validate_response(self):
        """Checks to see if region + location is valid search, returned location areas shouldn't need error checks"""
        while True:
            try:
                self.search = LocationPokemonSearch(self.location, self.region)
                self.valid_search = True
                break
            except QueryApiStatusCode404Error:
                print(f'API was unable to find your search of Region: {self.region} and Location: {self.location}')
                self.get_response()

    def handle_response(self):
        self.search.query_api()
        self.search.decode_json()

        print(f'{self.location} has {len(self.search.area_names)} sub area(s)')
        for area in self.search.area_encounters:
            print(f'{area.area} contains these pokemon:')
            print(', '.join(area.pokemon_encounters))


class SearchAgain(ResponseHandler):
    def __init__(self, input_search):
        super().__init__()
        self.input_prompt = "Would you like to do another search? (Yes/No/Change Mode)"
        self.valid_responses = ['yes', 'no', 'change mode']
        self.help_text = "\n Valid responses are: yes, no, and change mode"
        self.input_search = input_search

    # TODO: Replace logic with structural pattern matching when python 3.10 is more widely adapted
    def handle_response(self):
        """Returns the same or opposite search type depending on user input."""

        if self.response == 'no':
            exit()
        elif self.response == 'yes' and self.input_search == 'FindLocationOfPokemon':
            return FindLocationOfPokemon()
        elif self.response == 'yes' and self.input_search == 'FindPokemonInLocation':
            return FindPokemonInLocation()
        elif self.response == 'change mode':
            if self.input_search == 'FindLocationOfPokemon':
                return FindPokemonInLocation()
            elif self.input_search == 'FindPokemonInLocation':
                return FindLocationOfPokemon()
            else:
                raise Exception('Unexpected value for input_search.')
