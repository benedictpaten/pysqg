"""An in memory representation of an SQG.
"""
import os.path
from pysqg.json import jsonRead
from unittest import isinstance

def getPysqgBaseDir():
    import pysqg.sqg
    return os.path.split(os.path.abspath(pysqg.sqg.__file__))[0]

def getPysqgIncludeDir():
    os.path.join(getPysqgBaseDir(), "include")

def parseInclude(include):
    fileHandle = open(getPysqgIncludeDir(), 'r') 
    sqg = jsonRead(fileHandle)
    fileHandle.close()
    return sqg

class SQG:
    parsedIncludes = set()
    
    def __init__(self, name, includes=None, parents=None, sharedVariables=None):
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
        if arrayType.getType() in self.arrayLists:
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
        if self.type not in ArrayList.arrayListTypes:
            if inherits != None:
                if inherits not in ArrayList.arrayListTypes:
                    raise RuntimeError("Trying to inherit from an array list type not yet seen: %s %s" % (inherits, type))
                else:
                    baseSharedVariables, baseVariables = ArrayList.arrayListTypes[inherits][:2]
                    if sharedVariables == None:
                        sharedVariables = baseSharedVariables
                    for key in baseSharedVariables.keys(): #This serves to allow the new variables to overwrite previous definitions
                        if key not in sharedVariables:
                            sharedVariables[key] = baseSharedVariables[key]
                    if variables == None:
                        variables = ()
                    variables = baseVariables + variables
            if sharedVariables == None:
                sharedVariables = {}
            if variables == None:
                raise RuntimeError("The array names for the type %s are unspecified" % type)
            if len(variables) == 0:
                raise RuntimeError("The array names for the type %s are of zero length" % type)
            arrayNames = [ name for name, type in variables ]
            arrayTypes = [ type for name, type in variables ]
            for name, type in variables:
                if not isinstance(name, "".__class__):
                    raise RuntimeError("The name of an array variable is not a string %s" % name)
                if type not in ("int", "float", "string", "object", "array"):
                    raise RuntimeError("The type of an array variable is not a string %s %s" % (name, type))
            ArrayList.arrayListTypes[type] = (sharedVariables, variables, arrayNames, arrayTypes)   
        else:
            if inherits != None:
                raise RuntimeError("The type of array list is already seen, but the inherits tag is being redefined")
            if allowedTypes != None:
                raise RuntimeError("The type of array list is already seen, but the allowed tag is being redefined")
            if variables != None:
                raise RuntimeError("The type of array list is already seen, but the array names tag is being redefined")
        self.arrayWidth = len(self.getArrayNames())
        
    def getType(self):
        return self.type
    
    def getSharedVariables(self):
        return ArrayList[self.getType()][0].copy()
    
    def getArrayNames(self):
        return ArrayList[self.getType()][2][:]
    
    def getArrayTypes(self):
        return ArrayList[self.getType()][3][:]
    
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
    def __init__(self, type, inherits=None, allowedTypes=None, variables=None):
        self.__init__(type, inherits, allowedTypes, variables)
        self._array = []
    
    def addArray(self, array):
        array = array[:]
        if len(array) != len(self.getArrayWidth()):
            raise RuntimeError("Got an unexpected number of variables for an array %i %i" % (len(array), len(self.getArrayWidth())))
        arrayTypes = self.getArrayTypes()
        def fn(variable, type): #Do some lame conversion of variables to respect types.
            #Not sure this is the right behaviour yet
            if type == "string":
                return string(variable)
            elif type == "int":
                return int(variable)
            elif type == "float":
                return float(variable)
        self._array.addAll([ fn(array[i], arrayTypes[i]) for i in xrange(len(array)) ])
        
    def addDict(self, dict):
        variables = self.getArrayNames()
        array = []
        if len(variables) != len(dict):
            raise RuntimeError("Got an unexpected number of variables in a dictionary %i %i" % (len(dict), len(variables)))
        for name in variables:
            array.append(dict[name])
        self.addArray(array)
        
    def _length(self):
        return self.array / self.getArrayWidth()
    
    class _iter():
        def __init__(self, arrayList):
            self.arrayList = arrayList
            self.index = 0
    
        def next(self):
            if self.index >= self.arrayList._length()-1:
                raise StopIteration
            self.index += 1
            i = self.index * self.arrayList.getArrayWidth()
            j = i + self.arrayList.getArrayWidth()
            return self.arrayList.array[i:j]
    
    def __iter__(self):    
        return _iter(self)
    
class StreamingArrayList(AbstractArrayList):
    """Streaming array list class
    """   
    def __init__(self, stream, type, inherits=None, allowedTypes=None, variables=None):
        self.__init__(type, inherits, allowedTypes, variables)
        self.stream = stream


    
    