import unittest
import sys
from pysqg.tests import allTests
from sonLib.bioio import parseSuiteTestOptions

def allSuites(): 
    allTests = unittest.TestSuite((allTests.allSuites,))
        
def main():
    parseSuiteTestOptions()
    suite = allSuites()
    runner = unittest.TextTestRunner()
    runner.run(suite)
    i = runner.run(suite)
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())