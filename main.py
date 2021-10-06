from sys import exit


def main():
    print('''
Hello, this is Pokemon Route Search. This program will allow you to search via two methods.
Route search allows you to search for the route(s) in which a particular Pokemon can be found.
Pokemon search allows you to search for the pokemon within a particular route.
''')

    while True:
        attain_search_mode()


def attain_search_mode():
    """This function allows the user to enter what search mode they
    would like to use, ask for help, and to quit the program when finished

	Takes user input on mode and compares it to a list of possible inputs.
	Then it calls the desired search function, returns a help string, or quits the program
	"""

    mode_response_list = ['rs', 'route search', 'ps', 'pokemon search', 'quit', 'help']

    while True:
        mode_response = input('''Would you like to use Route Search(RS), Pokemon Search(PS), (quit), or (help)?''')

        if mode_response.lower() not in mode_response_list:
            print("Please input a valid response. Valid responses are: ",
                  f"{', '.join(str(response) for response in mode_response_list)}")

        elif mode_response.lower() == 'quit':
            print('Thank you for using Pokemon Route Search.')
            exit()
        elif mode_response.lower() == 'help':
            print('''
Valid responses are rs, ps, quit, and help. 
RS or route search returns all routes that a pokemon appears in. 
PS or pokemon search returns all pokemon that appear within a particular route.
Quit exits the program.
''')

        else:
            search_mode = mode_response.lower()
            break
    if search_mode == 'rs' or 'route_search':
        route_search()

    elif search_mode == 'ps' or 'pokemon search':
        pokemon_search()


def route_search():  # TODO: retrieve/validate data via api wrapper
    return


def pokemon_search():  # TODO: retrieve/validate data via api wrapper
    return


if __name__ == '__main__':
    main()
