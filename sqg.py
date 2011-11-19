"""An in memory representation of an SQG.
"""

def parseInclude(include):
    pass

class SQG:
    graphTypes = {}
    
    def __init__(self, name, includes=None, parents=None):
        self.name = int(name)
        
        #Parse the includes
        if includes == None:
            self.includes = []
        else:
            self.includes = includes
        for i in xrange(len(self.includes)):
            if self.includes[i] not in SQG.graphTypes:
                graphType = parseInclude(self.includes[i])
                if graphType == None:
                    raise RuntimeError("Could not find the following include: %s" % self.includes[i])
                self.includes[i] = graphType
            else:
                self.includes[i] = SQG.graphTypes[self.includes[i]]
        
        #Set the parents
        if parents == None:
            parents = []
        self.parents = parents
        
        #Set an initially empty dictionary of array lists
        self.arrayLists = {}
        
    def getIncludes(self):
        return self.includes[:]
    
    def getParents(self):
        return self.parents[:]
        
    def getArrayLists(self):
        return self.arrayLists.copy()
                
    def getArrayList(self, arrayType):
        if arrayType in self.arrayLists:
            return self.arrayLists[arrayType]
    
    def setArrayList(self, arrayList):
        if arrayType.getType() in self.arrayLists:
            raise RuntimeError("Trying to set an array list of type %s for an SQG which already has such an array list type" % arrayList.type)
        self.arrayLists[arrayList.getType()] = arrayList

class AbstractArrayList:
    """Basic array list class
    """
    arrayListTypes = {}
    
    def __init__(self, type, inherits=None, allowedTypes=None, variables=None):
        if type == None:
            raise RuntimeError("Type of arrayList is None")
        type = str(type)
        self.type = type
        if self.type not in ArrayList.arrayListTypes:
            if inherits != None:
                if inherits not in ArrayList.arrayListTypes:
                    raise RuntimeError("Trying to inherit from an array list type not yet seen: %s %s" % (inherits, type))
                else:
                    baseAllowedTypes, baseVariables = ArrayList.arrayListTypes[inherits]
                    if allowedTypes == None:
                        allowedTypes = baseAllowedTypes
                    if variables == None:
                        variables = ()
                    variables = baseVariables + variables
            if allowedTypes == None:
                allowedTypes = ()
            if variables == None:
                raise RuntimeError("The variables for the type %s are unspecified" % type)
            if len(variables) == 0:
                raise RuntimeError("The variables for the type %s are of zero length" % type)
            ArrayList.arrayListTypes[type] = (allowedTypes, variables)   
        else:
            if inherits != None:
                raise RuntimeError("The type of array list is already seen, but the inherits tag is being redefined")
            if allowedTypes != None:
                raise RuntimeError("The type of array list is already seen, but the allowed tag is being redefined")
            if variables != None:
                raise RuntimeError("The type of array list is already seen, but the variables tag is being redefined")
        self.variableLength = len(self.getVariables)
        
    def getType(self):
        return self.type
    
    def getAllowedTypes(self):
        return ArrayList[self.getType()][0]
    
    def getVariables(self):
        return ArrayList[self.getType()][1]
    
    def getArrayLength(self):
        return self.variableLength
    
    def addArray(self, array):
        raise RuntimeError("Calling an abstract method")
    
    def addDict(self, dict):
        raise RuntimeError("Calling an abstract method")
    
    def __iter__(self):
        raise RuntimeError("Calling an abstract method")
        
class InMemoryArrayList(AbstractArrayList):
    """In memory array list class
    """    
    def __init__(self, type, inherits=None, allowedTypes=None, variables=None):
        self.__init__(type, inherits, allowedTypes, variables)
        self._array = []
    
    def addArray(self, array):
        variables = self.getVariables()
        if len(array) != len(variables):
            raise RuntimeError("Got an unexpected number of variables for an array %i %i" % (len(array), len(variables)))
        self._array.addAll(array)
        
    def addDict(self, dict):
        variables = self.getVariables()
        array = []
        if len(variables) != len(dict):
            raise RuntimeError("Got an unexpected number of variables in a dictionary %i %i" % (len(dict), len(variables)))
        for name in variables:
            array.append(dict[name])
        self.addArray(array)
        
    def _length(self):
        return self.array / self.getArrayLength()
    
    class _iter():
        def __init__(self, arrayList):
            self.arrayList = arrayList
            self.index = 0
    
        def next(self):
            if self.index >= self.arrayList._length()-1:
                raise StopIteration
            self.index += 1
            i = self.index * self.arrayList.getArrayLength()
            j = i + self.arrayList.getArrayLength()
            return self.arrayList.array[i:j]
    
    def __iter__(self):    
        return _iter(self)
    
class StreamingArrayList(AbstractArrayList):
    """Streaming array list class
    """   
    def __init__(self, stream, type, inherits=None, allowedTypes=None, variables=None):
        self.__init__(type, inherits, allowedTypes, variables)
        self.stream = stream


    
    