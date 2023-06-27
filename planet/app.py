from datetime import datetime

import ephem
from geopy.geocoders import Nominatim


class Planet:

    def __init__(self, lon: str, lat: str, date: datetime) -> None:
        self.lon = lon
        self.lat = lat
        self.date = date.strftime('%Y/%m/%d')
        self.planets = [
            ephem.Mercury,
            ephem.Venus,
            ephem.Mars,
            ephem.Jupiter,
            ephem.Saturn,
            ephem.Moon,
            ephem.Sun,
        ]
        self.parameters = dict()
        self.dist_coef = ephem.meters_per_au / (1000 * 1000000)

    def planet_parameter(self, ephem_planet: ephem) -> None:

        gatech = ephem.Observer()
        gatech.lon = self.lon
        gatech.lat = self.lat
        gatech.date = self.date

        planet = ephem_planet(gatech)

        self.parameters[f'{planet.name}_earth_distance'] = planet.earth_distance * self.dist_coef
        self.parameters[f'{planet.name}_sun_distance'] = planet.sun_distance * self.dist_coef
        self.parameters[f'{planet.name}_hlat'] = planet.hlat
        self.parameters[f'{planet.name}_hlon'] = planet.hlon
        self.parameters[f'{planet.name}_size'] = planet.size
        self.parameters[f'{planet.name}_radius'] = planet.radius
        self.parameters[f'{planet.name}_a_ra'] = planet.a_ra
        self.parameters[f'{planet.name}_elong'] = planet.elong

    def get_parameters(self):
        for planet in self.planets:
            self.planet_parameter(planet)
        return self.parameters


class Geo:

    def __init__(self, place: str) -> None:
        self.place = place
        self.loc = Nominatim(user_agent="GetLoc")
        self.coord = self._get_coord()

    def _get_coord(self):
        getLoc = self.loc.geocode(self.place)
        return {
            'latitude': getLoc.latitude,
            'longitude': getLoc.longitude,
        }
