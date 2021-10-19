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


class PokemonNameIdAreNoneError(Error):
    """Raised when PokemonLocationSearch.name and PokemonLocationSearch.id are both equal to None"""
    pass


class PokemonNotFoundError(Error):
    """Raised when api query did not find a pokemon matching the search"""
    pass


class LocationRegionOrLocationAreNoneError(Error):
    """Raised when LocationPokemonSearch """


class LocationNotFoundError(Error):
    """Raised when API query did not find a location matching the search"""
    pass


class LocationAreaNotFoundError(Error):
    """Raised when API query did not find a location area matching the search"""


# Classes related to creating objects from PokemonSearch API query data
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
            f'''Location Name: {self.location_area}'''
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
            f'''Version Name: {self.version}
Max encounter chance: {self.max_chance}
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
Maximum level: {self.max_level}
Chance: {self.chance}
Encounter Method: {self.encounter_method}
Required Conditions: {self.condition_values}
'''
        return repr_str


class PokemonLocationSearch:
    """Object for handling input name/id and creating request and downstream location/version/encounter objects."""
    def __init__(self, pokemon_id=None, pokemon_name=None, search_filters=None):
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name
        self.search_filters = search_filters

        self.location_list = []
        self.request = None

    def query_api(self):  # TODO: endpoint without value or id returns paginated list of available resources not error
        if self.pokemon_id is None and self.pokemon_name is None:
            raise PokemonNameIdAreNoneError('Pokemon id and name are equal to none.')

        self.request = requests.get(
            f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_id or self.pokemon_name}/encounters')

        if self.request.content == b'NotFound':
            raise PokemonNotFoundError("Pokemon was not found in PokemonLocationSearch.api_query()")
        return

    def decode_json(self):
        self.location_list = [PokemonLocation(
            location_area=location['location_area']['name'],
            version_details=location['version_details'], )
            for location in self.request.json()]


class LocationAreaEncounters:
    """Object for handling encounters within a location and their encounter methods."""
    def __init__(self, area=None):
        self.area = area

        self.pokemon_encounters = []
        self.encounter_methods = None
        self.request = None

    def get_encounters(self):
        self.request = requests.get(f'https://pokeapi.co/api/v2/location-area/{self.area}/')

        if self.request.content == b'NotFound':
            raise LocationAreaNotFoundError(f"The search for the location area: {self.area} returned no results.")

    def decode_json(self):
        self.pokemon_encounters = \
            [encounter['pokemon']['name'] for encounter in self.request.json()['pokemon_encounters']]
        self.encounter_methods = \
            [method['encounter_method']['name'] for method in self.request.json()['encounter_method_rates']]

    def __repr__(self):
        repr_str = f'''Pokemon Encounters: {self.pokemon_encounters}
encounter_methods: {self.encounter_methods}'''


class LocationPokemonSearch:
    """Object for handling input location and creation of request and downstream location/location area objects """
    def __init__(self, region=None, location=None, search_filters=None):
        self.region = region
        self.location = location
        self.search_filters = search_filters

        self.area_list = []
        self.request = None

    def query_api(self):  # TODO: endpoint without value or id returns paginated list of available resources not error
        if self.region is None or self.location is None:
            raise LocationRegionOrLocationAreNoneError("LocationPokemonSearch needs both a region and a location")

        self.request = requests.get(f'https://pokeapi.co/api/v2/location/{self.location}/')

        # Some locations need the region in the URL too
        if self.request.content == b'NotFound':
            self.request = requests.get(f'https://pokeapi.co/api/v2/location/{self.region}-{self.location}/')

        # Some sea routes also need sea in the URL also
        if self.request.content == b'NotFound':
            self.request = requests.get(f'https://pokeapi.co/api/v2/location/{self.region}-sea-{self.location}/')

        if self.request.content == b'NotFound':
            raise LocationNotFoundError("Location was not found in LocationPokemonSearch.query_api()")

    def decode_json(self):
        self.area_list = [areas['name'] for areas in self.request.json()['areas']]
