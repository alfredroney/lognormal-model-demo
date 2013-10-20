Log-normal Model Demo
=====================

![Plot for an ETF](https://github.com/alfredroney/lognormal-model-demo/raw/screenshots/screenshot_SPY.png)

Demonstrates forecasting using a log-normal random walk model. Also demonstrates the Python "using" pseudo-RAII idiom, how to create a simple caching data store interface using *Pandas* and *cPickle*, and how to use the *unittest* module. Simple Monte Carlo simulations are employed to empirically validate the model fitter and forecasting routines.

Requirements
------------
1. Python 2.7
1. NumPy
1. MatPlotLib
1. Pandas
1. Internet connection
1. Graphical display

Utilities
--------

**evaluateLogNormalModel.py** - Define a portfolio and set of indices using CSV files, then load the data in bulk using the HistoricalQuotesDatabase class. Subsequent analyses will load the cached data instead of fetching the data from Yahoo! for a massive speedup. Once the database is loaded, the program steps through each symbol in the database, fitting a log-normal random walk model to the data from five years ago to one year ago, then comparing the predictions to the data for the last year. The analysis is presented using matplotlib plots.

**evaluateSecurity.py** - Simple analysis script for an ad-hoc set of securities specified on the command line. It fetches each ticker's data in turn, and presents a graphical comparison of the forecast with reality.

Classes
-------

**HistoricalQuotesDatabase.py** - Module for caching a frequently-accessed set of daily price quotes downloaded from Yahoo! using *Pandas*.

**TemporaryWorkingFolder.py** - Module for accessing the data folder using a pseudo-RAII idiom. Changes the working folder, and guarantees that the previous working folder will be restored regardless of exceptions or early return.
