import unittest
import sys
from pysqg.tests import allTests
from pysqg.bioio import parseSuiteTestOptions

def allSuites(): 
    return unittest.TestSuite((allTests.allSuites(),))
        
def main():
    parseSuiteTestOptions()
    i = unittest.TextTestRunner().run(allSuites())
    return len(i.failures) + len(i.errors)
        
if __name__ == '__main__':
    sys.exit(main())