import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="shape_to_network",
    version="0.1",
    author="Garvit",
    description="Module to convert the shapefile into the network for analysis",
    long_description=read('README.md'),
    license="open",
    install_requires=['networkx', 'fiona', 'shapely', 'haversine', 'pandas', 'geopandas', 'pandas']
)
