import ephem
from geopy.geocoders import Nominatim


class Planet:


    def __init__(self, lon: str, lat: str, date: str) -> None:
        self.lon = lon
        self.lat = lat
        self.date = date
        self.planets = [ephem.Mercury, ephem.Venus, ephem.Mars, ephem.Jupiter, ephem.Saturn, ephem.Moon]
        self.parametrs = dict()

    def planet_parametr(self, ephem_planet: ephem) -> None:

        gatech = ephem.Observer()
        gatech.lon = self.lon
        gatech.lat = self.lat
        gatech.date = self.date

        planet = ephem_planet(gatech)
        self.parametrs[f'{planet.name}_earth_distance'] = planet.earth_distance * ephem.meters_per_au / (1000 *1000000)
        self.parametrs[f'{planet.name}_sun_distance'] = planet.sun_distance * ephem.meters_per_au / (1000 *1000000)
        self.parametrs[f'{planet.name}_hlat'] = planet.hlat
        self.parametrs[f'{planet.name}_hlon'] = planet.hlon
        self.parametrs[f'{planet.name}_size'] = planet.size
        self.parametrs[f'{planet.name}_radius'] = planet.radius
        self.parametrs[f'{planet.name}_a_ra'] = planet.a_ra
        self.parametrs[f'{planet.name}_elong'] = planet.elong

    def get_parametrs(self):
        for planet in self.planets:
            self.planet_parametr(planet)
        return self.parametrs


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
