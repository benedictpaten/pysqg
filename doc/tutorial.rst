Quick Tutorial
==============

Overview
--------

In this tutorial we will go through the process of constructing an SQG file.
The example will build a graph derived from Richard Durbin's original example, and is shown 
in the following:

.. image:: example1.png
	:width: 700px

It represents an assembly problem.
The top of the diagram shows subsequences, termed *segments* aligned to an underlying sequence.
The lower diagram shows an *overlap graph* of the segments and their overlaps, which we
term *adjacencies*.

The Sqg Class
-------------

To construct the containing SQG object we start by importing the ``Sqg`` class and creating
an instance: 

>>> from pysqg.sqg import Sqg
>>> sqg = Sqg(includes=[ "ungappedOverlapGraph" ], \
... sharedVariables={ "Created":"Assemblathon File Format Working Group using \
Richard Durbin's example", "Date":"24/11/2011"})

Both arguments passed to the Sqg constructor are optional. 

The ``includes=[ "ungappedOverlapGraph" ]`` argument takes a list of graph *types*. 
Like in the C programming
language they are used to load pre-existing jsonSqg files that contain existing graph 
definitions.
For a full list of these graphs see the next chapter.

The *sharedVariables* argument is simply a python dictionary object (hash) used 
to describe properties of the graph.

The ArrayList Class
-------------------

Nodes, edges and subgraphs, the basic structures described by SQG, are 
represented as lists of typed arrays. ArrayLists use an inheritance mechanism
to allow complex types to be defined hierarchically.

We start by building a list of nodes:

>>> from pysqg.arrayList import InMemoryArrayList
>>> nodes = InMemoryArrayList(type="node")
>>> sqg.setArrayList(nodes)

The basic ArrayList class is defined in the ``pysqg.arrayList.AbstractArrayList``
class. This class is abstract, but inherited ArrayLists, here the ``InMemoryArrayList``,
allow ArrayLists with specific storage properties. The ``InMemoryArrayList`` used
here stores, as you would expect, the information it contains in memory.

The ``type="node"`` argument, which is required is used to define the type of the
arrayList. The nodes are added to the sqg object by the ``setArrayList`` function.
Only one type of a given list is allowed per Sqg instance.

The list can be retrieved from the sqg object by the following:

>>> sqg.getArrayList("node")
<pysqg.arrayList.InMemoryArrayList instance at 0x1086aa7e8>

As you might expect, each node is represented by an array with a single variable:

>>> nodes.getArrayNames()
('nodeName',)

Which is assumed to be an integer:

>>> nodes.getArrayTypes()
('int',)

To start to populate the graph we create the two *stub* nodes _1 and _2, which
represent boundaries of the graph and are often convenient, for example to represent
telomeres or more generally missing information.

>>> _1 = 0
>>> nodes.addArray([ _1 ])
>>> _2 = 1
>>> nodes.addDict({ "nodeName":_2 })

The above fragment shows the two ways to add an array to an ArrayList. Firstly,
as a list, and secondly as a dictionary (hash).

Edges as more complex ArrayLists
--------------------------------

The process of adding edges and more complex types to the graph follows exactly
the same process as the nodes.

>>> from pysqg.arrayList import OnDiskArrayList
>>> segmentEdges = OnDiskArrayList(file="./segmentEdges", type="multiLabelledSegment")
>>> sqg.setArrayList(segmentEdges)

The above fragment loads the ``OnDiskArrayList`` class, which stores the arrays it
contains on disk, and therefore is suitable where the number of edges is too large to fit
into memory. The ``file="./segmentEdges"`` required argument specifies the file
to store the arrayList's contents in. This time the ``type="multiLabelledSegment"`` argument
specifies the use of more complex arrayList type representing a segment edge:

>>> segmentEdges.getArrayNames()
('outNode', 'inNode', 'degree', 'length', 'sequence')
>>> segmentEdges.getArrayTypes()
('int', 'int', 'float', 'int', 'string')

We can now proceed to add the segment edges to the graph.

The *a* segment:

>>> aL, aR = 2, 3
>>> nodes.addArray([ aL ])
>>> nodes.addArray([ aR ])
>>> segmentEdges.addDict({ "inNode":aL, "outNode":aR, "length":10, \
... "sequence":"acggtcagca", "degree":1 })

Each edge addition involves the creation of two nodes, representing the segment
ends.

The *b1* segment:

>>> b1L, b1R = 4, 5
>>> nodes.addArray([ b1L ])
>>> nodes.addArray([ b1R ])
>>> segmentEdges.addDict({ "inNode":b1L, "outNode":b1R, "length":6, \
... "sequence":"catact", "degree":2 })

The *b2* segment:

>>> b2L, b2R = 6, 7
>>> nodes.addArray([ b2L ])
>>> nodes.addArray([ b2R ])
>>> segmentEdges.addDict({ "inNode":b2L, "outNode":b2R, "length":6, \
... "sequence":"cgtact", "degree":1 })

