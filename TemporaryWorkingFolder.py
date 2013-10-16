'''
Class for Pythonic RAII access to a folder without permanently changing
the global environment.

Created on Sep 11, 2013

@author: alfredroney
'''
import unittest
import os

defaultDataFolderPath = os.getcwd() + '/data'

class TemporaryWorkingFolder:
    '''
    Opens the requested data folder, restores global state when done. See unit tests for details.
    
    usage: with TemporaryWorkingFolder('/path/to/desired/temporary/folder'):
               do_some_file_operations_in_the_folder()
               raise YouMustCatchThisException('Restores previous working folder anyway')
    
    Will raise an OSError if the folder does not exist.
    '''
    def __init__(self,dataFolder=defaultDataFolderPath):
        self.dataFolder = str(dataFolder) # copy to preclude changes
        self.cwd = None
    
    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.dataFolder)
    
    def __exit__(self,exc_type,exc_value,traceback):
        os.chdir(self.cwd) # do first in case print raises
        if exc_type:
            print '!!! EXCEPTION !!!'
            print '       OBJECT :',self.__class__.__name__+'('+self.dataFolder+')'
            print '         TYPE :',exc_type
            print '        VALUE :',exc_value
            print '    TRACEBACK :',traceback
        
class TestTemporaryWorkingFolder(unittest.TestCase):
    def test_RAII(self):
        tmpwd = '/'
        os.chdir(tmpwd)
        self.assertEqual(tmpwd,os.getcwd())
        with TemporaryWorkingFolder():
            self.assertEqual(defaultDataFolderPath,os.getcwd())
        self.assertEqual(tmpwd,os.getcwd())

    def test_RAII_with_exception(self):
        tmpwd = '/'
        os.chdir(tmpwd)
        self.assertEqual(tmpwd,os.getcwd())
        errorString = '(EXPECTED) Testing exception handling'
        try:
            with TemporaryWorkingFolder(defaultDataFolderPath):
                self.assertEqual(defaultDataFolderPath,os.getcwd())
                raise IOError(errorString)
        except IOError as e:
            self.assertEqual(e.message,errorString)
        self.assertEqual(tmpwd,os.getcwd())

    def test_RAII_with_bogus_folder_raises_OSError(self):
        tmpwd = '/'
        os.chdir(tmpwd)
        self.assertEqual(tmpwd,os.getcwd())
        bogusFolder = '/jhgkj/kjhkj/gkjhie/aaaa/bggyha/nbhtn'
        try:
            with TemporaryWorkingFolder(bogusFolder):
                raise IOError('WTF?')
        except OSError as e:
            self.assertEqual(e.strerror,'No such file or directory') # fragile
            self.assertEqual(e.filename,bogusFolder) # fragile?
        except IOError as e:
            self.assertEquals(e.message,'WTF?')
            self.assertTrue(not 'raising OSError on bogus folder')
        self.assertEqual(tmpwd,os.getcwd())
