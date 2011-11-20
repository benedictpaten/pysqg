import unittest

from pysqg.sqg import SQG, InMemoryArrayList, StreamingArrayList

class TestCase(unittest.TestCase):
    
    def setup(self):
        """Constructs a simple graph to test
        """
        self.graphIncludes = ["multiGraph"]
        self.parents = [ "parent" ]
        self.sharedVariables = { "this is a test":None }
        self.sqg = SQG(1, includes=self.graphIncludes, parents=self.parents, sharedVariables=self.sharedVariables)
        
        def fn(type, arrays):
            arrayList = InMemoryArrayList(type)
            self.sqg.setArrayList(arrayList)
            i = len(arrays)/2
            for array in self.nodesArray[:i]:
                arrayList.addArray(array)
            for array in self.nodesArray[i:]:
                arrayList.nodes.addDict(dict(zip(self.arrayNames, array)))
            return arrayList
        
        self.graph = [ (type, arrayNames, arrays, sharedVariables, fn(type, arrays)) for type, arrayNames, arrays, sharedVariables in \
                      (("node", ("nodeName",), [ [1], [2], [3], [4], [5] ], {}),
                ("edge", ("node1", "node2"), [ [1, 3 ], [1, 4 ] ], {}),
                ("directedMultiEdge", ("outNode", "toNode", "degree"), [ [1, 2, 1 ], [2, 3, 2] ], {}),
                ("mixedSubgraph", ("subgraphName", "nodes"), [ ], { "edges":[ "directed", "undirected" ]})) ]   
    
    def testSQG_getIncludes(self):
        self.assertEqual(self.sqg.getIncludes(), self.graphIncludes)
    
    def testSQG_getParents(self):
        self.assertEqual(self.sqg.getParents(), self.parents)
        
    def testSQG_getSharedVariables(self):
        self.assertEqual(self.sqg.getSharedVariables(), self.sharedVariables)
    
    def testSQG_getArrayLists(self):
        self.assertEqual(self.sqg.getArrayLists(), self.arrayLists)
    
    def testSQG_getArrayList(self):
        for type, arrayNames, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(self.sqg.getArrayList(type), arrayList)
    
    def testArrayList_getType(self):
        for type, arrayNames, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getType(), type)
    
    def testArrayList_getSharedVariables(self):
        for type, arrayNames, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getSharedVariables(), sharedVariables)
    
    def testArrayList_getArrayNames(self):
        for type, arrayNames, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getArrayNames(), arrayNames)
    
    def testArrayList_getArrayWidth(self):
        for type, arrayNames, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getArrayWidth(), len(arrayNames))
    
    def testArrayList_iter(self):
        for type, arrayNames, array, sharedVariables, arrayList in self.graph:
            self.assertEquals([ i for i in arrayList], array)
