from sys import exit
from typing import List
from response import ResponseHandler


def main():
    print('''
Hello, this is Pokemon Route Search. This program will allow you to search via two methods.
Route search allows you to search for the route(s) in which a particular Pokemon can be found.
Pokemon search allows you to search for the pokemon within a particular route.
''')

    while True:
        attain_search_mode()


def attain_search_mode():
    search_mode = None
    response_handler = ResponseHandler()

    while search_mode is None:
        mode_response = input('''Would you like to use Route Search(RS), Pokemon Search(PS), (quit), or (help)?''')
        response_handler.search_mode_handler(mode_response)


def route_search():  # TODO: retrieve/validate data via api wrapper
    return


def pokemon_search():  # TODO: retrieve/validate data via api wrapper
    return


if __name__ == '__main__':
    main()
