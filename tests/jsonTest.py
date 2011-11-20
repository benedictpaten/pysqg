import unittest

from pysqg.json import jsonRead, jsonWrite
from pysqg.sqg import getPysqgIncludeDir

class TestCase(unittest.TestCase):    
    def testJsonRead(self):
        for include in ("graph", "digraph", "mixedGraph", "multiGraph", "breakpointGraph", "adjacencyGraph", "segmentGraph", "phylogeneticTree", "dnaHistoryGraph"):
            sqg = jsonRead(os.path.join(getPysqgIncludeDir(), include))
            self.assertEqual(sqg.getType() == include)
    
    def testJsonWrite(self):
        pass