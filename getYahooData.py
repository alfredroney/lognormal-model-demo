'''
Get daily historical price data for a symbol.

Created on Sep 10, 2013

@author: alfredroney
'''
import datetime as dt
import cPickle
from pandas.io.data import DataReader
import urllib
import urllib2

# The word on the web is that you can specify a start and 
# end date for the data, but Yahoo! always seems to return
# the full data set, so I don't bother with the dates.
yfURL = 'http://ichart.finance.yahoo.com/table.csv?'

def warnUser(msg):
    print '!!! WARNING !!! --',msg

def downloadLatestCSVFor(symbol):
    ''' Download the most recent data set for the specified symbol. '''
    try:
        symbolURL = yfURL + urllib.urlencode({ 's' : symbol })
        response = urllib2.urlopen(symbolURL)
        data = response.read()
        return data
    except:
        warnUser('Unable to download data for "'+symbol+'"')
    return None

def downloadDataFrameFor(symbol,numYears=5):
    ''' Uses the pandas DataReader function to fetch historical data for a given symbol '''
    try:
        endDate = dt.datetime.today()
        startDate = endDate - dt.timedelta(weeks=numYears*52)
        data = DataReader(symbol,'yahoo',startDate,endDate)
        return data
    except:
        warnUser('Unable to download data for "'+symbol+'"')
    return None

def downloadDataSet(symbols,numYears,pickleName='historicalData.pickle'):
    frames = {}
    for symbol in symbols:
        print 'Downloading historical record for "'+symbol+'" . . .'
        data = downloadDataFrameFor(symbol,numYears)
        if data:
            frames[symbol] = data
    if len(frames.keys()):
        if pickleName:
            print 'Pickling data set to "'+pickleName+'" . . .'
            with open(pickleName,'wb') as f:
                cPickle.dump(frames,f,cPickle.HIGHEST_PROTOCOL)
        return frames
    else:
        warnUser('NO DATA RETRIEVED')
    return None

def loadDataPickle(pickleName='historicalData.pickle'):
    with open(pickleName) as f:
        return cPickle.load(f)
    return None

if __name__ == '__main__':
    import os
    import sys
    if 3 > len(sys.argv):
        print
        print 'usage:',os.path.split(sys.argv[0])[-1],
        print '[years of data] [symbol 1] ([symbol 2] ...)'
        print
        print 'Downloads daily data from Yahoo! for the specified'
        print 'symbols as pandas DataFrame objects, and saves them'
        print 'to a pickle file.'
        print
        sys.exit(1)

    yearsData = int(sys.argv[1])
    symbols = sys.argv[2:]
    frames = downloadDataSet(symbols,yearsData)
    for key in frames:
        print key,frames[key]


