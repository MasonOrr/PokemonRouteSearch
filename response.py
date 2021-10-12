from sys import exit
from textwrap import dedent


class ResponseHandler:
    def __init__(self):
        self.input_prompt = ''
        self.response = ''
        self.valid_responses = []
        self.valid_search = False
        self.help_text = ''
        self.context = ''
        return

    def get_response(self):
        """User input prompt based on input_prompt attr and responds to help. lower() to sanitize input"""

        self.response = input(f'{self.input_prompt}').lower()

        if self.response == 'help':
            print(dedent(self.help_text))
            self.get_response()
        return

    def validate_response(self):
        """Checks if user input is in valid_responses attr and informs user of valid options if not. Also quits"""

        if self.response in self.valid_responses:
            self.valid_search = True
            return
        elif self.response == 'quit':
            return exit()
        else:
            print("Please input a valid response. Valid responses are: ",
                  f"{', '.join(item for item in self.valid_responses)} \n")


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
        self.search_type = None

    def set_search_type(self):
        """Returns search type class based on user input. Added exception in case of bad validation"""

        if self.response == 'rs' or 'route search':
            return RouteSearch()
        elif self.response == 'ps' or 'pokemon search':
            return PokemonSearch()
        else:
            raise Exception('Unexpected search type in self.response')


class PokemonSearch(ResponseHandler):
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

    def validate_response(self):
        return
        # prompt again if failed
    # alter data to be printed


class RouteSearch(ResponseHandler):
    def __init__(self):
        super().__init__()
        self.help_text = '''\
                        This is the Route Search Mode.
                        You can enter a Route and find what pokemon are located in it.
                        Enter filter if you would like to limit search to a specific encounter type (e.g. fishing).
                        Enter clear filter if you would like to remove a previous filter.
                        Quit exits the program
                    '''
        self.input_prompt = "Please enter a Route name, filter, clear filter, or quit"
        self.filter_by_encounter = ''

    def validate_response(self):
        return
        # prompt again if failed
    # alter data to be printed


class SearchAgain(ResponseHandler):
    def __init__(self):
        super().__init__()
        self.input_prompt = "Would you like to do another search? (Yes/No/Change Mode)"
        self.valid_responses = ['yes', 'no', 'change mode']
        self.help_text = "Valid responses are: yes, no, and change mode"
        self.search_type

    def handle_response(self):
        """Returns the same or opposite search type depending on user input."""
        if self.response == 'yes':
            search_type = search_type.__init__()
            # TODO: Refactor attain_search_type in main.py to search again
        elif self.response == 'no':
            exit()
        elif self.response == 'change mode':
            if isinstance(search_type, PokemonSearch):
                search_type = RouteSearch()
                # TODO: Refactor attain_search_type in main.py to search again
            elif isinstance(search_type, RouteSearch):
                search_type = PokemonSearch
                # TODO: Refactor attain_search_type in main.py to search again
