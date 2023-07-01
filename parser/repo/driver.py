from parser.db import client


def create_tables():
    client.command("""CREATE TABLE quake.quakes
    (
        Magnitude Float64,
        Date DateTime('Europe/London'),
        Longitude Float64,
        Latitude Float64,
        Mercury_earth_distance Float64,
        Mercury_sun_distance Float64,
        Mercury_hlat Float64,
        Mercury_hlon Float64,
        Mercury_size Float64,
        Mercury_radius Float64,
        Mercury_a_ra Float64,
        Mercury_elong Float64,
        Venus_earth_distance Float64,
        Venus_sun_distance Float64,
        Venus_hlat Float64,
        Venus_hlon Float64,
        Venus_size Float64,
        Venus_radius Float64,
        Venus_a_ra Float64,
        Venus_elong Float64,
        Mars_earth_distance Float64,
        Mars_sun_distance Float64,
        Mars_hlat Float64,
        Mars_hlon Float64,
        Mars_size Float64,
        Mars_radius Float64,
        Mars_a_ra Float64,
        Mars_elong Float64,
        Jupiter_earth_distance Float64,
        Jupiter_sun_distance Float64,
        Jupiter_hlat Float64,
        Jupiter_hlon Float64,
        Jupiter_size Float64,
        Jupiter_radius Float64,
        Jupiter_a_ra Float64,
        Jupiter_elong Float64,
        Saturn_earth_distance Float64,
        Saturn_sun_distance Float64,
        Saturn_hlat Float64,
        Saturn_hlon Float64,
        Saturn_size Float64,
        Saturn_radius Float64,
        Saturn_a_ra Float64,
        Saturn_elong Float64,
        Moon_earth_distance Float64,
        Moon_sun_distance Float64,
        Moon_hlat Float64,
        Moon_hlon Float64,
        Moon_size Float64,
        Moon_radius Float64,
        Moon_a_ra Float64,
        Moon_elong Float64,
        Sun_earth_distance Float64,
        Sun_sun_distance Float64,
        Sun_hlat Float64,
        Sun_hlon Float64,
        Sun_size Float64,
        Sun_radius Float64,
        Sun_a_ra Float64,
        Sun_elong Float64
    )
    ENGINE = MergeTree()
    PRIMARY KEY (Longitude, Latitude, Date)
    """)


def drop_tables():
    client.command('DROP TABLE quakes')
