from pysqg.sqg import Sqg
sqg = Sqg(includes=[ "ungappedOverlapGraph" ], \
sharedVariables={ "Created":"Assemblathon File Format Working Group using Richard Durbin's example", "Date":"24/11/2011"})
from pysqg.arrayList import InMemoryArrayList
nodes = InMemoryArrayList(type="node")
sqg.setArrayList(nodes)
sqg.getArrayList("node")
nodes.getArrayNames()
nodes.getArrayTypes()
_1 = 0
nodes.addArray([ _1 ])
_2 = 1
nodes.addDict({ "nodeName":_2 })
from pysqg.arrayList import OnDiskArrayList
segmentEdges = OnDiskArrayList(file="./segmentEdges", type="multiLabelledSegment")
sqg.setArrayList(segmentEdges)
segmentEdges.getArrayNames()
segmentEdges.getArrayTypes()
aL, aR = 2, 3
nodes.addArray([ aL ])
nodes.addArray([ aR ])
segmentEdges.addDict({ "inNode":aL, "outNode":aR, "length":10, \
"sequence":"acggtcagca", "degree":1 })
b1L, b1R = 4, 5
nodes.addArray([ b1L ])
nodes.addArray([ b1R ])
segmentEdges.addDict({ "inNode":b1L, "outNode":b1R, "length":6, \
"sequence":"catact", "degree":2 })
b2L, b2R = 6, 7
nodes.addArray([ b2L ])
nodes.addArray([ b2R ])
segmentEdges.addDict({ "inNode":b2L, "outNode":b2R, "length":6, \
"sequence":"cgtact", "degree":1 })
cL, cR = 8, 9
nodes.addArray([ cL ])
nodes.addArray([ cR ])
segmentEdges.addDict({ "inNode":cL, "outNode":cR, "length":8, \
"sequence":"ggactcta", "degree":2 })
dL, dR = 10, 11
nodes.addArray([ dL ])
nodes.addArray([ dR ])
segmentEdges.addDict({ "inNode":dL, "outNode":dR, "length":10, \
"sequence":"agcgtgcata", "degree":1 })
adjacencyEdges = OnDiskArrayList(file="./adjacencyEdges", type="overlapAdjacency")
sqg.setArrayList(adjacencyEdges)
adjacencyEdges.getArrayNames()
adjacencyEdges.getArrayTypes()
adjacencyEdges.addDict({ "node1":_1, "node2":aL, "overlap":-1})
adjacencyEdges.addDict({ "node1":aR, "node2":b1L, "overlap":-2})
adjacencyEdges.addDict({ "node1":b1R, "node2":b1L, "overlap":0})
adjacencyEdges.addDict({ "node1":b1R, "node2":cR, "overlap":-1})
adjacencyEdges.addDict({ "node1":cL, "node2":b2R, "overlap":0})
adjacencyEdges.addDict({ "node1":b2L, "node2":cL, "overlap":-1})
adjacencyEdges.addDict({ "node1":cR, "node2":dL, "overlap":-1})
adjacencyEdges.addDict({ "node1":dR, "node2":_2, "overlap":0})
for node1, node2, overlap in adjacencyEdges:
	print "node1", node1, "node2", node2, "overlap", overlap

mixedSubgraphs = InMemoryArrayList(type="mixedSubgraph")
mixedSubgraphs.getArrayNames()
mixedSubgraphs.getArrayTypes()

mixedSubgraphs.getSharedVariables()

walks = InMemoryArrayList(type="walk", inherits="mixedSubgraph", variables=[ "start", "int", "stop", "int" ])
sqg.setArrayList(walks)
walks.getArrayNames()
walks.getArrayTypes()

walks.addDict({ "subgraphName":0, "nodes":[ _1, aL, aR, b1L, b1R, b1L, b1R, cR, cL, b2R, b2L, cL, cR, dL, dR, _2 ], "start":0, "stop":0 })
walks.addDict({ "subgraphName":1, "nodes":[ aL, aR, b1L, b1R, b1L, b1R, cR, cL, b2L, b2R, cL, cR, dL, dR ], "start":3, "stop":10 })

from pysqg.jsonSqg import makeJsonSqgFromSqg
jsonSqg = makeJsonSqgFromSqg(sqg)
print jsonSqg
from pysqg.jsonSqg import makeSqgFromJsonSqg
makeSqgFromJsonSqg(jsonSqg)
makeJsonSqgFromSqg(sqg, putOnDiskArraysInJsonSqg=True)

import os
os.remove("./segmentEdges")
os.remove("./adjacencyEdges")

