"""Interface for converting between Sqg and NetworkX.
"""
import networkx as NX
from pysqg.arrayList import AbstractArrayList, InMemoryArrayList
from pysqg.sqg import Sqg

# return a NetowrkX representation of the given SQG
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
    nxGraph.graph['includes'] = sqg.getIncludes()
    nxGraph.graph['sqgName'] = sqg.getName()
    nxGraph.graph['parents'] = sqg.getParents()
    nxGraph.graph['sharedVariables'] = sqg.getSharedVariables()
    return nxGraph, nxSubgraphs

# returns an SQG representation of the given NetowrkX graphs
# (and optional subgraphs).  
def networkxRead(nxGraph, nxSubgraphList = []):
    sqgName = None
    includes = None
    parents = None
    sharedVariables = None
    if 'includes' in nxGraph.graph:
        includes = nxGraph.graph['includes']
    if 'sqgName' in nxGraph.graph:
        sqgName = nxGraph.graph['sqgName']
    if 'sharedVariables' in nxGraph.graph:
        sharedVariables = nxGraph.graph['sharedVariables']
    if 'parents' in nxGraph.graph:
        parents = nxGraph.graph['parents']
    
    sqg = Sqg(includes=includes, name=sqgName, 
              sharedVariables=sharedVariables, parents=parents)
      
    readNodesFromNX(nxGraph, sqg)
    readEdgesFromNX(nxGraph, sqg)
    readSubgraphsFromNX(nxGraph, nxSubgraphList, sqg)
    return sqg


# private general function

def isSQGDirected(sqg):
    for arrayListType, arrayList in sqg.getArrayLists().items():
        if arrayList.inheritsFrom('directedEdge'):
            return True
    return False
        
def isNXGraphDirected(nxGraph):
    return type(nxGraph) == NX.DiGraph or type(nxGraph) == NX.MultiDiGraph    



# private reading functions

def getSQGVariablesFromNXAttributes(nxAttrib, excludeList = []):
    variables = []
    for key, val in nxAttrib.items():
        if key not in excludeList:
            variables.append(str(key))
            variables.append(str(type(val).__name__))
    return variables

def readNodesFromNX(nxGraph, sqg):
    for node in nxGraph.nodes():
        nodeType = 'node'
        nodeAttrib = nxGraph.node[node]
        nodeArrayDict = nodeAttrib.copy()
        if 'type' in nodeAttrib:
            nodeType = nodeAttrib['type']
            del nodeArrayDict['type']
        nodeArrayDict['nodeName'] = node
        
        nodeArrayList = sqg.getArrayList(nodeType)
        if nodeArrayList is None:
            variables = None
            if nodeType not in AbstractArrayList._arrayListTypes:
                variables = getSQGVariablesFromNXAttributes(nodeArrayDict)
            nodeArrayList = InMemoryArrayList(type=nodeType, variables=variables)
            sqg.setArrayList(nodeArrayList)
        
        nodeArrayList.addDict(nodeArrayDict) 

def readEdgesFromNX(nxGraph, sqg):
    for edge in nxGraph.edges():
        edgeAttrib = nxGraph[edge[0]][edge[1]]
        edgeArrayDict = edgeAttrib.copy()
        if "directed" in edgeAttrib:
            del edgeArrayDict['directed']
            edgeArrayDict["outNode"] = edge[0]
            edgeArrayDict["inNode"] = edge[1]
            edgeType = 'directedEdge'
        else:
            edgeArrayDict["node1"] = edge[0]
            edgeArrayDict["node2"] = edge[1]
            edgeType = 'edge'

        if 'type' in edgeAttrib:
            edgeType = edgeAttrib['type']
            del edgeArrayDict['type']
                
        edgeArrayList = sqg.getArrayList(edgeType)
        if edgeArrayList is None:
            variables = None
            if edgeType not in AbstractArrayList._arrayListTypes:
                variables = getSQGVariablesFromNXAttributes(edgeArrayDict)
            edgeArrayList = InMemoryArrayList(type=edgeType, variables=variables)
            sqg.setArrayList(edgeArrayList)
        
        edgeArrayList.addDict(edgeArrayDict)

def readSubgraphsFromNX(nxGraph, nxSubgraphList, sqg):
    for nxSubgraph in nxSubgraphList:
        subgraphType = 'subgraph'
        edgeTypes = None
        subgraphAttrib = nxSubgraph.graph
        subgraphArrayDict = subgraphAttrib.copy()
        if 'type' in subgraphAttrib:
            subgraphType = subgraphAttrib['type']
            del subgraphArrayDict['type']
        if 'edgeTypes' in subgraphAttrib:
            edgeTypes = subgraphAttrib['edgeTypes']
            del subgraphArrayDict['edgeTypes']
        subgraphArrayDict['nodes'] = nxSubgraph.nodes()
        
        subgraphArrayList = sqg.getArrayList(subgraphType)
        if subgraphArrayList is None:
            variables, sharedVariables = None, None
            if subgraphType not in AbstractArrayList._arrayListTypes:
                variables = getSQGVariablesFromNXAttributes(subgraphArrayDict)
                if edgeTypes is not None:
                    sharedVariables = dict()
                    sharedVariables["edges"] = edgeTypes
            subgraphArrayList = InMemoryArrayList(type=subgraphType, 
                                                  sharedVariables=sharedVariables, 
                                                  variables=variables)
            sqg.setArrayList(subgraphArrayList)
        
        subgraphArrayList.addDict(subgraphArrayDict)



## private writing functions

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
        nxGraph[outNodeName][inNodeName]["directed"] = 1

def writeSubgraphsIntoNX(subgraphArrayList, nxGraph, nxSubgraphs):
    assert nxGraph is not None
    if 'nodes' not in subgraphArrayList.getArrayNames():
        raise RuntimeError("Could not find nodes in subgraph") 
    if 'subgraphName' not in subgraphArrayList.getArrayNames():
        raise RuntimeError("Could not find subgraphName in subgraph") 
    nodesIndex = subgraphArrayList.getArrayNames().index('nodes')
    
    sharedVariables = subgraphArrayList.getSharedVariables()
    assert sharedVariables is not None
    if 'edges' not in sharedVariables:
        raise RuntimeError("Could not edges in subgraph's sharedVariables")
    edgeTypes = sharedVariables['edges']
    
    for subgraphArray in subgraphArrayList:        
        nodes = subgraphArray[nodesIndex]
        nxSubgraph = nxGraph.subgraph(nodes)
        nxSubgraph.graph = dict()
        nxSubgraph.graph['edgeTypes'] = ' '.join(edgeTypes)
        for edge in nxSubgraph.edges():
            edgeAttributes = nxSubgraph[edge[0]][edge[1]]
            assert 'type' in edgeAttributes
            edgeType = edgeAttributes['type']
            if edgeType not in edgeTypes:
                nxSubgraph.remove_edge(edge[0], edge[1])
        setNXAttributesFromArrayList(nxSubgraph.graph, subgraphArrayList,
                                     subgraphArray, [nodesIndex])
        nxSubgraphs.append(nxSubgraph)
        

            
            