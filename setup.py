import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="PokemonRouteSearch",
    version="1.0.0",
    author="Mason Orr",
    author_email="masoncorr@gmail.com",
    description=("Command line program to search PokeAPI for the locations of a pokemon or the pokemon in a location"),
    license="BSD",
    url="https://github.com/MasonOrr/PokemonRouteSearch",
    packages=['PokeApi_wrapper', 'PokemonRouteSearch'],
    long_description=read('README.md')
)