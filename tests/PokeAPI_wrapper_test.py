import pytest
import requests_mock

from ..PokeAPI_wrapper.api_wrapper import *


class TestApiWrapper:
    def test_init(self):
        case_1 = ApiWrapper('region', 'hoenn')
        case_2 = ApiWrapper('generation', '6', region='kalos')

        assert case_1.endpoint == 'region'
        assert case_1.search_id == 'hoenn'
        assert case_1.region is None

        assert case_2.endpoint == 'generation'
        assert case_2.search_id == '6'
        assert case_2.region == 'kalos'

    def test_create_query_url(self):
        case_1 = ApiWrapper('version', '4')
        case_2 = ApiWrapper('version-group', 'ruby-sapphire')

        case_1.create_query_url()
        case_2.create_query_url()

        assert case_1.query_url == 'https://pokeapi.co/api/v2/version/4/'
        assert case_2.query_url == 'https://pokeapi.co/api/v2/version-group/ruby-sapphire/'

    def test_query_api(self):
        case_1 = ApiWrapper('version', '4')
        case_2 = ApiWrapper('version-group', 'ruby-sapphire-emerald')

        case_1.create_query_url()
        case_2.create_query_url()

        with requests_mock.Mocker() as mock_request:
            mock_request.get('https://pokeapi.co/api/v2/version/4/', status_code=200)
            case_1.query_api()

            assert isinstance(case_1.request, requests.models.Response)
            assert case_1.request.status_code == 200

        with pytest.raises(QueryApiStatusCode404Error):
            with requests_mock.Mocker() as mock_request:
                mock_request.get('https://pokeapi.co/api/v2/version-group/ruby-sapphire-emerald/', status_code=404)
                case_2.query_api()


class TestPokemonLocationSearch:
    def test_init(self):
        case_1 = PokemonLocationSearch('zigzagoon')
        case_2 = PokemonLocationSearch('95')

        assert case_1.endpoint == 'pokemon'
        assert case_1.search_filters is None
        assert case_1.search_id == 'zigzagoon'

        assert case_2.endpoint == 'pokemon'
        assert case_2.location_list == []
        assert case_2.search_id == '95'

    def test_create_query_url(self):
        case_1 = PokemonLocationSearch('zigzagoon')
        case_2 = PokemonLocationSearch('95')

        case_1.create_query_url()
        case_2.create_query_url()

        assert case_1.query_url == 'https://pokeapi.co/api/v2/pokemon/zigzagoon/encounters/'
        assert case_2.query_url == 'https://pokeapi.co/api/v2/pokemon/95/encounters/'

    def test_query_api(self):
        case_1 = PokemonLocationSearch('zigzagoon')
        case_2 = PokemonLocationSearch('95')

        case_1.create_query_url()
        case_2.create_query_url()

        with requests_mock.Mocker() as mock_request:
            mock_request.get('https://pokeapi.co/api/v2/pokemon/zigzagoon/encounters/', status_code=200)
            case_1.query_api()

            assert isinstance(case_1.request, requests.models.Response)
            assert case_1.request.status_code == 200

        with pytest.raises(QueryApiStatusCode404Error):
            with requests_mock.Mocker() as mock_request:
                mock_request.get('https://pokeapi.co/api/v2/pokemon/95/encounters/', status_code=404)
                case_2.query_api()

    def test_decode_json(self):
        case_areas = ['sinnoh-route-202-area', 'sprout-tower-2f', 'sprout-tower-3f', 'burned-tower-1f',
                      'burned-tower-b1f', 'bell-tower-2f', 'bell-tower-3f', 'bell-tower-4f', 'bell-tower-5f',
                      'bell-tower-6f', 'bell-tower-7f', 'bell-tower-8f', 'bell-tower-9f', 'bell-tower-10f',
                      'unknown-all-rattata-area', 'petalburg-woods-area', 'hoenn-route-101-area',
                      'hoenn-route-102-area', 'hoenn-route-103-area', 'hoenn-route-104-area',
                      'hoenn-route-110-area', 'hoenn-route-116-area', 'hoenn-route-117-area',
                      'hoenn-route-118-area', 'hoenn-route-119-area', 'hoenn-route-120-area',
                      'hoenn-route-121-area', 'hoenn-route-123-area', 'kalos-route-2-area']

        case = PokemonLocationSearch('zigzagoon')

        with open("zigzagoon_search.json", "r") as mock_data:
            with requests_mock.Mocker() as mock_request:
                mock_request.get('https://pokeapi.co/api/v2/pokemon/zigzagoon/encounters/', json=json.load(mock_data))
                case.create_query_url()
                case.query_api()

            case.decode_json()

            for item in case.location_list:
                assert isinstance(item, PokemonLocation)
                assert item.location_area in case_areas


