from response import ResponseHandler, SearchType, RouteSearch, PokemonSearch, SearchAgain


def main():
    print('''
Hello, this is Pokemon Route Search. This program will allow you to search via two methods.
Route search allows you to search for the route(s) in which a particular Pokemon can be found.
Pokemon search allows you to search for the pokemon within a particular route.
''')

    # Handles getting the type of search
    search = SearchType()
    search = search.search_type()

    # Handles the api call and data manipulation of search

    # Allows searching again
    search = SearchAgain(type(search).__name__)  # type(search).__name__ returns current class name of search
    search.search_again()


if __name__ == '__main__':
    main()
