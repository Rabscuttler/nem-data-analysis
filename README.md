NEM Analysis
==============================

Holds code, mapping files, data and analysis of various aspects of Australia's National Eletricity Market.


Binder
------------
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/prakaa/nem-data-analysis/7c0802edf08dbd4e069a4801fca79fa0342da343)

Use Binder to run notebooks interactively. Note that resource limits might prevent you from running analysis with high volumes of data.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands for env building and data fetching
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources. Includes data not available on NEMWeb
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- Docs generated using Sphinx.
    │
    ├── notebooks          <- Jupyter notebooks for various analyses.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── Pipfile & lock     <- Project requirements. Makefile can build pipenv env, if pipenv is installed.
    │
    ├── requirements.txt   <- The requirements file. Only contains pipenv for project installation and for
    │                         project initialisatio using Binder. Please use pipenv
    │
    ├── setup.py           <- makes project pip installable (pip install -e .). Retained so src can be
    │                         installed, please use pipenv to install project.
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Functions and scripts to download or generate data
    │   │
    │   ├── plot_helpers   <- Functions and scripts to assist with plotting
    │   │
    │   └── visualization  <- Functions and scripts to create exploratory and results oriented visualizations

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
