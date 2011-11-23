import unittest
import sys
import pysqg.tests.converters.allTests
import pysqg.tests.db.allTests
import pysqg.tests.jsonSqgTest
import pysqg.tests.py.allTests
import pysqg.tests.sqgTest
from pysqg.bioio import parseSuiteTestOptions

def allSuites(): 
    return unittest.TestSuite((unittest.makeSuite(pysqg.tests.sqgTest.TestCase, 'test'),
                               unittest.makeSuite(pysqg.tests.jsonSqgTest.TestCase, 'test'),
                               pysqg.tests.converters.allTests.allSuites(),
                               pysqg.tests.py.allTests.allSuites(),
                               pysqg.tests.db.allTests.allSuites()))
                                  
def main():
    parseSuiteTestOptions()
    i = unittest.TextTestRunner().run(allSuites())
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())