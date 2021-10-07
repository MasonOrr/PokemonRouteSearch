class ResponseHandler:
    def search_mode_handler(self, response):
        """Interprets users response and returns selected mode"""

        search_mode = None
        allowed_responses = ['rs', 'route search', 'ps', 'pokemon search', 'quit', 'help']

        if response.lower() not in allowed_responses:
            print("Please input a valid response. Valid responses are: ",
                  f"{', '.join(str(response) for response in allowed_responses)}")

        elif response.lower() == 'quit':
            print('Thank you for using Pokemon Route Search.')
            exit()

        elif response.lower() == 'help':
            print('''
Valid responses are rs, ps, quit, and help. 
RS or route search returns all routes that a pokemon appears in. 
PS or pokemon search returns all pokemon that appear within a particular route.
Quit exits the program.
''')

        elif response.lower() == 'rs' or 'route_search':
            search_mode = "route_search"

        elif response.lower() == 'ps' or 'pokemon search':
            search_mode = "pokemon_search"

    def pokemon_search_handler(self):
        return

    def route_search_handler(self):
        return