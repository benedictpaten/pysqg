import unittest
import sys
import pysqg.tests.db.mongoDBTest
from sonLib.bioio import parseSuiteTestOptions

def allSuites(): 
    return unittest.TestSuite((unittest.makeSuite(pysqg.tests.db.mongoDBTest.TestCase, 'test'),))
        
def main():
    parseSuiteTestOptions()
    i = unittest.TextTestRunner().run(allSuites())
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())