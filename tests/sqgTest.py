import unittest

from pysqg.sqg import SQG, InMemoryArrayList, StreamingArrayList

class TestCase(unittest.TestCase):
    def setUp(self):
        """Constructs a simple graph to test
        """
        self.graphIncludes = ["multigraph"]
        self.parents = [ "parent" ]
        self.sharedVariables = { "this is a test":None }
        self.sqgName = 1
        self.sqg = SQG(includes=self.graphIncludes, name=self.sqgName, parents=self.parents, sharedVariables=self.sharedVariables)
        
        def fn(type, arrayNames, arrays):
            arrayList = InMemoryArrayList(type=type)
            self.sqg.setArrayList(arrayList)
            i = len(arrays)/2
            for array in arrays[:i]:
                arrayList.addArray(array)
            for array in arrays[i:]:
                arrayList.addDict(dict(zip(arrayNames, array)))
            return arrayList
        
        self.graph = [ (type, arrayNames, arrayTypes, arrays, sharedVariables, fn(type, arrayNames, arrays)) for \
                      type, arrayNames, arrayTypes, arrays, sharedVariables in \
                      (("node", ("nodeName",), ("int",), [ [1], [2], [3], [4], [5] ], {}),
                ("edge", ("node1", "node2"), ("int", "int"), [ [1, 3 ], [1, 4 ] ], {}),
                ("multiDirectedEdge", ("outNode", "inNode", "degree"), ("int", "int", "float"), [ [1, 2, 1 ], [2, 3, 2] ], {}),
                ("mixedSubgraph", ("subgraphName", "nodes"), ("int", "array"), [ ], { "edges":[ "edge", "directedEdge" ]})) ]   
    
    def testSQG_getIncludes(self):
        self.assertEqual(self.sqg.getIncludes(), self.graphIncludes)
        
    def testSQG_getName(self):
        self.assertEqual(self.sqg.getName(), self.sqgName)
    
    def testSQG_getParents(self):
        self.assertEqual(self.sqg.getParents(), self.parents)
        
    def testSQG_getSharedVariables(self):
        self.assertEqual(self.sqg.getSharedVariables(), self.sharedVariables)
    
    def testSQG_getArrayLists(self):
        self.assertEqual(self.sqg.getArrayLists(), dict([ (type, arrayList) for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph ]))
    
    def testSQG_getArrayList(self):
        for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(self.sqg.getArrayList(type), arrayList)
    
    def testArrayList_getType(self):
        for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getType(), type)
    
    def testArrayList_getSharedVariables(self):
        for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getSharedVariables(), sharedVariables)
    
    def testArrayList_getArrayNames(self):
        for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getArrayNames(), arrayNames)
            
    def testArrayList_getArrayTypes(self):
        for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getArrayTypes(), arrayTypes)
    
    def testArrayList_getArrayWidth(self):
        for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph:
            self.assertEqual(arrayList.getArrayWidth(), len(arrayNames))
    
    def testArrayList_iter(self):
        for type, arrayNames, arrayTypes, array, sharedVariables, arrayList in self.graph:
            self.assertEquals([ i for i in arrayList], array)

def main():
    from sonLib.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()