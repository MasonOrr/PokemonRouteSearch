import requests, json
from .response_models import PokemonLocation, LocationAreaEncounters


endpoints = {
  "encounter-condition": "https://pokeapi.co/api/v2/encounter-condition/{self.search_id}/",
  "encounter-condition-value": "https://pokeapi.co/api/v2/encounter-condition-value/{self.search_id}/",
  "encounter-method": "https://pokeapi.co/api/v2/encounter-method/{self.search_id}/",
  "generation": "https://pokeapi.co/api/v2/generation/{self.search_id}/",
  "location": "https://pokeapi.co/api/v2/location/{self.search_id}/",
  "location-area": "https://pokeapi.co/api/v2/location-area/{self.search_id}/",
  "pokemon": "https://pokeapi.co/api/v2/pokemon/{self.search_id}/encounters/",
  "region": "https://pokeapi.co/api/v2/region/{self.search_id}/",
  "version": "https://pokeapi.co/api/v2/version/{self.search_id}/"
}


# region Creating custom errors for to ease debugging
class Error(Exception):
    """Base class for other exceptions"""
    pass


class QueryApiStatusCode404Error(Error):
    """Raised when ApiWrapper.query_api() receives a 404 status code."""


class RegionIsNoneError(Error):
    """Raised when the location endpoint requires a region and object has no region attribute"""
# endregion


# region ApiWrapper and subclasses for handling api query to PokeAPI
class ApiWrapper:
    # TODO: docstring
    def __init__(self, endpoint, search_id, region=None, search_filters=None):
        self.endpoint = endpoint
        self.search_id = search_id
        self.region = region
        self.search_filters = search_filters

        self.query_url = None
        self.request = None
        self.response_list = []

    def create_query_url(self):
        self.query_url = endpoints[self.endpoint]

    def query_api(self):  # TODO: endpoint without value or id returns paginated list of available resources not error
        self.request = requests.get(self.query_url)

        if self.request.status_code == 404:
            raise QueryApiStatusCode404Error(f"{self.query_url} returned 404 status code.")


class PokemonLocationSearch(ApiWrapper):
    """Subclass of ApiWrapper for the LocationSearch query. Creates PokemonLocation objects based on query."""
    def __init__(self, search_id, **kwargs):
        super().__init__(search_id, **kwargs)
        self.endpoint = "pokemon"

        self.location_list = []

    def decode_json(self):
        self.location_list = [PokemonLocation(
            location_area=location['location_area']['name'],
            version_details=location['version_details'], )
            for location in self.request.json()]


class LocationPokemonSearch(ApiWrapper):
    """Subclass of ApiWrapper for the PokemonSearch query. Creates LocationAreaObjects objects based on query.

    This programs current terminal based design makes searching by location areas from user input too difficult
    a lot of knowledge about the underlying naming conventions and game data. The extra logic in the __init__
    takes the more human usable location as input and creates a list of areas needed for the query.
    """
    def __init__(self, search_id, **kwargs):
        super().__init__(search_id, **kwargs)
        self.endpoint = "location"

        # getting list of areas within location
        self.request = requests.get(self.query_url)

        # Some locations need the region in url
        if self.request.status_code == 404:
            if self.region is None:
                raise RegionIsNoneError(
                    f"LocationPokemonSearch has no region and might need it to complete the query.")
            self.request = requests.get(f'https://pokeapi.co/api/v2/location/{self.region}-{self.search_id}/')

        # Some sea routes need the region and sea in url
        if self.request.status_code == 404:
            self.request = requests.get(f'https://pokeapi.co/api/v2/location/{self.region}-sea-{self.search_id}/')

        if self.request.status_code == 404:
            raise QueryApiStatusCode404Error(f"{self.query_url} returned 404 status code.")

        self.area_names = [areas['name'] for areas in self.request.json()['areas']]
        self.area_data = []
        self.area_encounters = []

    # TODO: endpoint without value or id returns paginated list of available resources not error
    def query_api(self):
        self.area_data = \
            [requests.get(f'https://pokeapi.co/api/v2/location-area/{area}/').json() for area in self.area_names]

        for query in self.area_data:
            if query.status_code == 404:
                raise QueryApiStatusCode404Error("A query in area_data returned a 404 status code.")

    def decode_json(self):
        self.area_encounters = [LocationAreaEncounters(
            area=area['name'],
            pokemon_encounters=[encounter['pokemon']['name'] for encounter in area['pokemon_encounters']],
            encounter_methods=[method['encounter_method']['name'] for method in area['encounter_method_rates']]
        ) for area in self.area_data]
# endregion
