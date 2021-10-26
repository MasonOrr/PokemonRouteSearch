import pytest
from _pytest.monkeypatch import MonkeyPatch
from PokemonRouteSearch.response_handler import *


class TestResponseHandler:
    def test_get_response(self):
        print_patch = MonkeyPatch()

        with pytest.raises(SystemExit):
            case_1 = ResponseHandler()
            print_patch.setattr('builtins.input', lambda _: 'quit')
            case_1.get_response()

        case_2 = ResponseHandler()
        print_patch.setattr('builtins.input', lambda _: 'route SEARCH')
        case_2.get_response()
        assert case_2.response == 'route search'

    def test_handle_response(self):
        with pytest.raises(Exception):
            case = ResponseHandler()
            case.handle_response()


class TestSearchType:
    def test_validate_response(self):
        case_1 = SearchType()
        case_2 = SearchType()

        case_1.response = 'rs'
        case_2.response = 'berry search'

        case_1.validate_response()

        def ignore_confirmed(arg):
            return
        ignore_get_response = MonkeyPatch()
        ignore_get_response.setattr(SearchType, "get_response", ignore_confirmed)

        assert case_1.valid_search
        assert not case_2.valid_search

    def test_handle_response(self):
        case_1 = SearchType()
        case_2 = SearchType()
        case_3 = SearchType()

        case_1.response = 'rs'
        case_2.response = 'ps'
        case_3.response = 'How did I get here?'

        case_1_return = case_1.handle_response()
        case_2_return = case_2.handle_response()

        assert isinstance(case_1_return, FindLocationOfPokemon)
        assert isinstance(case_2_return, FindPokemonInLocation)
        with pytest.raises(Exception):
            assert case_3.handle_response()


class TestPokemonSearch:
    def test_validate_response(self):
        pass

    def test_handle_response(self):
        pass


class TestRouteSearch:
    def test_validate_response(self):
        pass

    def test_handle_response(self):
        pass


class TestSearchAgain:
    def test_validate_response(self):
        pass

    def test_handle_response(self):
        pass
