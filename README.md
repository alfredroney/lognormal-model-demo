Log-normal Model Demo
=====================

![Plot for an ETF](https://github.com/alfredroney/lognormal-model-demo/raw/screenshots/screenshot_SPY.png)

Demonstrates forecasting using a log-normal random walk model. Stock prices downloaded from Yahoo! using Pandas are fit and plotted. Also demonstrates the Python "using" construct, how to create a simple caching data store, and how to use the unittest module. Simple Monte Carlo simulations are used to validate the model fitter and forecasting routines.

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

evaluateLogNormalModel.py - Define a portfolio and set of indices using CSV files, then load them in bulk using the HistoricalQuotesDatabase class. Subsequent analyses will load the cached data instead of fetching the data from Yahoo! for a massive speedup. Once the database is loaded, it steps through each symbol, fitting a log-normal model to the data from five years ago to one year ago, then comparing the predictions to the data for the last year. The analysis is presented using matplotlib plots.

evaluateSecurity.py - Simple analysis script for an ad-hoc set of securities. It fetches each ticker's data in turn, and presents a graphical comparison of the log-normal random walk forecast with reality.

Classes
-------

HistoricalQuotesDatabase.py - Module for caching a frequently-accessed data set.

TemporaryWorkingFolder.py - Module for accessing the data folder using a pseudo-RAII idiom. Changes the working folder, and guarantees that the previous working folder will be restored regardless of exceptions or early return.
