"""An in memory representation of an SQG.
"""

class SQG:
    graphTypes = {}
    
    def __init__(self, name, includes=None, type=None, parents=None):
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
        
        #Set the type, and add it to the graph types
        if type == None:
            raise RuntimeError("Type of SQG is None")
        type = str(type)
        self.type = type
        if type not in self.graphTypes:
            graphType = parseInclude(self.includes[i]) #Check if there exists a full definition for this type in the library of includes
            if graphType == None:
                SQG.graphTypes[type] = self 
            assert SQG.graphTypes[type] != None
        
        #Set the parents
        self.parents = parents
        
        #Set an initially empty dictionary of array lists
        self.arrayLists = {}
        
    def getArrayLists(self):
        return self.arrayLists.copy()
                
    def getArrayList(self, arrayType):
        if arrayType in self.arrayLists:
            return self.arrayLists[arrayType]
    
    def setArrayList(self, arrayList):
        if arrayType.getType() in self.arrayLists:
            raise RuntimeError("Trying to set an array list of type %s for an SQG which already has such an array list type" % arrayList.type)
        self.arrayLists[arrayList.getType()] = arrayList

class ArrayListIter():
    def __init__(self, arrayList):
        self.arrayList = arrayList
        self.index = 0

    def next(self):
        if self.index >= self.arrayList.length()-1:
            raise StopIteration
        self.index += 1
        return self.arrayList[self.index]

class ArrayList:
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
        self.array = []
        self.variableLength = len(self.getVariables)
        
    def getType(self):
        return self.type
    
    def getAllowedTypes(self):
        return ArrayList[self.getType()][0]
    
    def getVariables(self):
        return ArrayList[self.getType()][1]
    
    def addArray(self, array):
        variables = self.getVariables()
        if len(array) != len(variables):
            raise RuntimeError("Got an unexpected number of variables for an array %i %i" % (len(array), len(variables)))
        for i in xrange(len(variables)):
            name, type  = variables[i]
            if array[i].__class__ != type:
                raise RuntimeError("Got an unexpected object type in an array %s %s", array[i].__class__, type)
        self.array.addAll(array)
    
    def length(self):
        assert len(self.array) % self.variableLength == 0
        return len(self.array)/self.variableLength
            
    def getArray(self, index):
        i = self.variableLength * index
        if index < 0 or i + self.variableLength > len(self.array):
            raise RuntimeError("Got an index out of bounds request %i %i" % (index, self.length()))
        return self.array[i:i:self.variableLength]
    
    def addDict(self, dict):
        variables = self.getVariables()
        array = []
        if len(variables) != len(dict):
            raise RuntimeError("Got an unexpected number of variables in a dictionary %i %i" % (len(dict), len(variables)))
        for i in xrange(variables):
            name, type = i
            array.append(dict[name])
        self.addArray(array)
    
    def getDict(self, index):
        variables = self.getVariables()
        array = self.getArray(index)
        dict = {}
        for i in xrange(variables):
            name, type = i
            dict[name] = array[i]
        return dict

    def __iter__(self):
        return ArrayListIter(self)
    