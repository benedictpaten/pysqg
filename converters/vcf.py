#!/usr/bin/env python 

import sys
import datetime
import json

from pysqg.sqg import Sqg
from pysqg.arrayList import InMemoryArrayList
from pysqg.jsonSqg import makeSqgFromJsonSqg

###############################################
## VCF dataholders
###############################################
class VCFVariant(object):
	def __init__(self, pos, ref, alt):
		self.pos = int(pos)
		self.ref = str(ref)
		self.alt = map(str, alt)

	def altStr(self):
		return ",".join(self.alt)

	def variantStr(self, referenceName):
		return "\t".join(map(str, [referenceName, self.pos, '.', self.ref, self.altStr(),'.','PASS','.']))

	def __cmp__(self, other):
		return cmp(self.pos, other.pos)

class VCF(object):
	###############################################
	## Basics
	###############################################
	def __init__(self):
		self.referenceSequences = dict()
		self.variants = dict()
		self.referenceName = "reference.fa"

	###############################################
	## Printing VCF
	###############################################
	def header(self):
		lines = []
		lines.append("##fileFormat=VCFv4.0")
		date = datetime.date.today()
		lines.append("##fileDate=%i%i%i" % (date.year, date.month, date.day))
		lines.append("##source=sqgToVcf")
		lines.append("##reference=%s" % self.referenceName)
		lines.append("#" + "\t".join(["CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO"]) + '\n')
		return "\n".join(lines)

	def variants_reference(self, referenceName):
		return "\n".join(variant.variantStr(referenceName) for variant in sorted(self.variants[referenceName]))

	def variantsStr(self):
		return self.header() + "\n".join(self.variants_reference(X) for X in sorted(self.variants)) + '\n'

	###############################################
	## Printing FastA reference
	###############################################
	def fastaSequence(self, sequence):
		return "\n".join(sequence[start:start+60] for start in range(0, len(sequence), 80))

	def referenceStr2(self, referenceName):
		return ">" + str(referenceName) + "\n" + self.fastaSequence(self.referenceSequences[referenceName])

	def referenceStr(self):
		return "\n".join(self.referenceStr2(X) for X in self.referenceSequences) + '\n'

###############################################
## SQG to VCF Reference
###############################################
def complementBase(base):
	if base == 'A':
		return 'T'
	elif base == 'T':
		return 'A'
	elif base == 'C':
		return 'G'
	elif base == 'G':
		return 'C'
	else:
		assert False

def complement(sequence):
	return map(complementBase, sequence)

def reverse(sequence):
	return "".join(reversed(sequence))

def revcomp(sequence):
	return reverse(complement(sequence))

def getSegmentSequence(node, index):
	segment = index[node]
	if node == segment[0]:
		return segment[4]
	elif node == segment[1]:
		return revcomp(segment[4])
	else:
		assert False # Error in lookup table

def extractNodeSequence(sequence, nodes, index):
	start = nodes.next()
	finish = nodes.next()
	return getSegmentSequence(start, index)

def extractSqgReference(walk, index):
	nodes = list(walk[1])
	sequence = ""
	for i in range(0,len(nodes),2):
		sequence += getSegmentSequence(nodes[i], index)
	return sequence

def extractSqgReferences(sqg, index):
	walks = list(sqg.getArrayList('walk'))
	return dict((i, extractSqgReference(walks[i], index)) for i in range(len(walks)))

###############################################
## SQG to VCF Variants
###############################################
def extractWalkVariants(walk, segmentIndex, adjacencyIndex):
	nodes = list(walk[1])
	distance = 1
	variants = []
	for index in range(0, len(nodes), 2):
		nodeA = nodes[index]
		nodeB = nodes[index+1]
		distance += segmentIndex[nodeA][3]
		if nodeB in adjacencyIndex and len(adjacencyIndex[nodeB]) > 1:
			neighbours = [X[1] for X in adjacencyIndex[nodeB]]
			alts = filter(lambda X: X != nodes[index + 2], neighbours)
			altSequences = [segmentIndex[X][4] for X in alts]
			refSequence = segmentIndex[nodes[index + 2]][4]
			variants.append(VCFVariant(distance, refSequence, altSequences))
	return variants
			

def extractSqgVariants(sqg, segmentIndex, adjacencyIndex):
	walks = list(sqg.getArrayList('walk'))
	return dict((i,extractWalkVariants(walks[i], segmentIndex, adjacencyIndex)) for i in range(len(walks)))

###############################################
## Master functions
###############################################

def sqgToVcf(sqg):
	segmentIndex = dict([(segment[0], segment) for segment in sqg.getArrayList('multiLabelledSegment')] 
		     + [(segment[1], segment) for segment in sqg.getArrayList('multiLabelledSegment')])

	adjacencyIndex = dict()
	for adjacency in sqg.getArrayList('overlapAdjacency'):
		if adjacency[0] not in adjacencyIndex:
			adjacencyIndex[adjacency[0]] = []
		adjacencyIndex[adjacency[0]].append(adjacency)
		if adjacency[1] not in adjacencyIndex:
			adjacencyIndex[adjacency[1]] = []
		adjacencyIndex[adjacency[1]].append(adjacency)
		
	vcf = VCF()
	vcf.referenceSequences = extractSqgReferences(sqg, segmentIndex)
	vcf.variants = extractSqgVariants(sqg, segmentIndex, adjacencyIndex)
	return vcf

def vcfToSqg(sqg):
	pass

###############################################
## Test wrapper
###############################################
def main():
	vcf = sqgToVcf(makeSqgFromJsonSqg(json.load(sys.stdin)))
	file = open(vcf.referenceName, "w")
	file.write(vcf.referenceStr())
	file.close()
	file = open("variants.fa", "w")
	file.write(vcf.variantsStr())
	file.close()

if __name__ == "__main__":
	main()
