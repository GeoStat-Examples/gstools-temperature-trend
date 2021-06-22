"""
Kriging geographical data
-------------------------

In this example we are going to interpolate actual temperature data from
the German weather service `DWD <https://www.dwd.de/EN>`_.
"""
import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import gstools as gs


border = np.loadtxt(os.path.join("..", "data", "de_borders.txt"))
ids, lat, lon, temp = np.loadtxt(os.path.join("..", "data", "temp_obs.txt")).T

###############################################################################
# First we will estimate the variogram of our temperature data.
# As the maximal bin distance we choose 8 degrees, which corresponds to a
# chordal length of about 900 km.

bins = gs.standard_bins((lat, lon), max_dist=np.deg2rad(8), latlon=True)
bin_c, vario = gs.vario_estimate((lat, lon), temp, bin_edges=bins, latlon=True)

###############################################################################
# Now we can use this estimated variogram to fit a model to it.
# Here we will use a :any:`Spherical` model. We select the ``latlon`` option
# to use the `Yadrenko` variant of the model to gain a valid model for lat-lon
# coordinates and we rescale it to the earth-radius. Otherwise the length
# scale would be given in radians representing the great-circle distance.
#
# We deselect the nugget from fitting and plot the result afterwards.
#
# .. note::
#
#    You need to plot the Yadrenko variogram, since the standard variogram
#    still holds the ordinary routine that is not respecting the great-circle
#    distance.

model = gs.Spherical(latlon=True, rescale=gs.EARTH_RADIUS)
model.fit_variogram(bin_c, vario, nugget=False)
ax = model.plot("vario_yadrenko", x_max=bin_c[-1])
ax.scatter(bin_c, vario)
ax.set_xlabel("great circle distance / radians")
ax.set_ylabel("semi-variogram")
fig = ax.get_figure()
fig.savefig(os.path.join("..", "results", "variogram.pdf"), dpi=300)
print(model)

###############################################################################
# As we see, we have a rather large correlation length of 600 km.
#
# Now we want to interpolate the data using Universal and Regression kriging
# in order to compare them.
# We will use a north-south drift by assuming a linear correlation
# of temperature with latitude.


def north_south_drift(lat, lon):
    """North south trend depending linearly on latitude."""
    return lat


uk = gs.krige.Universal(
    model=model,
    cond_pos=(lat, lon),
    cond_val=temp,
    drift_functions=north_south_drift,
)

# fit linear regression model for temperature depending on latitude
regress = stats.linregress(lat, temp)
trend = lambda x, y: regress.intercept + regress.slope * x

dk = gs.krige.Detrended(
    model=model,
    cond_pos=(lat, lon),
    cond_val=temp,
    trend=trend,
)

###############################################################################
# Now we generate the kriging field, by defining a lat-lon grid that covers
# the whole of Germany. The :any:`Krige` class provides the option to only
# krige the mean field, so one can have a glimpse at the estimated drift.

g_lat = np.arange(47, 56.1, 0.1)
g_lon = np.arange(5, 16.1, 0.1)

field1 = uk((g_lat, g_lon), mesh_type="structured", return_var=False)
mean = uk((g_lat, g_lon), mesh_type="structured", only_mean=True)
field2 = dk((g_lat, g_lon), mesh_type="structured", return_var=False)


###############################################################################
# And that's it. Now let's have a look at the generated field and the input
# data along with the estimated mean:

levels = np.linspace(5, 23, 64)
fig, ax = plt.subplots(1, 3, figsize=[10, 5], sharey=True)
sca = ax[0].scatter(lon, lat, c=temp, vmin=5, vmax=23, cmap="coolwarm")
co1 = ax[1].contourf(g_lon, g_lat, field1, levels, cmap="coolwarm")
co2 = ax[2].contourf(g_lon, g_lat, field2, levels, cmap="coolwarm")

[ax[i].plot(border[:, 0], border[:, 1], color="k") for i in range(3)]
[ax[i].set_xlim([5, 16]) for i in range(3)]
[ax[i].set_xlabel("Longitude / °") for i in range(3)]
ax[0].set_ylabel("Latitude / °")

ax[0].set_title("Temperature observations at 2m\nfrom DWD (2020-06-09 12:00)")
ax[1].set_title("Universal Kriging\nwith North-South drift")
ax[2].set_title("Regression Kriging\nwith North-South trend")

fmt = dict(orientation="horizontal", shrink=0.5, fraction=0.1, pad=0.2)
fig.colorbar(co2, ax=ax, **fmt).set_label("T / °C")
fig.savefig(os.path.join("..", "results", "kriging.pdf"), dpi=300)

###############################################################################
# To get a better impression of the estimated north-south drift, we'll take
# a look at a cross-section at a longitude of 10 degree:

fig, ax = plt.subplots()
label = "latitude-temperature scatter"
reg_trend = trend(g_lat, g_lon)
ax.scatter(lat, temp, c="silver", alpha=1.0, edgecolors="none", label=label)
ax.plot(g_lat, field1[:, 50], label="Interpolated temperature at 10° lon")
ax.plot(g_lat, mean[:, 50], label="North-South drift: Universal Kriging")
ax.plot(g_lat, reg_trend, label="North-South trend: Regression Kriging")
ax.set_ylim(7)
ax.set_xlabel("Latitude / °")
ax.set_ylabel("T / °C")
ax.set_title("North-South cross-section")
ax.legend()
fig.savefig(os.path.join("..", "results", "trend.pdf"), dpi=300)
