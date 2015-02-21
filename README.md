Log-normal Model Demo, v1.1.0
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

Quick Start
-----------
**Linux**

1. Ensure all required packages are installed.
2. Open a new terminal window and switch to a folder with write and execute permissions.
3. Clone this repository and run *evaluateLogNormalModel.py*
    
    git clone https://github.com/alfredroney/lognormal-model-demo.git
    cd lognormal-model-demo
    python evaluateLogNormalModel.py

**Mac OS X**

1. Download and install *Canopy Express* from https://store.enthought.com using the defaults.
2. Follow steps 2-3 from the Linux instructions.

**Windows**

1. Download and install *Canopy Express* from https://store.enthought.com using the defaults.
2. Clone the git repository to a folder with write and execute permissions.
2. Open a new Canopy terminal window.
3. Switch to the cloned repository and run the code:
    
    python evaluateLogNormalModel.py

When you are finished examining a plot, closing the plot window will automatically queue up the next ticker in the portfolio. The tickers of interest are defined in plain text files in the data sub-folder, one-per-line, using a { symbol, comment } format. Comment lines are prefixed with the '#' character.

Utilities
--------

**evaluateLogNormalModel.py** - Define a portfolio and set of indices using CSV files, then load the data in bulk using the HistoricalQuotesDatabase class. Subsequent analyses will load the cached data instead of fetching the data from Yahoo! for a massive speedup. Once the database is loaded, the program steps through each symbol in the database, fitting a log-normal random walk model to the data from five years ago to one year ago, then comparing the predictions to the data for the last year. The analysis is presented using matplotlib plots.

**evaluateSecurity.py** - Simple analysis script for an ad-hoc set of securities specified on the command line. It fetches each ticker's data in turn, and presents a graphical comparison of the forecast with reality.

Classes
-------

**HistoricalQuotesDatabase.py** - Module for caching a frequently-accessed set of daily price quotes downloaded from Yahoo! using *Pandas*.

**TemporaryWorkingFolder.py** - Module for accessing the data folder using a pseudo-RAII idiom. Changes the working folder, and guarantees that the previous working folder will be restored regardless of exceptions or early return

Modules
-------

**getYahooData.py** - Interface to Pandas data download routine.

**makeFakeDailyPrices.py** - Uses a PRNG from *NumPy* to generate test data with specified parameters. Used to test the regression algorithm.

**getMeanSquareDisplacement.py** - Computes the average of the squares of the change in a time series using a simple moving average technique.

**estimateLogNormalModelFromDailyPrices.py** - Given a time series of prices and other parameters, generate a forecast and confidence interval for the underlying security.



