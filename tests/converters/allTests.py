import unittest
import sys
import pysqg.tests.converters.fastaTest
from pysqg.bioio import parseSuiteTestOptions

def allSuites(): 
    return unittest.TestSuite((unittest.makeSuite(pysqg.tests.converters.fastaTest.TestCase, 'test'),))
        
def main():
    parseSuiteTestOptions()
    i = unittest.TextTestRunner().run(allSuites())
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())