class TestLocationPokemonSearch:

    def test_init(self):
        case_1 = LocationPokemonSearch('route-40', region='johto')
        case_2 = LocationPokemonSearch('77')

        assert case_1.endpoint == 'location'
        assert case_1.region == 'johto'
        assert case_1.request.url == 'https://pokeapi.co/api/v2/location/johto-sea-route-40/'

        assert case_2.endpoint == 'location'
        assert case_2.area_names == ['ice-path-1f', 'ice-path-b1f', 'ice-path-b2f', 'ice-path-b3f']
        assert case_2.search_id == '77'

    def test_query_api(self):
        case_1 = LocationPokemonSearch('route-40', region='johto')
        case_2 = LocationPokemonSearch('77')

        case_1.query_api()
        case_2.query_api()

        for item in case_1.area_data:
            assert isinstance(item, requests.models.Response)
        for item in case_2.area_data:
            assert isinstance(item, requests.models.Response)

    def test_decode_json(self):
        case_pokemon = [
            ['arbok', 'raichu', 'sandslash', 'golbat', 'gloom', 'parasect', 'venomoth', 'persian', 'psyduck', 'golduck',
             'primeape', 'poliwag', 'poliwhirl', 'kadabra', 'machoke', 'weepinbell', 'geodude', 'graveler', 'slowpoke',
             'slowbro', 'magneton', 'dodrio', 'hypno', 'kingler', 'electrode', 'seadra', 'goldeen', 'seaking',
             'magikarp', 'gyarados', 'ditto', 'wobbuffet', 'makuhita', 'absol', 'chingling', 'bronzor'],
            ['sandslash', 'wigglytuff', 'golbat', 'gloom', 'parasect', 'venomoth', 'psyduck', 'golduck', 'poliwag',
             'poliwhirl', 'kadabra', 'machoke', 'weepinbell', 'geodude', 'graveler', 'magneton', 'dodrio', 'electrode',
             'marowak', 'rhyhorn', 'rhydon', 'chansey', 'goldeen', 'magikarp', 'gyarados', 'ditto', 'wobbuffet',
             'makuhita', 'absol', 'chingling', 'bronzor'],
            ['arbok', 'raichu', 'sandslash', 'golbat', 'parasect', 'psyduck', 'golduck', 'poliwag', 'poliwhirl',
             'kadabra', 'machoke', 'geodude', 'graveler', 'slowpoke', 'slowbro', 'magneton', 'kingler', 'electrode',
             'marowak', 'lickitung', 'rhyhorn', 'rhydon', 'chansey', 'seadra', 'goldeen', 'seaking', 'magikarp',
             'gyarados', 'ditto', 'mewtwo', 'wobbuffet', 'makuhita', 'absol', 'chingling', 'bronzor']]

        case_area_details = [
            {
                'name': 'cerulean-cave-1f',
                'file': 'cerulean_cave_1f_search.json',
                'url': 'https://pokeapi.co/api/v2/location-area/cerulean-cave-1f'
            },
            {
                'name': 'cerulean-cave-2f',
                'file': 'cerulean_cave_2f_search.json',
                'url': 'https://pokeapi.co/api/v2/location-area/cerulean-cave-2f'
            },
            {
                'name': 'cerulean-cave-b1f',
                'file': 'cerulean_cave_b1f_search.json',
                'url': 'https://pokeapi.co/api/v2/location-area/cerulean-cave-b1f'
            }
        ]

        case = LocationPokemonSearch('147')

        # for testing if data changes or server is down
        for i, location_area in enumerate(case.area_names):
            with open(case_area_details[i]['file'], "r") as mock_data:
                with requests_mock.Mocker() as mock_request:
                    mock_request.get(case_area_details[i]['url'], json=json.load(mock_data))
                    case.area_encounters.append(mock_request)

        case.decode_json()
        for item in case.area_encounters:
            assert isinstance(item, LocationAreaEncounters)
            assert item.pokemon_encounters in case_pokemon

        # for testing if server is up
        case.query_api()
        case.decode_json()

        for item in case.area_encounters:
            assert isinstance(item, LocationAreaEncounters)
            assert item.pokemon_encounters in case_pokemon
