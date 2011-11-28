#!/usr/bin/env python

import sys
import json

from simpleparse.common import numbers, strings, comments
from simpleparse.parser import Parser

from pysqg.sqg import Sqg
from pysqg.arrayList import InMemoryArrayList
from pysqg.jsonSqg import makeJsonSqgFromSqg

################################################
## Lexical parsing
################################################

declaration = r'''# note use of raw string when embedding in python code...
fastg          :=  contig*
contig	       :=  '>',identifier,'\n',body
body           :=  segment*
segment        :=  sequence/construct
construct      :=  gap/tandem/alts
gap            :=  '[gap|',range,']'
tandem         :=  '[tandem|',sequence,'|',range,']'
alts           :=  '[alt',alt+,']'
alt            :=  '|',sequence
range          :=  estimate/range2
estimate       :=  number
range2         :=  number,':',number,':',number
sequence       :=  [ATGCNatgcn-]+
identifier     :=  [a-zA-Z_0-9.]+
number         :=  [0-9.]+
'''

def removeUselessReturns(instream):
	input = ""
	for line in instream:
		if line[0] == ">":
			if len(input) > 0:
				input += '\n'
			input += line
		else:
			input += line.strip()
	return input

def parseInput(input):
	parser = Parser(declaration)
	success, children, nextcharacter = parser.parse(input, production="fastg")
	assert success
	return children

################################################
## Converting parseTree to Sqg
################################################

def sequenceToString(parseTree, input):
	assert parseTree[0] == "sequence"
	return input[parseTree[1]:parseTree[2]]	

def sequenceToSqg(data, parseTree, sqg, input):
	assert parseTree[0] == "sequence"
	myWalk, previous = data

	nodes = sqg.getArrayList('node')
	counter = nodes.size()
	nodes.addArray([ counter ])
	nodes.addArray([ counter + 1])

	sequenceString = sequenceToString(parseTree, input)
	segmentEdges = sqg.getArrayList('multiLabelledSegment')
	segmentEdges.addDict({"outNode":counter, "inNode":counter + 1, "length":len(sequenceString), "sequence":sequenceString, "degree":1})

	adjacencyEdges = sqg.getArrayList('overlapAdjacency')
	for prevNode in previous:
		adjacencyEdges.addDict({ "node1":prevNode, "node2":counter, "overlap":0})

	myWalk.extend([counter, counter+1])
	return myWalk, [counter + 1]

def altToSqg(parseTree, sqg, input, previous):
	assert parseTree[0] == "alt"

	nodes = sqg.getArrayList('node')
	counter = nodes.size()
	sequenceString = sequenceToString(parseTree[3][0], input)
	nodes.addArray([ counter ])
	nodes.addArray([ counter + 1])

	sequenceString = sequenceToString(parseTree[3][0], input)
	segmentEdges = sqg.getArrayList('multiLabelledSegment')
	segmentEdges.addDict({"outNode":counter, "inNode":counter + 1, "length":len(sequenceString), "sequence":sequenceString, "degree":1})

	adjacencyEdges = sqg.getArrayList('overlapAdjacency')
	for prevNode in previous:
		adjacencyEdges.addDict({ "node1":prevNode, "node2":counter, "overlap":0})

def altsToSqg(data, parseTree, sqg, input):
	assert parseTree[0] == "alts"
	myWalk, previous = data
	altToSqg(parseTree[3][0], sqg, input, previous)
	segmentEdges = sqg.getArrayList('node')
	counter = segmentEdges.size()
	myWalk.extend([counter-2, counter-1])
	new = [counter-1]
	
	for index in range(1,len(parseTree[3])):
		altToSqg(parseTree[3][index], sqg, input, previous)
		new += [segmentEdges.size()-1]
	return myWalk, new

def constructToSqg(data, parseTree, sqg, input):
	assert parseTree[0] == "construct"
	child = parseTree[3][0]
	if child[0] == "alts":
		return altsToSqg(data, child, sqg, input)
	elif child[0] == "gap":
		pass
	elif child[0] == "tandem":
		pass
	else:
		assert false # Unknown construct, other than alt, gap or tandem

def segmentToSqg(data, parseTree, sqg, input):
	assert parseTree[0] == "segment"
	child = parseTree[3][0]
	if child[0] == 'sequence':
		return sequenceToSqg(data, child, sqg, input)
	elif child[0] == "construct":
		return constructToSqg(data, child, sqg, input)
	else:
		assert False

def bodyToSqg(parseTree, sqg, input):
	assert parseTree[0] == "body"
	return reduce(lambda X, Y: segmentToSqg(X, Y, sqg, input), parseTree[3], ([],[]))

def contigToSqg(parseTree, sqg, input, counter):
	assert parseTree[0] == "contig"
	myWalk, last = bodyToSqg(parseTree[3][1], sqg, input)
	walks = sqg.getArrayList('walk')
	walks.addDict({"subgraphName":counter, "nodes":myWalk, "start":0, "stop":0})

def initializeSqg():
	sqg = Sqg(includes=['ungappedOverlapGraph'])
	nodes = InMemoryArrayList(type="node")
	segmentEdges = InMemoryArrayList(type="multiLabelledSegment")
	adjacencyEdges = InMemoryArrayList(type="overlapAdjacency")
	walks = InMemoryArrayList(type="walk", inherits="mixedSubgraph", variables=[ "start", "int", "stop", "int" ], sharedVariables={ "edges":[ "segmentEdge", "adjacencyEdge" ] })
	sqg.setArrayList(nodes)
	sqg.setArrayList(segmentEdges)
	sqg.setArrayList(adjacencyEdges)
	sqg.setArrayList(walks)
	return sqg

################################################
## Master functions
################################################

def fastgToSqg(instream):
	input = removeUselessReturns(instream)
	parseTreeList = parseInput(input)
	sqg = initializeSqg()
	for index in range(len(parseTreeList)):
		contigToSqg(parseTreeList[index], sqg, input, index)
	return sqg

def sqgToFastg(sqg):
	pass
			
################################################
## For playing around
################################################

def main():
	jsonGraph = makeJsonSqgFromSqg(fastgToSqg(sys.stdin))
	json.dump(jsonGraph, sys.stdout)

if __name__ == "__main__":
	main()
