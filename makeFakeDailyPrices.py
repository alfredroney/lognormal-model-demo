'''
Created on Sep 28, 2013

@author: alfredroney
'''
import numpy as np
from estimateLogNormalModelFromDailyPrices \
    import getNumTradingDaysPerYear, estimateLogNormalModelFromDailyPrices,\
        makeLogNormalDailyPriceForecast
import unittest

def makeFakeDailyPrices(growthRate,logVol,numDays,numCols):
    ''' tested implicitly in estimateLogNormalModelFromDailyPrices '''
    drift = np.log(1.0 + growthRate)/getNumTradingDaysPerYear()
    dW = drift + logVol*np.random.randn(numDays,numCols)
    dW[0,:] = 0.0
    return np.exp(np.cumsum(dW,0))    

class TestMakeFakeDailyPrices(unittest.TestCase):
    def test_meanSquaredDisplacement(self):
        from getMeanSquareDisplacement import getMeanSquareDisplacement
        numTradingDays = 4*getNumTradingDaysPerYear()
        growthRate     = 0.5
        logVolatility  = 2.0**-8
        numCols = 15000
        
        p = makeFakeDailyPrices(growthRate,logVolatility,numTradingDays,numCols)
        
        
        Ex21 = np.mean(getMeanSquareDisplacement(np.log(p),10),1)
        t = np.arange(10)
        volTerm = t*np.square(logVolatility)
        driftTerm = np.square(t*np.log(1.0+growthRate)/getNumTradingDaysPerYear())
        Ex20 = volTerm + driftTerm

        error = np.sqrt(np.mean(np.square((Ex21[1:] - Ex20[1:])/Ex20[1:])))

        self.assertLess(error,0.002)

        if 0:    
            import matplotlib.pyplot as plt
            print 'MSE =',np.round(100*error,3),'%'
            plt.plot(t,Ex21,'ro ')
            plt.plot(t,Ex20,'g:')
            plt.show()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    numTradingDays = getNumTradingDaysPerYear()
    growthRate     = 0.5
    logVolatility  = 0.01
    numCols = 8
    
    p = makeFakeDailyPrices(growthRate,logVolatility,numTradingDays,numCols)
    
    gr,lv = estimateLogNormalModelFromDailyPrices(p)
    
    print 'AGR    =',np.round(np.mean(gr),6),'+/-',np.round(np.std(gr),6)
    print 'logVOL =',np.round(np.mean(lv),6),'+/-',np.round(np.std(lv),6)

    # get forecast
    t,u,splus,sminus \
    = makeLogNormalDailyPriceForecast(growthRate, logVolatility, numTradingDays)
    
    # plot simulated prices
    plt.plot(t,p,'y-')
    
    # plot simulated mean return in absence of volatility
    plt.plot(t,u,'g-',linewidth=2)
    
    # plot edges of 68% confidence interval
    plt.plot(t,splus,'r-',t,sminus,'r-')

    plt.xlabel('trading day')
    plt.ylabel('return')
    
    plt.show()
