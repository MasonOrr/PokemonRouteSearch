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

        self.input_prompt = "Would you like to use Route Search(RS), Pokemon Search(PS), (quit), or (help)?"
        self.valid_responses = ['rs', 'route search', 'ps', 'pokemon search', 'quit', 'help']
        self.help_text = '''\
                            Valid responses are rs, ps, quit, and help. 
                            RS or route search returns all routes that a pokemon appears in. 
                            PS or pokemon search returns all pokemon that appear within a particular route.
                            Quit exits the program.
                        '''

    def get_search_type(self):
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


class RouteSearch(ResponseHandler):
    def __init__(self):
        super().__init__()
