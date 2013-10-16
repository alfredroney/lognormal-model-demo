'''
Object for holding and maintaining historical quote data for a user-specified
portfolio of securities + a set of indices.

Created on Sep 11, 2013

@author: alfredroney
'''
import cPickle
import unittest
from TemporaryWorkingFolder import TemporaryWorkingFolder
from getYahooData import loadDataPickle, downloadDataSet
import os

defaultDatabaseFolderPath = os.getcwd() + '/data'
defaultNumYears = 5

databasePickleName   = 'historicalQuotesDatabase.pickle'
securitiesFileName   = 'securities.dat'
indicesFileName      = 'indices.dat'

def loadSymbolDictFromFile(fileName):
    ''' expects a CSV file with two columns: {symbol,desc} '''
    with open(fileName) as f:
        d = {}
        for line in f.readlines():
            symbol,desc = line.strip().split(',')
            symbol = symbol.strip()
            desc = desc.strip()
            if not symbol.startswith('#'):
                d[symbol] = desc
            else:
                print 'Ignoring',symbol,'('+desc+')'
        return d

class HistoricalQuotesDatabase:
    def __init__(self,goOnlineImmediately=True):
        self.databaseFolderPath = defaultDatabaseFolderPath
        self.numYears = defaultNumYears
    
        self.databasePickleName = databasePickleName
        self.securitiesFileName = securitiesFileName
        self.indicesFileName    = indicesFileName
        
        self.data = None
        
        if goOnlineImmediately:
            self.goOnline()

    def goOnline(self):
        self.data = self.tryToLoadDatabase()    
        if not self.data:
            self.updateDatabase()
        print
        print '+------------------------------------------'
        print '| Folder:',self.databaseFolderPath
        print '| Database:',self.databasePickleName
        print '|',len(self['securities']),'securities:',
        print self['securities']
        print '|',len(self['indices']),'indices:',self['indices']
        print '+------------------------------------------'
        print
        
    def tryToLoadDatabase(self):
        try:
            with TemporaryWorkingFolder(self.databaseFolderPath):
                data = loadDataPickle(self.databasePickleName)
                return data
        except:
            return None
        
    def updateDatabase(self):
        try:
            with TemporaryWorkingFolder(self.databaseFolderPath):
                data = {}
                data['securities'] = loadSymbolDictFromFile(self.securitiesFileName)
                data['indices'] = loadSymbolDictFromFile(self.indicesFileName)
                symbols = data['securities'].keys() + data['indices'].keys()
                data['prices'] = downloadDataSet(symbols, self.numYears, None)
    
                for symbol in data['securities'].keys():
                    if not data['prices'].has_key(symbol):
                        del data['securities'][symbol]
    
                for symbol in data['indices'].keys():
                    if not data['prices'].has_key(symbol):
                        del data['indices'][symbol]
    
                if 0 < len(data['securities']) and 0 < len(data['indices']):
                    with open(self.databasePickleName,'wb') as f:
                        cPickle.dump(data,f,cPickle.HIGHEST_PROTOCOL)
                    self.data = data
        except:
            self.data = None

    def __getitem__(self,key):
        if self.data:
            if 'securities' == key or 'indices' == key:
                return self.data[key].keys()
            elif 'prices' == key:
                return self.data[key]
            elif key in self.data['securities']:
                return self.data['securities'][key]
            elif key in self.data['indices']:
                return self.data['indices'][key]
        return None

class TestHistoricalQuotesDatabase(unittest.TestCase):
    def test_HistoricalQuotesDatabase(self):
        hdb = HistoricalQuotesDatabase()
        
        self.assertEqual(hdb.databasePickleName,databasePickleName)
        self.assertEqual(hdb.securitiesFileName,securitiesFileName)
        self.assertEqual(hdb.indicesFileName, indicesFileName)
        
        self.assertNotEqual(None,hdb.data)

        hdb = HistoricalQuotesDatabase(False)

        self.assertEqual(None,hdb.data)
        
        hdb.databasePickleName = 'database_for_test.pickle'
        hdb.securitiesFileName = 'securities_for_test.dat'
        hdb.indicesFileName    = 'indices_for_test.dat'
        hdb.numYears = 1
        hdb.goOnline()
        
        for symbol in hdb['securities']:
            self.assertTrue(hdb['prices'].has_key(symbol))
        for symbol in hdb['indices']:
            self.assertTrue(hdb['prices'].has_key(symbol),symbol)
        
        self.assertEquals(hdb['securities'],['SPY', 'AAPL', 'GLD'])
        self.assertEquals(hdb['indices'],['^IXIC', '^GSPC'])
        