import unittest
import os
from pysqg.bioio import getTempFile
from pysqg.arrayList import InMemoryArrayList, OnDiskArrayList
from pysqg.jsonSqg import readJsonSqgFile, writeJsonSqgFile
import pysqg.tests.abstractTests as abstractTests

class TestCase(abstractTests.AbstractTestCase):
    def setUp(self):
        """Constructs a simple graph to test, testing json parsing in and out..
        """
        abstractTests.AbstractTestCase.setUp(self)
        
        def fn3(type):
            """Make a an on disk array list
            """
            tempFile = getTempFile(rootDir=os.getcwd())
            self.tempFiles.append(tempFile)
            return OnDiskArrayList(file=tempFile, type=type)
        
        def fn4(i, putOnDiskArraysInJsonSqg=False):
            """Write and then re-read the sqg in a temporary file
            """
            sqg, graph = i
            tempFile = getTempFile(rootDir=os.getcwd())
            self.tempFiles.append(tempFile)
            writeJsonSqgFile(sqg, tempFile, putOnDiskArraysInJsonSqg=putOnDiskArraysInJsonSqg)
            sqg = readJsonSqgFile(tempFile)
            return sqg, graph
         
        self.graphs = ((self.makeGraph(InMemoryArrayList), self.makeGraph(fn3), 
                        fn4(self.makeGraph(InMemoryArrayList)), fn4(self.makeGraph(fn3)),
                        fn4(self.makeGraph(fn3), True)))
    
    def tearDown(self):
        abstractTests.AbstractTestCase.tearDown(self)

def main():
    from pysqg.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()