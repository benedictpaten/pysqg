"""Creates a sqg representation of the hierarchy of different ArrayLists as a forest with the graphs that define them also represented.
""" 

import os
import sys
import json
import networkx as NX
from pysqg.sqg import Sqg
from pysqg.arrayList import InMemoryArrayList
from pysqg.jsonSqg import makeJsonSqgFromSqg
from pysqg.shared import getPysqgIncludeDir
from pysqg.py.networkX import networkxWrite

inheritanceGraph = Sqg(includes=["mixedGraph"])
arrayLists = InMemoryArrayList(type="arrayLists", inherits="node", variables=[ "name", "string", "arrayNames", "string", "arrayTypes", "string" ]) #Nodes representing array list types
sqgs = InMemoryArrayList(type="sqgs", inherits="node", variables=[ "name", "string" ]) #Nodes representing sqg definitions
inheritEdges = InMemoryArrayList(type="inherit", inherits="directedEdge") #Edges showing inheritance between array lists
graphEdges = InMemoryArrayList(type="graph", inherits="directedEdge") #Edges showing which show which sqg defined which array list

#Add them to the graph
inheritanceGraph.setArrayList(arrayLists)
#inheritanceGraph.setArrayList(sqgs)
inheritanceGraph.setArrayList(inheritEdges)
#inheritanceGraph.setArrayList(graphEdges)

#Build the nodes and connect the graphs to the array types
typeStringsToNodeNamesAndArrays = {}
i = 0
for file in os.listdir(getPysqgIncludeDir()):
    if file[-5:] == ".json":
        Sqg(includes=[file[:-5]]) #This ensures the graphs are in memory
        graphNode = i
        i = i+1
        sqgs.addDict({ "nodeName":graphNode, "name":file[:-5] })
        #Now iterate through the new array list types
        fileHandle = open(os.path.join(getPysqgIncludeDir(), file), 'r')
        jsonSqg = json.load(fileHandle)
        fileHandle.close()
        for arrayListType in jsonSqg.keys(): 
            if arrayListType not in ("name", "include", "parents", "sharedVariables"): #This is very hacky, it would be nice to have a clean way to know which sqg defined which array list.
                arrayList = InMemoryArrayList(type=arrayListType)
                arrayNode = i
                i = i+1
                typeStringsToNodeNamesAndArrays[arrayListType] = (arrayNode, arrayList)
                arrayLists.addDict({ "nodeName":arrayNode, "name":arrayListType, "arrayNames":" ".join(arrayList.getArrayNames()), "arrayTypes":" ".join(arrayList.getArrayTypes()) })
                graphEdges.addDict({ "outNode":graphNode, "inNode":arrayNode })

#Add in the inherits edges
for typeString in typeStringsToNodeNamesAndArrays.keys():
    arrayNode, arrayList = typeStringsToNodeNamesAndArrays[typeString]
    if arrayList.getInherits() != None:
        parentArrayNode, parentArrayList = typeStringsToNodeNamesAndArrays[arrayList.getInherits().getType()]
        inheritEdges.addDict({ "outNode":parentArrayNode, "inNode":arrayNode })


#We're done
print makeJsonSqgFromSqg(inheritanceGraph)

#Here wedump a dot version of the graph, using the networkX interface.
nxDiGraph = NX.DiGraph()
networkxWrite(inheritanceGraph, nxDiGraph)
for node in nxDiGraph.nodes():
    nxDiGraph.node[node]["label"] = nxDiGraph.node[node]["name"]
    if nxDiGraph.node[node]["type"] == "sqgs":
        nxDiGraph.node[node]["shape"] = "box"
NX.drawing.nx_agraph.write_dot(nxDiGraph, sys.stdout)


