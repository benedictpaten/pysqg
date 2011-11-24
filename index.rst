.. pysqg documentation master file, created by
   sphinx-quickstart on Wed Nov 23 14:58:08 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pysqg's documentation!
=================================

Pysqg is a package implementing tools for the prototype 
SeQuence Graph (SQG) file format. Described within this documentation
is the file format, based upon the JSON format
(http://www.json.org/), and the set of tools that we have implemented to interface with it.

Sqg is designed to represent hierarchically **many** graphs commonly used to represent DNA molecules. 
As such we would like it to act as a superset format, enabling us to create a veritable Rosetta Stone through which existing formats
might be converted. 

The Sqg format and pysqg package have been designed to be: 
	
	* Lightweight:
		- It is easy to completely understand the basic semantics and syntax of Sqg in just a few minutes.
		
		- It is easy to learn and use the associated tools with only a prefunctory knowledge of Python.
		
		- The basic Pysqg tools have no dependencies, so it is easy to install.
	
	* Extensible:
		- Sqg has a small syntax but uses the notion of inheritence, as used in object oriented programming languages, to allow a hierarchy of types to be defined.
		
		- The initial hierarchy is powerful and non-redundant, expressing several important classes of graph, but it is incomplete. We envision it being added to progressively by community input.
	
	* Portable:
		- Sqg is based upon JSON. JSON parsers/writers are already available in many, many languages.
		
		- Pysqg has been implemented purely in Python, but a C/C++ implementation may shortly arise.
		
		- Pysqg already provides easy converters to several important projects, such as:
			+ Numpy, the numerical computing package for Python.
			+ NetworkX, the most popular in memory graph library for Python.
			+ MongoDB, the popular JSON document based database that allows for massive and efficient complex queries using a map/reduce framework.
		
	* Scaleable:
		- Sqg allows the breaking up of large graphs hierarchically.
		- Pysqg supports in memory and **on disk** manipulation of edges and nodes.

The remainder of this documentation is divided into several short chapters. 

	* Firstly, a quick start tutorial that in 5 minutes should provide you with a working knowledge (and installation!) of Pysqg, without ever having to learn the syntax of the underlying SQG file format.
	* Secondly, a description of the SQG format.
	* Thirdly, a description of the graph hierarchy, with explanations of each graph's uses.
	* Fourthly, a full guide to installing Pysqg.
	* Fiftly, a series of examples demonstrating Pysqg.
	* Sixth, documentation on the Python modules in the Pysqg package.
	
Contents:

.. toctree::

   doc/tutorial.rst
   doc/json.rst
   doc/hierarchy.rst
   doc/installation.rst
   doc/examples.rst
   doc/modules.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

