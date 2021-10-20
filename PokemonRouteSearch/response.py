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

    def get_response(self):
        """User input prompt based on input_prompt attr and responds to help. lower() to sanitize input"""

        self.response = input(f'{self.input_prompt}').lower()

        if self.response == 'help':
            print(dedent(self.help_text))
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
            return PokemonSearch()
        elif self.response in ['rs', 'route search']:
            return RouteSearch()
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
        # check api if valid response
            # self.valid_search = True
            # return
        # if invalid
            # print to user that search was bad
            # self.get_response()
        return

    def handle_response(self):  # alter data to be returned to user
        return


# TODO: depending on api can also see if handle_response() and validate_response() are also inheritable
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
        self.filter_by_encounter_method = ''

    def validate_response(self):
        # check api if valid response
            # self.valid_search = True
            # Return
        # if invalid
            # print to user that search was bad
            # self.get_response()
        return

    def handle_response(self):  # alter data to be returned to user
        return


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
        elif self.response == 'yes' and self.input_search == 'RouteSearch':
            return RouteSearch()
        elif self.response == 'yes' and self.input_search == 'PokemonSearch':
            return PokemonSearch()
        elif self.response == 'change mode':
            if self.input_search == 'RouteSearch':
                return PokemonSearch()
            elif self.input_search == 'PokemonSearch':
                return RouteSearch()
            else:
                raise Exception('Unexpected value for input_search.')
