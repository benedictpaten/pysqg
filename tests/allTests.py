import unittest
import sys
import pysqg.tests.db.allTests
import pysqg.tests.json.allTests
import pysqg.tests.converters.allTests
import pysqg.tests.sqgTest
from sonLib.bioio import parseSuiteTestOptions

def allSuites(): 
    allTests = unittest.TestSuite((pysqg.tests.db.allTests.allSuites,
                                   pysqg.tests.json.allTests.allSuites,
                                   pysqg.tests.converters.allTests.allSuites,
                                   unittest.makeSuite(pysqg.tests.sqg.TestsCase.allTests, 'test')))
                                  
def main():
    parseSuiteTestOptions()
    suite = allSuites()
    runner = unittest.TextTestRunner()
    runner.run(suite)
    i = runner.run(suite)
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())