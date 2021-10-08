from response import ResponseHandler, SearchType


def main():
    print('''
Hello, this is Pokemon Route Search. This program will allow you to search via two methods.
Route search allows you to search for the route(s) in which a particular Pokemon can be found.
Pokemon search allows you to search for the pokemon within a particular route.
''')
    attain_search_type()


# Gets and validates user input. Then sets search_type to desired mode.
def attain_search_type():
    search_type_handler = SearchType()

    while not search_type_handler.valid_search:
        search_type_handler.get_response()
        search_type_handler.validate_response()

    search_type = search_type_handler.get_search_type()


if __name__ == '__main__':
    main()
