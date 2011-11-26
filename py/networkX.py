"""Interface for writing into Sqg into NetworkX.
"""
import networkx as NX
from pysqg.arrayList import AbstractArrayList
from pysqg.sqg import Sqg

def networkxWrite(sqg, nxGraph):
    for arrayListType, arrayList in sqg.getArrayLists().items():
        writeArrayListIntoNX(arrayList, nxGraph)
    
def setNXAttributesFromArrayList(nxAttrib, arrayList, newArray, excludeList):
    names = arrayList.getArrayNames()
    nxAttrib["type"] = arrayList.getType()  
    for i in range(len(newArray)):
        if i not in excludeList:
            nxAttrib[names[i]] = newArray[i]

def writeNodesIntoNX(nodeArrayList, nxGraph):
    if 'nodeName' not in nodeArrayList.getArrayNames():
        raise RuntimeError("Could not find nodeName in node array") 
    nodeNameIndex = nodeArrayList.getArrayNames().index('nodeName')
                
    for nodeArray in nodeArrayList:
        nodeName = nodeArray[nodeNameIndex]
        nxGraph.add_node(nodeName)
        setNXAttributesFromArrayList(nxGraph.node[nodeName], nodeArrayList, 
                                     nodeArray, [nodeNameIndex])
        
def writeEdgesIntoNX(edgeArrayList, nxGraph):
    if 'node1' not in edgeArrayList.getArrayNames():
        raise RuntimeError("Could not find node1 in edge array")
    if 'node2' not in edgeArrayList.getArrayNames():
        raise RuntimeError("Could not find node2 in edge array")    
    node1Index = edgeArrayList.getArrayNames().index('node1')
    node2Index = edgeArrayList.getArrayNames().index('node2')
    
    for edgeArray in edgeArrayList:
        node1Name = edgeArray[node1Index]
        node2Name = edgeArray[node2Index]
        nxGraph.add_edge(node1Name, node2Name)
        setNXAttributesFromArrayList(nxGraph[node1Name][node2Name], edgeArrayList, 
                                     edgeArray, [node1Index, node2Index])

def writeDirectedEdgesIntoNX(edgeArrayList, nxGraph):
    if 'outNode' not in edgeArrayList.getArrayNames():
        raise RuntimeError("Could not find outNode in edge array")
    if 'inNode' not in edgeArrayList.getArrayNames():
        raise RuntimeError("Could not find inNode in edge array")    
    outNodeIndex = edgeArrayList.getArrayNames().index('outNode')
    inNodeIndex = edgeArrayList.getArrayNames().index('inNode')
    
    for edgeArray in edgeArrayList:
        outNodeName = edgeArray[outNodeIndex]
        inNodeName = edgeArray[inNodeIndex]
        nxGraph.add_edge(outNodeName, inNodeName)
        setNXAttributesFromArrayList(nxGraph[outNodeName][inNodeName], edgeArrayList, 
                                     edgeArray, [outNodeIndex, inNodeIndex])
        
def writeArrayListIntoNX(arrayList, nxGraph):
    if arrayList.inheritsFrom('node'):
        writeNodesIntoNX(arrayList, nxGraph)
    elif arrayList.inheritsFrom('edge'):
        writeEdgesIntoNX(arrayList, nxGraph)
    elif arrayList.inheritsFrom('directedEdge'):
        writeDirectedEdgesIntoNX(arrayList, nxGraph)
    elif arrayList.inheritsFrom('subgraph'):
        writeSubgraphsIntoNX(arrayList, nxGrgaph)
    else:
        writeMetadataIntoNX(arrayList, nxGraph)
        
    
        
            
            