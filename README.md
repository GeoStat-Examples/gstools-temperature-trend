[![GS-Frame](https://img.shields.io/badge/github-GeoStat_Framework-468a88?logo=github&style=flat)](https://github.com/GeoStat-Framework)
[![Gitter](https://badges.gitter.im/GeoStat-Examples/community.svg)](https://gitter.im/GeoStat-Examples/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5159727.svg)](https://doi.org/10.5281/zenodo.5159727)

# Finding a temperature trend in DWD data: regression vs. universal kriging

In this example we are going to interpolate temperature data from the
german weather service (DWD) downlaoded through the python package
[wetterdienst](https://github.com/earthobservations/wetterdienst).

In order to find a north-south trend in the data we will compare results from
regression and universal kriging provided by GSTools.


## Structure

The workflow is organized by the following structure:
- `data/` - downloaded temperature data and german border line
- `src/`
  - `00_data_download.py` - downloading routines
  - `01_dwd_krige.py` - interpolation and comparison plot generation
- `results/` - all produced results


## Python environment

Main Python dependencies are stored in `requirements.txt`:

```
gstools==1.3.1
matplotlib
cartopy==0.18.0
geopandas==0.8.1
wetterdienst==0.13.0
```

You can install them with `pip` (potentially in a virtual environment):

```bash
pip install -r requirements.txt
```


## Contact

You can contact us via <info@geostat-framework.org>.


## License

MIT © 2021
