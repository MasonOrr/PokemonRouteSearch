import requests

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
    """Pokemon Location object for creating an instance of a location with a list of version differences"""

    def __init__(self, location_area=None, version_details=None):
        self.location_area = location_area
        self.version_details = [LocationVersionDetails(
            version=version['version']['name'],
            max_chance=version['max_chance'],
            encounter_details=version['encounter_details'])
            for version in version_details]

    def __repr__(self):
        repr_str = \
            f'''Location Name: {self.location_area}
-Version Details: 
--{self.version_details}
'''
        return repr_str


class LocationVersionDetails:
    """For creating an instance of game version differences with a list of individual encounter details"""
    def __init__(self, version=None, max_chance=None, encounter_details=None):
        self.version = version
        self.max_chance = max_chance
        self.encounter_details = [EncounterDetails(
            min_level=encounter['min_level'],
            max_level=encounter['max_level'],
            condition_values=[condition['name']  # if statement is for when the list is empty
                              for condition in encounter['condition_values'] if encounter['condition_values']],
            chance=encounter['chance'],
            encounter_method=encounter['method']['name'])
            for encounter in encounter_details]

    def __repr__(self):
        repr_str = \
            f'''--Version Name: {self.version}
--Max encounter chance: {self.max_chance}
---Encounter Details: 
----{self.encounter_details}
'''
        return repr_str


class EncounterDetails:
    """For creating an instance of different encounters"""
    def __init__(self, min_level=None, max_level=None, condition_values=None, chance=None, encounter_method=None):
        self.min_level = min_level
        self.max_level = max_level
        self.condition_values = condition_values
        self.chance = chance
        self.encounter_method = encounter_method

    def __repr__(self):
        repr_str = \
            f'''Minimum level: {self.min_level}
----Maximum level: {self.max_level}
----Chance: {self.chance}
----Encounter Method: {self.encounter_method}
----Required Conditions: {self.condition_values}
'''
        return repr_str


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
        return

    def decode_json(self):
        self.location_list = [PokemonLocation(
            location_area=location['location_area']['name'],
            version_details=location['version_details'], )
            for location in self.request.json()]
