The Json Schema
===============

Describe json syntax / schema

Describe rules for inheritance

Describe rules for variables

Describe rules for types

Give basic example

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