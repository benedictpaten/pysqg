"""Interface for writing into Sqg into NetworkX.
"""
import networkx as NX
from pysqg.arrayList import AbstractArrayList
from pysqg.sqg import Sqg

def networkxWrite(sqg):
    if isSQGDirected(sqg):
        nxGraph = NX.DiGraph()
    else:
        nxGraph = NX.Graph()
    nxSubgraphs = []
    for arrayListType, arrayList in sqg.getArrayLists().items():
        writeArrayListIntoNX(arrayList, nxGraph)
    for arrayListType, arrayList in sqg.getArrayLists().items():
        writeArrayListIntoNXSubgraphs(arrayList, nxGraph, nxSubgraphs)
    return nxGraph, nxSubgraphs
    
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
        if isNXGraphDirected(nxGraph):
            nxGraph.add_edge(node2Name, node1Name)
            setNXAttributesFromArrayList(nxGraph[node2Name][node1Name], edgeArrayList, 
                                     edgeArray, [node2Index, node1Index])
            

def writeDirectedEdgesIntoNX(edgeArrayList, nxGraph):
    if not isNXGraphDirected(nxGraph):
        raise RuntimeError("Could not add directed edge undirected nx graph") 
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

def writeSubgraphsIntoNX(subgraphArrayList, nxGraph, nxSubgraphs):
    assert nxGraph is not None
    if 'nodes' not in subgraphArrayList.getArrayNames():
        raise RuntimeError("Could not find nodes in subgraph") 
    if 'subgraphName' not in subgraphArrayList.getArrayNames():
        raise RuntimeError("Could not find subgraphName in subgraph") 
    nodesIndex = subgraphArrayList.getArrayNames().index('nodes')
    subgraphNameIndex = subgraphArrayList.getArrayNames().index('subgraphName')
    
    sharedVariables = subgraphArrayList.getSharedVariables()
    assert sharedVariables is not None
    if 'edges' not in sharedVariables.getArrayNames():
        raise RuntimeError("Could not edges in subgraph's sharedVariables")
    edgesIndex =  sharedVariables.getArrayNames().index(edgesIndex)
    edgeTypes = sharedVariables.getArrayNames()[edgesIndex]
    
    for subgraphArray in subgraphArrayList:        
        subgraphName = subgraphArray[subgraphNameIndex]
        nodes = subgraphArray[nodesIndex]
        nxSubgraph = nxGraph.subgraph(nodes)
        nxSubgraph.graph['subgraphName'] = str(subgraphName)
        nxSubgraph.graph['edgeTypes'] = ' '.join(edgeTypes)
        for edge in nxSubgraph.edges():
            edgeAttributes = nxSubgraph[edge[0]][edge[1]]
            assert 'type' in edgeAttributes
            edgeType = edgeAttributes['type']
            if edgeTYpe not in edgeTypes:
                nxSubgraph.remove_edge(edge)
        setNXAttributesFromArrayList(nxSubgraph.graph, subgraphArrayList,
                                     subgraphArray, [nodesIndex, subgraphNameIndex])
        nxSubgraphs.append(nxSubgraph)
        
def writeArrayListIntoNX(arrayList, nxGraph):
    if arrayList.inheritsFrom('node'):
        writeNodesIntoNX(arrayList, nxGraph)
    elif arrayList.inheritsFrom('edge'):
        writeEdgesIntoNX(arrayList, nxGraph)
    elif arrayList.inheritsFrom('directedEdge'):
        writeDirectedEdgesIntoNX(arrayList, nxGraph)
    elif arrayList.inheritsFrom('subgraph'):
        pass
    else:
        writeMetadataIntoNX(arrayList, nxGraph)

# to be called after writeArrayListIntoNX (ie nxGraph already filled)
def writeArrayListIntoNXSubgraphs(arrayList, nxGraph, nxSubgraphs):
    if arrayList.inheritsFrom('subgraph'):
        writeSubgraphsIntoNX(arrayList, nxGraph, nxSubgraphs)

def isSQGDirected(sqg):
    for arrayListType, arrayList in sqg.getArrayLists().items():
        if arrayList.inheritsFrom('directedEdge'):
            return True
    return False
        
def isNXGraphDirected(nxGraph):
    return type(nxGraph) == NX.DiGraph or type(nxGraph) == NX.MultiDiGraph    
            
            