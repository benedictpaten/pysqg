"""Core sqg data structure
"""

import os.path
from pysqg.shared import getPysqgIncludeDir
from pysqg.bioio import logger

def parseInclude(include):
    includeFile = os.path.join(getPysqgIncludeDir(), include + ".json")
    logger.debug("Going to parse the include file: %s", includeFile)
    from pysqg.jsonSqg import readJsonSqgFile
    return readJsonSqgFile(includeFile)

class Sqg:
    """The sqg datastructure
    """
    parsedIncludes = set()
    
    def __init__(self, includes, name=None, parents=None, sharedVariables=None):
        #Set the name
        self.name = None
        if name != None:
            self.name = int(name)
        
        #Parse the includes
        if includes == None:
            self.includes = []
        else:
            self.includes = includes
        for include in self.includes:
            if include not in Sqg.parsedIncludes:
                graphType = parseInclude(include)
                if graphType == None:
                    raise RuntimeError("Could not find the following include: %s" % self.includes[i])
                Sqg.parsedIncludes.add(include)
        
        #Set the parents
        if parents == None:
            parents = []
        self.parents = parents
        
        #Set the shared variables
        if sharedVariables == None:
            sharedVariables = {}
        self.sharedVariables = sharedVariables
        
        #Set an initially empty dictionary of array lists
        self.arrayLists = {}
        
    def getIncludes(self):
        """The list of array lists to include from the include hierarchy
        """
        return self.includes[:]
    
    def getName(self):
        """The name of the sqg as an int, this is optional and may be null.
        """
        return self.name
    
    def getParents(self):
        """The list of parent sqg files, used in defining a decomposition of sqg graphs
        """
        return self.parents[:]
    
    def getSharedVariables(self):
        """Common variables for the graph. These are not shared and may be made specific to the given graph instance.
        """
        return self.sharedVariables.copy()
        
    def getArrayLists(self):
        """The set of array lists, as a dictionary of the form { "type1":arrayList1, "type2":arrayList2 ... },
        where type is the string describing the type of the array list.
        """
        return self.arrayLists.copy()
                
    def getArrayList(self, arrayType):
        """Gets an array list of a specific type, specified as a string, if it exists in the SQG, else return None.
        """
        if arrayType in self.arrayLists:
            return self.arrayLists[arrayType]
    
    def setArrayList(self, arrayList):
        """Sets the array list type of a given type. Only one arrayList of a given type may be included in an SQG.
        """
        if arrayList.getType() in self.arrayLists:
            raise RuntimeError("Trying to set an array list of type %s for an Sqg which already has such an array list type" % arrayList.type)
        self.arrayLists[arrayList.getType()] = arrayList

    
    