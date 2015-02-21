'''
Created on Sep 28, 2013

@author: alfredroney
'''
import numpy as np
import unittest

def getNumTradingDaysPerYear():
    return 251

#print 'tradingDaysPerYear =',getNumTradingDaysPerYear()

def estimateLogNormalModelFromDailyPrices(p):
    '''
    Input: p -> columns contain time series of daily prices in columns
    Output: (annualGrowthRate,logVolatility)
    '''
    dW = np.diff(np.log(p),axis=0)
    logVolatility = np.std(dW,0)
    drift = np.mean(dW,0)
    annualGrowthRate = np.exp(drift*getNumTradingDaysPerYear()) - 1.0
    return (annualGrowthRate,logVolatility)

def makeLogNormalDailyPriceForecast(growthRate,logVolatility,numTradingDays):
    '''
    Produces a time series representation of the forecast
    and 68% confidence interval.
     
    Input: model parameters, number of days forecast desired.
    Output: (t,mean,upper bound,lower bound)
    '''
    t = np.arange(numTradingDays)
    logu = t*np.log(1.0 + growthRate)/getNumTradingDaysPerYear()
    u = np.exp(logu)
    sigma  = np.sqrt(t)*logVolatility
    splus  = np.exp(logu + sigma)
    sminus = np.exp(logu - sigma)
    return (t,u,splus,sminus)


class estimateLogNormalModelFromDailyPricesTest(unittest.TestCase):
    def test_estimator(self):
        from makeFakeDailyPrices import makeFakeDailyPrices        
        numTradingDays = 4*getNumTradingDaysPerYear()
        annualGrowthRate0 = 3.14
        logVolatility0    = 0.00123
        numCols = 50000 # keep this fairly large to prevent sporadic failures
        
        p = makeFakeDailyPrices(annualGrowthRate0,logVolatility0,
                                numTradingDays,numCols)
        
        annualGrowthRate1,logVolatility1 \
            = estimateLogNormalModelFromDailyPrices(p)
        
        self.assertEqual(annualGrowthRate1.shape,(numCols,))
        self.assertEqual(logVolatility1.shape,(numCols,))
        
        # these may rarely fail due to stochastic nature of the test
        self.assertAlmostEqual(np.mean(annualGrowthRate1),annualGrowthRate0,3)
        self.assertAlmostEqual(np.mean(logVolatility1),logVolatility0,3)

    def test_forecaster(self):
        from makeFakeDailyPrices import makeFakeDailyPrices        
        numTradingDays = getNumTradingDaysPerYear()
        annualGrowthRate = 0.25
        logVolatility    = 0.03125
        numCols = 100000
        
        p = makeFakeDailyPrices(annualGrowthRate,logVolatility,
                                numTradingDays,numCols)

        # get forecast
        t,_,splus,sminus \
        = makeLogNormalDailyPriceForecast(annualGrowthRate, logVolatility,
                                           numTradingDays)

        # count the number of simulated prices that were within the
        # 68% confidence boundaries for each trading day
        inRange = np.zeros(numTradingDays,dtype=np.double)
        for i in range(numCols):
            a = p[:,i] > sminus
            b = p[:,i] < splus
            inRange += a*b
        inRange /= numCols
        expectedFraction = 0.682689
        forecastError = (inRange[1:] - expectedFraction)/expectedFraction
                
        if 0:
            print 'minimum error =',np.min(np.abs(forecastError))*100,'%'
            print 'maximum error =',np.max(np.abs(forecastError))*100,'%'
            import matplotlib.pyplot as plt
            plt.plot(t[1:],forecastError,'b:',linewidth=2)            
            plt.show()

        self.assertTrue(np.all(np.abs(forecastError) < 0.01))