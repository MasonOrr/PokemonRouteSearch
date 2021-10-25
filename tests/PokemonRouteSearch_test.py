import pytest
from _pytest.monkeypatch import MonkeyPatch
from ..PokemonRouteSearch.response import *


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
    def test_init(self):
        pass

    def test_validate_response(self):
        pass

    def test_handle_response(self):
        pass

    def test_process_query(self):
        pass


class TestPokemonSearch:
    def test_init(self):
        pass

    def test_validate_response(self):
        pass

    def test_handle_response(self):
        pass

    def test_process_query(self):
        pass


class TestRouteSearch:
    def test_init(self):
        pass

    def test_validate_response(self):
        pass

    def test_handle_response(self):
        pass

    def test_process_query(self):
        pass


class TestSearchAgain:
    def test_init(self):
        pass

    def test_validate_response(self):
        pass

    def test_handle_response(self):
        pass

    def test_process_query(self):
        pass
