# region Custom errors for easier debugging
class Error(Exception):
    """Base class for other exceptions"""
    pass


class LocationAreaNotFoundError(Error):
    """Raised when API query did not find a location area matching the search"""
# endregion


# region Classes related to creating objects from '/pokemon/{id or name}/encounters/' endpoint
class PokemonLocation:
    """Pokemon Location object for creating an instance of a location with a list of version differences"""

    def __init__(self, location_area=None, version_details=None):
        self.location_area = location_area
        self.version_details = [PokemonLocationVersionDetails(
            version=version['version']['name'],
            max_chance=version['max_chance'],
            encounter_details=version['encounter_details'])
            for version in version_details]

    def __repr__(self):
        repr_str = \
            f'''Location Name: {self.location_area}'''
        return repr_str


class PokemonLocationVersionDetails:
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
# endregion


# region Classes related to creating objects from '/location-area/{id or name}/' endpoint
class LocationAreaEncounters:
    """Object for handling encounters within a location and their encounter methods."""
    def __init__(self, area=None, pokemon_encounters=None, encounter_methods=None):
        self.area = area
        self.pokemon_encounters = pokemon_encounters
        self.encounter_methods = encounter_methods

    def __repr__(self):
        repr_str = f'''Pokemon Encounters: {self.pokemon_encounters}
encounter_methods: {self.encounter_methods}'''
        return repr_str
# endregion
