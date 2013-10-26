'''
Created on Oct 20, 2013

@author: alfredroney
'''
from estimateLogNormalModelFromDailyPrices import getNumTradingDaysPerYear
from evaluateLogNormalModel import doVisualAnalysis
from getYahooData import downloadDataFrameFor
import numpy as np

if __name__ == '__main__':
    import sys
    import os
    
    if len(sys.argv) < 3:
        print
        print 'usage:',os.path.split(sys.argv[0])[-1],
        print '[Number of Years] [ticker 1] ([ticker 2]...)'
        print
        print 'Makes pretty graphs for evaluating potential investments.'
        print
        sys.exit(1)
    
    numYears = int(sys.argv[1])
    
    for ticker in sys.argv[2:]:
        try:
            data = downloadDataFrameFor(ticker,numYears)
            t = data.index
            p = np.array(data['Adj Close'])
            doVisualAnalysis(t,p,getNumTradingDaysPerYear(),ticker,None)
        except:
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            print '!! Error while analyzing',ticker
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            