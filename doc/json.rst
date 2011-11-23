The Json Schema
===============

Some text, *italic text*, **bold text**
 
* bulleted list.  There needs to be a space right after the "*"
* item 2
 
.. note::
    This is a note.
 
Here's some Python code:
 
>>> for i in range(10):
...     print i

Json files can be embedded::

{ 	
	"include":[], 
	"node": [ { "variables":[ "nodeName", "int" ] } ], 
	"edge": [ { "variables":[ "node1", "int", "node2", "int" ] } ], 	
	"subgraph":[ { "sharedVariables":{ "edges":[ "edge" ] },
                   "variables":[ "subgraphName", "int", "nodes", "array" ]
                   } 
                ]
}