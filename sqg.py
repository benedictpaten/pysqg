"""An in memory representation of an SQG.
"""
import os.path
import json
from sonLib.bioio import logger

def jsonWrite(sqg, fileHandle): 
    raise RuntimeError("Not implemented yet")

def jsonRead(fileHandle):
    jsonSQG = json.load(fileHandle)
    
    #Fn to parse out variables from top level json
    def fn(name, defaultObj):
        obj = defaultObj
        if name in jsonSQG:
            obj = jsonSQG[name]
            assert isinstance(obj, defaultObj.__class__)
        return obj
    
    name = None
    if "name" in jsonSQG:
        name = int(jsonSQG["name"])
    
    sqg = SQG(includes=fn("include", []), 
              name=name, 
              parents=fn("parents", []), 
              sharedVariables=fn("sharedVariables", {}))
    
    arrayListTypes = [ arrayListType for arrayListType in jsonSQG.keys() if arrayListType not in \
                      ("name", "include", "parents", "sharedVariables") ]
    while len(arrayListTypes) > 0:
        arrayListType = arrayListTypes.pop()
        jsonArrayList = jsonSQG[arrayListType]
        assert isinstance(jsonArrayList, [].__class__)
        properties = jsonArrayList[0]
        
        def fn(name):
            if name in properties:
                return properties[name]
            return None
        
        inherits = fn("inherits")
        if inherits != None and inherits in arrayListTypes:
            arrayListTypes = [ arrayListType ] + arrayListTypes
            continue
        
        arrayList = InMemoryArrayList(arrayListType, 
                                      inherits=inherits, 
                                      sharedVariables=fn("sharedVariables"), 
                                      variables=fn("variables"))
        
        sqg.setArrayList(arrayList)
        if len(jsonArrayList) == 2:
            arrays = jsonArrayList[1]
            arrayWidth = arrayList.getArrayWidth()
            #Now parse in the different arrays
            assert len(arrays) % arrayWidth == 0 #Otherwise the length of the array is not divisible by the length of each entry
            for j in xrange(0,len(arrays),arrayWidth):
                arrayList.addArray(arrays[j:j+arrayWidth])
    
    return sqg

def getPysqgBaseDir():
    import pysqg.sqg
    return os.path.split(os.path.abspath(pysqg.sqg.__file__))[0]

def getPysqgIncludeDir():
    return os.path.join(getPysqgBaseDir(), "include")

def parseInclude(include):
    includeFile = os.path.join(getPysqgIncludeDir(), include + ".json")
    logger.debug("Going to parse the include file: %s", includeFile)
    fileHandle = open(includeFile, 'r') 
    sqg = jsonRead(fileHandle)
    fileHandle.close()
    return sqg

class SQG:
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
            if include not in SQG.parsedIncludes:
                graphType = parseInclude(include)
                if graphType == None:
                    raise RuntimeError("Could not find the following include: %s" % self.includes[i])
                SQG.parsedIncludes.add(include)
        
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
        return self.includes[:]
    
    def getName(self):
        return self.name
    
    def getParents(self):
        return self.parents[:]
    
    def getSharedVariables(self):
        return self.sharedVariables.copy()
        
    def getArrayLists(self):
        return self.arrayLists.copy()
                
    def getArrayList(self, arrayType):
        if arrayType in self.arrayLists:
            return self.arrayLists[arrayType]
    
    def setArrayList(self, arrayList):
        if arrayList.getType() in self.arrayLists:
            raise RuntimeError("Trying to set an array list of type %s for an SQG which already has such an array list type" % arrayList.type)
        self.arrayLists[arrayList.getType()] = arrayList

