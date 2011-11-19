import unittest
import sys
import pysqg.tests.py.networkXTest
import pysqg.tests.py.numpyTest
from sonLib.bioio import parseSuiteTestOptions

def allSuites(): 
    allTests = unittest.TestSuite((unittest.makeSuite(pysqg.tests.py.networkXTest.TestsCase.allTests, 'test'),
                                   unittest.makeSuite(pysqg.tests.py.numpyTest.TestsCase.allTests, 'test')))
        
def main():
    parseSuiteTestOptions()
    suite = allSuites()
    runner = unittest.TextTestRunner()
    runner.run(suite)
    i = runner.run(suite)
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())