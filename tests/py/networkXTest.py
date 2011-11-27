import unittest
import os
from pymongo import Connection
from pysqg.bioio import getTempFile
from pysqg.py.networkX import networkxWrite, networkxRead
from pysqg.arrayList import InMemoryArrayList
import pysqg.tests.abstractTests as abstractTests

class TestCase(abstractTests.AbstractTestCase):
    def setUp(self):
        """Constructs a simple graph to writes it into networkx then reads it back out.
        """
        abstractTests.AbstractTestCase.setUp(self)
        sqg, graph = self.makeGraph(InMemoryArrayList)
        nxGraph, nxSubgraphList = networkxWrite(sqg)    
        self.graphs = [(networkxRead(nxGraph, nxSubgraphList), graph)]
        
    def tearDown(self):
        pass
    
    
def main():
    from pysqg.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()