"""
Kriging geographical data
-------------------------

In this example we are going to interpolate actual temperature data from
the German weather service `DWD <https://www.dwd.de/EN>`_.

Data is retrieved utilizing the beautiful package
`wetterdienst <https://github.com/earthobservations/wetterdienst>`_,
which serves as an API for the DWD data.

For better visualization, we also download a simple shapefile of the German
borderline with `cartopy <https://github.com/SciTools/cartopy>`_.
"""
import os
import numpy as np
from cartopy.io import shapereader as shp_read  # version 0.18.0
import geopandas as gp  # 0.8.1
from wetterdienst.dwd import observations as obs  # version 0.13.0


def get_borders_germany():
    """Download simple german shape file with cartopy."""
    shpfile = shp_read.natural_earth("50m", "cultural", "admin_0_countries")
    df = gp.read_file(shpfile)  # only use the simplest polygon
    poly = df.loc[df["ADMIN"] == "Germany"]["geometry"].values[0][0]
    path = os.path.join("..", "data", "de_borders.txt")
    np.savetxt(path, list(poly.exterior.coords))


def get_dwd_temperature(date="2020-06-09 12:00:00"):
    """Get air temperature from german weather stations from 9.6.20 12:00."""
    settings = dict(
        resolution=obs.DWDObservationResolution.HOURLY,
        start_date=date,
        end_date=date,
    )
    sites = obs.DWDObservationStations(
        parameter_set=obs.DWDObservationParameterSet.TEMPERATURE_AIR,
        period=obs.DWDObservationPeriod.RECENT,
        **settings,
    )
    ids, lat, lon = sites.all().loc[:, ["STATION_ID", "LAT", "LON"]].values.T
    observations = obs.DWDObservationData(
        station_ids=ids,
        parameters=obs.DWDObservationParameter.HOURLY.TEMPERATURE_AIR_200,
        periods=obs.DWDObservationPeriod.RECENT,
        **settings,
    )
    temp = observations.all().VALUE.values
    sel = np.isfinite(temp)
    # select only valid temperature data
    ids, lat, lon, temp = ids.astype(float)[sel], lat[sel], lon[sel], temp[sel]
    head = "id, lat, lon, temp"  # add a header to the file
    path = os.path.join("..", "data", "temp_obs.txt")
    np.savetxt(path, np.array([ids, lat, lon, temp]).T, header=head)


get_borders_germany()
get_dwd_temperature(date="2020-06-09 12:00:00")
