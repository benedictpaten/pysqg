import unittest
import sys
import pysqg.tests.converters.allTests
import pysqg.tests.db.allTests
import pysqg.tests.jsonTest
import pysqg.tests.py.allTests
import pysqg.tests.sqgTest
from sonLib.bioio import parseSuiteTestOptions

def allSuites(): 
    return unittest.TestSuite((pysqg.tests.db.allTests.allSuites(),
                               unittest.makeSuite(pysqg.tests.json.TestCase, 'test'),
                               pysqg.tests.converters.allTests.allSuites(),
                               pysqg.tests.py.allTests.allSuites(),
                               unittest.makeSuite(pysqg.tests.sqgTest.TestCase, 'test')))
                                  
def main():
    parseSuiteTestOptions()
    i = unittest.TextTestRunner().run(allSuites())
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())