class AbstractArrayList:
    """Basic array list class
    """
    arrayListTypes = {}
    
    def __init__(self, type, inherits=None, sharedVariables=None, variables=None):
        if type == None:
            raise RuntimeError("Type of arrayList is None")
        type = str(type)
        self.type = type
        if self.type not in AbstractArrayList.arrayListTypes:
            if inherits != None:
                if inherits not in AbstractArrayList.arrayListTypes:
                    raise RuntimeError("Trying to inherit from an array list type not yet seen: %s %s" % (inherits, type))
                else:
                    baseSharedVariables, baseVariables = AbstractArrayList.arrayListTypes[inherits][:2]
                    if sharedVariables == None:
                        sharedVariables = baseSharedVariables
                    for key in baseSharedVariables.keys(): #This serves to allow the new variables to overwrite previous definitions
                        if key not in sharedVariables:
                            sharedVariables[key] = baseSharedVariables[key]
                    if variables == None:
                        variables = ()
                    variables = baseVariables + tuple(variables)
            if sharedVariables == None:
                sharedVariables = {}
            if variables == None:
                raise RuntimeError("The variables for the type %s are unspecified" % type)
            if len(variables) == 0:
                raise RuntimeError("The variables for the type %s are of zero length" % type)
            arrayNames = [ str(name) for name in variables[::2] ]
            arrayTypes = [ str(variableType) for variableType in variables[1::2] ]
            for name, variableType in zip(arrayNames, arrayTypes):
                if not isinstance(name, "".__class__):
                    raise RuntimeError("The name of an array variable is not a string %s %s" % (name, name.__class__))
                if variableType not in ("int", "float", "string", "object", "array"):
                    raise RuntimeError("The type of an array variable is not a string %s %s" % (name, variableType))
            AbstractArrayList.arrayListTypes[self.type] = (sharedVariables, tuple(variables), tuple(arrayNames), tuple(arrayTypes))   
        else:
            pass
            #if inherits != None:
            #    raise RuntimeError("The type of array list is already seen, but the inherits tag is being redefined")
            #if sharedVariables != None:
            #    raise RuntimeError("The type of array list is already seen, but the shared variables tag is being redefined")
            #if variables != None:
            #    raise RuntimeError("The type of array list is already seen, but the array variables tag is being redefined")
        self.arrayWidth = len(self.getArrayNames())
        
    def getType(self):
        return self.type
    
    def getSharedVariables(self):
        return AbstractArrayList.arrayListTypes[self.getType()][0].copy()
    
    def getArrayNames(self):
        return AbstractArrayList.arrayListTypes[self.getType()][2][:]
    
    def getArrayTypes(self):
        return AbstractArrayList.arrayListTypes[self.getType()][3][:]
    
    def getArrayWidth(self):
        return self.arrayWidth
    
    def addArray(self, array):
        raise RuntimeError("Calling an abstract method")
    
    def addDict(self, dict):
        raise RuntimeError("Calling an abstract method")
    
    def __iter__(self):
        raise RuntimeError("Calling an abstract method")
        
class InMemoryArrayList(AbstractArrayList):
    """In memory array list class
    """    
    def __init__(self, type, inherits=None, sharedVariables=None, variables=None):
        AbstractArrayList.__init__(self, type, inherits, sharedVariables, variables)
        self._array = []
    
    def addArray(self, array):
        array = array[:]
        if len(array) != self.getArrayWidth():
            raise RuntimeError("Got an unexpected number of variables for an array %i %i" % (len(array), self.getArrayWidth()))
        arrayTypes = self.getArrayTypes()
        def fn(variable, type): #Do some lame conversion of variables to respect types.
            #Not sure this is the right behaviour yet
            if type == "string":
                return string(variable)
            elif type == "int":
                return int(variable)
            elif type == "float":
                return float(variable)
        for i in xrange(len(array)):
            self._array.append(fn(array[i], arrayTypes[i]))
        
    def addDict(self, dict):
        variables = self.getArrayNames()
        array = []
        if len(variables) != len(dict):
            raise RuntimeError("Got an unexpected number of variables in a dictionary %i %i" % (len(dict), len(variables)))
        for name in variables:
            array.append(dict[name])
        self.addArray(array)
        
    def _length(self):
        return len(self._array) / self.getArrayWidth()
    
    class _iter():
        def __init__(self, arrayList):
            self.arrayList = arrayList
            self.index = 0
    
        def next(self):
            if self.index > self.arrayList._length()-1:
                raise StopIteration
            i = self.index * self.arrayList.getArrayWidth()
            j = i + self.arrayList.getArrayWidth()
            self.index += 1
            return self.arrayList._array[i:j]
    
    def __iter__(self):    
        return InMemoryArrayList._iter(self)
    
class StreamingArrayList(AbstractArrayList):
    """Streaming array list class
    """   
    def __init__(self, stream, type, inherits=None, sharedVariables=None, variables=None):
        AbstractArrayList.__init__(self, type, inherits, sharedVariables, variables)
        self.stream = stream


    
    