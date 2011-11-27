Examples using pysqg
====================

The pysqg/examples folder contains demos using pysqg.

Building the graph hierarchy diagram
++++++++++++++++++++++++++++++++++++

The demo examples/sqgHierarchy.py uses pysqg to build a graph representing
the hierarchy of ``ArrayList`` types and then uses the networkX interface to create
a graphViz (dot) file representing the graph.

Converting from FastG to VCF
++++++++++++++++++++++++++++++++++++

As a demo..

Building a de-Bruijn graph from a FastQ file
++++++++++++++++++++++++++++++++++++++++++++

Using pysqg a FastQ file is read and converted into a graph, dumped into mongoDB
and then processed with a simple map-reduce algorithm to produce a de-Bruijn graph.
The de-Bruijn graph that is extracted from Mongo and written out in SQG.
