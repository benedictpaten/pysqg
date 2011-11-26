The SQG File Format
===================

The basic JSON (http://www.json.org/) based syntax can be described recursively. 
We break this in to two parts, firstly describing the
the SQG containing object, then describing the contained array lists.

SQG Syntax
----------

The SQG file format can be described recursively as follows:


**SQG**
	*{ "include":stringList, name parents sharedVariables arrayLists }*

**name**
	*, "name":int*

**stringList**
	*[ strings ]*
	*[]*

**strings**
	*string, strings*
	*string*

**parents**
	*, "parents":stringList*
	*empty*

**empty**


**sharedVariables**
	*, "sharedVariables":object*
	*empty*
	
TODO: 

Describe rules for include
Describe sharedVariables and names
	
Array List Syntax
-----------------

An SQG may contain a series of Array Lists, each of which describes a set of graph primitives,
such as edges, nodes or subgraphs.

**arrayLists**
	*, arrayType:arrayList arrayLists*
	*empty*

**arrayType**
	*string*

**arrayList**
	*[ properties, null, string ]*
	*[ properties, array ]*
	*[ properties ]*

**properties**
	*{ "inherits":type variablesDict sharedVariables }*
	*{ "variables":[ variables ] sharedVariables }*
	
**variablesDict**
	*, "variables":[ variables ]*
	*empty*

**variables**
	*variableName, type*
	*variableName, type, variables*

**variableName**
	*string*

**type**
	*"string"*
	*"int"*
	*"float"*
	*"bool"*
	*"array"*
	*"object"*

TODO: 

Describe rules for inheritance
Describe rules for variables 
Describe rules for types
Describe rules for subgraphs
