import unittest
import os
from sonLib.bioio import getTempFile, system
from pysqg.sqg import SQG, InMemoryArrayList, OnDiskArrayList, jsonRead, jsonWrite

class TestCase(unittest.TestCase):
    def setUp(self):
        """Constructs a simple graph to test
        """
        self.graphIncludes = ["multigraph"]
        self.parents = [ "parent" ]
        self.sharedVariables = { "this is a test":None }
        self.sqgName = 1
        self.tempFiles = []
        
        
        def fn3(type):
            """Make a an on disk array list
            """
            tempFile = getTempFile(rootDir=os.getcwd())
            self.tempFiles.append(tempFile)
            return OnDiskArrayList(file=tempFile, type=type)
        
        def fn2(arrayListConstructor):
            sqg = SQG(includes=self.graphIncludes, name=self.sqgName, parents=self.parents, sharedVariables=self.sharedVariables)
            
            def fn(type, arrayNames, arrays):
                """Write the arrays into an array list
                """
                arrayList = arrayListConstructor(type=type)
                sqg.setArrayList(arrayList)
                i = len(arrays)/2
                for array in arrays[:i]:
                    arrayList.addArray(array)
                for array in arrays[i:]:
                    arrayList.addDict(dict(zip(arrayNames, array)))
                return arrayList
            
            graph = [ (type, inherits, arrayNames, arrayTypes, arrays, sharedVariables, fn(type, arrayNames, arrays)) for \
                          type, inherits, arrayNames, arrayTypes, arrays, sharedVariables in \
                          (("node", None, ("nodeName",), ("int",), [ [1], [2], [3], [4], [5] ], {}),
                    ("edge", None, ("node1", "node2"), ("int", "int"), [ [3, 4 ], [ 5, 2 ], [1, 3 ], [1, 4 ] ], {}),
                    ("multiDirectedEdge", "directedEdge", ("outNode", "inNode", "degree"), ("int", "int", "float"), [ [1, 2, 1.0 ], [2, 3, 3.3 ] ], {}),
                    ("mixedSubgraph", "subgraph", ("subgraphName", "nodes"), ("int", "array"), [ [ 1, [ 1, 2, 3, 4 ]], [2, [ 2, 3 ]], [4, [ 5 ]] ], { "edges":[ "edge", "directedEdge" ]})) ]  
            
            return sqg, graph
        
        def fn4(i):
            """Write and then re-read the sqg in a temporary file
            """
            sqg, graph = i
            tempFile = getTempFile(rootDir=os.getcwd())
            self.tempFiles.append(tempFile)
            fileHandle = open(tempFile, 'w')
            jsonWrite(sqg, fileHandle)
            fileHandle.close()
            fileHandle = open(tempFile, 'r')
            sqg = jsonRead(fileHandle)
            fileHandle.close()
            return sqg, graph
         
        self.graphs = (fn2(InMemoryArrayList), fn2(fn3), fn4(fn2(InMemoryArrayList)), fn4(fn2(fn3)))
    
    def tearDown(self):
        for tempFile in self.tempFiles:
            os.remove(tempFile)
        
    def testSQG_getIncludes(self):
        for sqg, graph in self.graphs:
            self.assertEqual(sqg.getIncludes(), self.graphIncludes)
        
    def testSQG_getName(self):
        for sqg, graph in self.graphs:
            self.assertEqual(sqg.getName(), self.sqgName)
    
    def testSQG_getParents(self):
        for sqg, graph in self.graphs:
            self.assertEqual(sqg.getParents(), self.parents)
        
    def testSQG_getSharedVariables(self):
        for sqg, graph in self.graphs:
            self.assertEqual(sqg.getSharedVariables(), self.sharedVariables)
    
    def testSQG_getArrayLists(self):
        for sqg, graph in self.graphs:
            self.assertEqual(dict([ (type, arrayList.getType()) for type, arrayList in sqg.getArrayLists().items() ]), dict([ (type, arrayList.getType()) for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph ]))
    
    def testSQG_getArrayList(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                self.assertEqual(sqg.getArrayList(type).getType(), arrayList.getType())
        
    def testArrayList_getType(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                self.assertEqual(arrayList.getType(), type)
                
    def testArrayList_getInherits(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                if inherits == None:
                    self.assertEqual(arrayList.getInherits(), None)
                else:
                    self.assertEqual(arrayList.getInherits().getType(), inherits)
    
    def testArrayList_getSharedVariables(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                self.assertEqual(arrayList.getSharedVariables(), sharedVariables)
    
    def testArrayList_getArrayNames(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                self.assertEqual(arrayList.getArrayNames(), arrayNames)
            
    def testArrayList_getArrayTypes(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                self.assertEqual(arrayList.getArrayTypes(), arrayTypes)
    
    def testArrayList_getArrayWidth(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                self.assertEqual(arrayList.getArrayWidth(), len(arrayNames))
    
    def testArrayList_iter(self):
        for sqg, graph in self.graphs:
            for type, inherits, arrayNames, arrayTypes, array, sharedVariables, arrayList in graph:
                self.assertEquals([ i for i in arrayList], array)

def main():
    from sonLib.bioio import parseSuiteTestOptions
    import sys
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()