The *c* segment:

>>> cL, cR = 8, 9
>>> nodes.addArray([ cL ])
>>> nodes.addArray([ cR ])
>>> segmentEdges.addDict({ "inNode":cL, "outNode":cR, "length":8, \
... "sequence":"ggactcta", "degree":2 })

And finally the *d* segment:

>>> dL, dR = 10, 11
>>> nodes.addArray([ dL ])
>>> nodes.addArray([ dR ])
>>> segmentEdges.addDict({ "inNode":dL, "outNode":dR, "length":10, \
... "sequence":"agcgtgcata", "degree":1 })

The other edges in the graph represent the *adjacencies*, the connections between
the ends of the segments. 

>>> adjacencyEdges = OnDiskArrayList(file="./adjacencyEdges", type="overlapAdjacency")
>>> sqg.setArrayList(adjacencyEdges)

Here they are allowed to overlap, hence we use the 
``overlapAdjacency`` type. The array variables are shown below.

>>> adjacencyEdges.getArrayNames()
('node1', 'node2', 'overlap')
>>> adjacencyEdges.getArrayTypes()
('int', 'int', 'int')

Given this type we can add the adjacencies to the graph.

>>> adjacencyEdges.addDict({ "node1":_1, "node2":aL, "overlap":-1})
>>> adjacencyEdges.addDict({ "node1":aR, "node2":b1L, "overlap":-2})
>>> adjacencyEdges.addDict({ "node1":b1R, "node2":b1L, "overlap":0})
>>> adjacencyEdges.addDict({ "node1":b1R, "node2":cR, "overlap":-1})
>>> adjacencyEdges.addDict({ "node1":cL, "node2":b2R, "overlap":0})
>>> adjacencyEdges.addDict({ "node1":b2L, "node2":cL, "overlap":-1})
>>> adjacencyEdges.addDict({ "node1":cR, "node2":dL, "overlap":-1})
>>> adjacencyEdges.addDict({ "node1":dR, "node2":_2, "overlap":0})

ArrayList objects are purposefully very limited in their abilities, 
being designed as means to store information but not randomly access it. Rather
we choose to make it simple to convert sqg instances and their arrayLists into
other formats, for example into databases and more complex in memory and on disk storage
mechanisms that provide such functionality. The key means to access the arrays in an arrayList
we use iterators. For example:

>>> for node1, node2, overlap in adjacencyEdges:
...     print "node1", node1, "node2", node2, "overlap", overlap
... 
node1 0 node2 2 overlap -1
node1 3 node2 4 overlap -2
node1 5 node2 4 overlap 0
node1 5 node2 9 overlap -1
node1 8 node2 7 overlap 0
node1 6 node2 8 overlap -1
node1 9 node2 10 overlap -1
node1 11 node2 1 overlap 0

Shows how it is possible to iterate through the adjacency edges of the Sqg.
To convert the arrayList into the JSON based SQG format

Subgraphs as Walks
------------------

Todo. Define subgraph type and show walks.


Reading and writing SQG files
-----------------------------

To convert the ``sqg`` object into a SQG file we use an associated conversion function:

>>> from pysqg.jsonSqg import makeJsonSqgFromSqg
>>> jsonSqg = makeJsonSqgFromSqg(sqg)
>>> print jsonSqg
{'node': [{'sharedVariables': {}, 'variables': ['nodeName', 'int']}, \
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]], 'multiLabelledSegment': \
[{'inherits': 'multiSegment', 'sharedVariables': {}, 'variables': \
['inNode', 'int', 'degree', 'float', 'length', 'int', 'sequence', 'string']}, \
[3, 2, 1.0, 10, 'acggtcagca', 5, 4, 2.0, 6, 'catact', 7, 6, 1.0, 6, 'cgtact', \
9, 8, 2.0, 8, 'ggactcta', 11, 10, 1.0, 10, 'agcgtgcata']], 'overlapAdjacency': \
[{'inherits': 'adjacency', 'sharedVariables': {}, 'variables': \
['node2', 'int', 'overlap', 'int']}, []], 'sharedVariables': \
{'Date': '24/11/2011', 'Created': "Assemblathon File Format Working Group \
using Richard Durbin's example"}, 'parents': [], 'include': ['ungappedOverlapGraph']}

More conveient functions to write (and read) directly to (and from) SQG files 
are also available.

To do the reverse, and load an sqg object from an SQG file representation is also simple.

>>> from pysqg.jsonSqg import makeJsonSqgFromSqg
>>> sqg2 = makeSqgFromJsonSqg(jsonSqg)
>>> print sqg2
<pysqg.sqg.Sqg instance at 0x1086bd7e8>

More Advanced Conversions
-------------------------

As mentioned, our aim is to provide simple conversion from sqg objects to a variety
of different databses, file formats and graph and numerical programming packages.

In the examples chapter you will examples using MongoDB, Numpy and NetworkX and
conversions to and from the FastG and VCF formats.


Hierarchy
-------------------------

