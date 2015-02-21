'''
Created on Oct 6, 2013

@author: alfredroney
'''
from estimateLogNormalModelFromDailyPrices \
    import estimateLogNormalModelFromDailyPrices,\
         makeLogNormalDailyPriceForecast, getNumTradingDaysPerYear
from HistoricalQuotesDatabase import HistoricalQuotesDatabase
import matplotlib.pyplot as plt
import numpy as np
import sys

def getForecast(t,p,ndays):
    pfit = p[-4*ndays:-ndays]
    if len(pfit) < 2:
        raise ValueError('Not enough data for a '+str(ndays)+'-day forecast')    
    tpred = t[-ndays:]
    npred = len(tpred)
    p0 = p[-ndays]
    gr,lv = estimateLogNormalModelFromDailyPrices(pfit)
    _,u,sp,sm = makeLogNormalDailyPriceForecast(gr, lv, npred)
    projstr = 'Projected ' + str(np.round(100.0*gr,1)) + '%'
    actstr  = 'Actual ' \
            + str(np.round(100*(p[-1]/p[-ndays] - 1),1)) + '%'
            
    u  *= p0
    sp *= p0
    sm *= p0
    
    return u,sm,sp,tpred,projstr,actstr

def plotForecast(t,p,u,sm,sp,tpred,projstr,actstr,titleString):
    plt.figure(figsize=(11,8.5))
    plt.plot(t,p)
    plt.plot(tpred,u,'g-',linewidth=2.0)
    plt.plot(tpred,sm,'r-',tpred,sp,'r-')

    maxY = np.max([np.max(p),sp[-1]])
    minY = np.min([np.min(p),sm[-1]])
    plt.ylim(minY,maxY)
    plt.plot([tpred[0],tpred[0]],[minY,maxY],'y:')

    plt.xlabel('trading days')
    plt.ylabel('Adjusted Close ($USD)')
    
    plt.legend(['Market Price','Projected Price','68% Confidence Cone'],loc=2)
    
    plt.title(titleString)
    plt.figtext(0.6,0.12,'Return: ' +projstr + ', ' + actstr,
                bbox=dict(facecolor='white',alpha=0.85,ec='none'))
    plt.show()

def printDivider():
    print '----------------------------------'

def doVisualAnalysis(t,p,ndays,ticker,tickerDesc):
    titleString = ticker
    if tickerDesc:
        titleString +=  ' (' + tickerDesc + ')'
    printDivider()
    print 'Analyzing',titleString+':'
    try:
        u,sm,sp,tpred,projstr,actstr = getForecast(t,p,ndays)
        print projstr
        print actstr    
        plotForecast(t,p,u,sm,sp,tpred,projstr,actstr,titleString)
    except ValueError as valueError:
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print '!! Error while analyzing "'+ticker+'":'
        print '!!', valueError.args[0]
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    except:
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print '!! Unexpected error while analyzing "'+ticker+'":'
        print '!!', sys.exc_info()[1]
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'    
    printDivider()

if __name__ == '__main__':
    db = HistoricalQuotesDatabase()
    
    for ticker in sorted(db['securities']+db['indices']):
        try:
            data = db['prices'][ticker]
            t = data.index
            p = np.array(data['Adj Close'])
            doVisualAnalysis(t,p,getNumTradingDaysPerYear(),ticker,db[ticker])
        except:
            print 'Unexpected error with "'+ticker+'":',
            print sys.exc_info()[0]
            
