import requests, json

# Using PokeAPI


endpoints = [
    'encounter-method',
    'encounter-condition',
    'encounter-condition-value',
    'generation',
    'version',
    'version-group',
    'location',
    'location-area',
    'region',
    'pokemon',
    'pokemon-habitat'
]


# Creating custom errors for to ease debugging
class Error(Exception):
    """Base class for other exceptions"""
    pass


class PokemonNameIdAreNoneError(Exception):
    """Raised when name and id are both equal to None"""


class PokemonNotFoundError(Error):
    """Raised when api query did not find a pokemon matching the search"""
    pass


class LocationNotFoundError(Error):
    """Raised when api query did not find a location matching the search"""
    pass


class PokemonLocation:
    def __init__(self, location_area=None, max_chance=None, min_level=None, max_level=None,
                 condition_values=None, chance=None, encounter_method=None, version=None):
        self.location_area = location_area
        self.max_chance = max_chance
        self.min_level = min_level
        self.max_level = max_level
        self.condition_values = condition_values
        self.chance = chance
        self.encounter_method = encounter_method
        self.version = version

    def __str__(self):
        return f'Location: {self.location_area}'


class PokemonLocationSearch:
    def __init__(self, pokemon_id=None, pokemon_name=None, search_filters=None):
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name
        self.search_filters = search_filters
        self.location_list = []
        self.request = None

    def query_api(self):
        if self.pokemon_id is None and self.pokemon_name is None:
            raise PokemonNameIdAreNoneError('Pokemon id and name are equal to none.')

        self.request = requests.get(
            f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_id or self.pokemon_name}/encounters')

        if self.request.content == b'NotFound':
            raise PokemonNotFoundError("Pokemon was not found in api query")

    def decode_json(self, request):
        self.location_list = [PokemonLocation(location_area=location['location_area']['name']) for location in
                              self.request.json()]
