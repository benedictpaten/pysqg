import unittest
import sys
import pysqg.tests.py.networkXTest
import pysqg.tests.py.numpyTest
from pysqg.bioio import parseSuiteTestOptions

def allSuites(): 
    return unittest.TestSuite((unittest.makeSuite(pysqg.tests.py.networkXTest.TestCase, 'test'),
                                   unittest.makeSuite(pysqg.tests.py.numpyTest.TestCase, 'test')))
        
def main():
    parseSuiteTestOptions()
    i = unittest.TextTestRunner().run(allSuites())
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())