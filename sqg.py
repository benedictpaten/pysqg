"""Core functions working with Sqgs
"""
import os.path
import json
from sonLib.bioio import logger

def makeJsonSqgProperties(sqg):
    """Build the sqg object sans array lists
    """
    jsonSqg = { "include":sqg.getIncludes(), 
               "parents":sqg.getParents(), "sharedVariables":sqg.getSharedVariables(),
                }
    if sqg.getName() != None:
        jsonSqg["name"] = sqg.getName()
    return jsonSqg

def makeJsonArrayListProperties(arrayList):
    """Build the json properties object for an array list.
    """
    jsonProperties = {}
    sharedVariables = arrayList.getSharedVariables()
    variables = zip(arrayList.getArrayNames(), arrayList.getArrayTypes())
    if arrayList.getInherits() != None:
        parentArrayList = arrayList.getInherits()
        jsonProperties["inherits"] = arrayList.getInherits().getType()
        variables = variables[-parentArrayList.getArrayWidth():]
        for key, value in parentArrayList.getSharedVariables().items():
            if key in sharedVariables and sharedVariables[key] == value:
                sharedVariables.pop(key)
    jsonProperties["sharedVariables"] = arrayList.getSharedVariables()
    flatVariables = []
    for i, j in variables:
        flatVariables.append(i)
        flatVariables.append(j)
    jsonProperties["variables"] = flatVariables
    return jsonProperties

def makeJsonSqgFromSqg(sqg):
    jsonSqg = makeJsonSqgProperties(sqg)
    
    #Add the arraylists in a hacky way, currently
    for arrayListType, arrayList in sqg.getArrayLists().items():
        jsonSqg[arrayListType] = [ makeJsonArrayListProperties(arrayList) ]
        if isinstance(arrayList, InMemoryArrayList):
            jsonSqg[arrayListType].append(arrayList._array)
        else:
            jsonSqg[arrayListType].append(None)
            jsonSqg[arrayListType].append(arrayList.file)
    
    return jsonSqg

def readJsonSqgFile(sqgFile):
    fileHandle = open(sqgFile, 'r')
    jsonSqg = json.load(fileHandle)
    sqg = makeSqgFromJsonSqg(jsonSqg)
    fileHandle.close()
    return sqg

def writeJsonSqgFile(sqg, sqgFile):
    fileHandle = open(sqgFile, 'w')
    jsonSqg = makeJsonSqgFromSqg(sqg)
    json.dump(jsonSqg, fileHandle)
    fileHandle.close()

def makeSqgFromJsonSqg(jsonSqg):
    #Fn to parse out variables from top level json
    def fn(name, defaultObj):
        obj = defaultObj
        if name in jsonSqg:
            obj = jsonSqg[name]
            assert isinstance(obj, defaultObj.__class__)
        return obj
    
    name = None
    if "name" in jsonSqg:
        name = int(jsonSqg["name"])
    
    sqg = Sqg(includes=fn("include", []), 
              name=name, 
              parents=fn("parents", []), 
              sharedVariables=fn("sharedVariables", {}))
    
    arrayListTypes = [ arrayListType for arrayListType in jsonSqg.keys() if arrayListType not in \
                      ("name", "include", "parents", "sharedVariables") ]
    while len(arrayListTypes) > 0:
        arrayListType = arrayListTypes.pop()
        jsonArrayList = jsonSqg[arrayListType]
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
        
        if len(jsonArrayList) not in (1, 2, 3):
            raise RuntimeError("Got an incorrect number of arguments for a json array list: %s %i" % (jsonArrayList, len(jsonArrayList)))
        
        if len(jsonArrayList) in (1, 2): #In memory
            arrayList = InMemoryArrayList(type=arrayListType, 
                                          inherits=inherits, 
                                          sharedVariables=fn("sharedVariables"), 
                                          variables=fn("variables"))
            if len(jsonArrayList) == 2:
                arrays = jsonArrayList[1]
                arrayWidth = arrayList.getArrayWidth()
                #Now parse in the different arrays
                assert len(arrays) % arrayWidth == 0 #Otherwise the length of the array is not divisible by the length of each entry
                for j in xrange(0,len(arrays),arrayWidth):
                    arrayList.addArray(arrays[j:j+arrayWidth])
        else: #On disk
            arrayList = OnDiskArrayList(file=jsonArrayList[2],
                                        type=arrayListType, 
                                        inherits=inherits, 
                                        sharedVariables=fn("sharedVariables"), 
                                        variables=fn("variables"))
        
        sqg.setArrayList(arrayList)
    return sqg

def getPysqgBaseDir():
    import pysqg.sqg
    return os.path.split(os.path.abspath(pysqg.sqg.__file__))[0]

def getPysqgIncludeDir():
    return os.path.join(getPysqgBaseDir(), "include")

def parseInclude(include):
    includeFile = os.path.join(getPysqgIncludeDir(), include + ".json")
    logger.debug("Going to parse the include file: %s", includeFile)
    return readJsonSqgFile(includeFile)

class Sqg:
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
            raise RuntimeError("Trying to set an array list of type %s for an Sqg which already has such an array list type" % arrayList.type)
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
                    else:
                        for key in baseSharedVariables.keys(): #This serves to allow the new variables to overwrite previous definitions
                            if key not in sharedVariables:
                                sharedVariables[key] = baseSharedVariables[key]
                    if variables == None:
                        variables = baseVariables
                    else:
                        variables = baseVariables + tuple(variables)
            else: #Case that it doesn't inherit, the variables must exist
                if variables == None:
                    raise RuntimeError("The variables for the type %s are unspecified" % type)
                if len(variables) == 0:
                    raise RuntimeError("The variables for the type %s are of zero length" % type)
                if len(variables) % 2 != 0:
                    raise RuntimeError("The variables and their types are not paired for the type" % type)
                variables = tuple(variables)
            
            assert len(variables) > 0
            assert len(variables) % 2 == 0
            
            arrayNames = tuple([ str(name) for name in variables[::2] ])
            arrayTypes = tuple([ str(variableType) for variableType in variables[1::2] ])
            for name, variableType in zip(arrayNames, arrayTypes):
                if not isinstance(name, "".__class__):
                    raise RuntimeError("The name of an array variable is not a string %s %s" % (name, name.__class__))
                if variableType not in ("int", "float", "string", "object", "array"):
                    raise RuntimeError("The type of an array variable is not a string %s %s" % (name, variableType))
                        
            if sharedVariables == None:
                sharedVariables = {}
            
            AbstractArrayList.arrayListTypes[self.type] = (sharedVariables, variables, arrayNames, arrayTypes, inherits, self)
            #Replace reference with abstract version of class, so that getInherits retrieves abstract version of class
            AbstractArrayList.arrayListTypes[self.type] = (sharedVariables, variables, arrayNames, arrayTypes, inherits, AbstractArrayList(type, inherits=inherits, sharedVariables=sharedVariables, variables=variables))
        else:
            #Check the definition of the array is not being altered
            existingSharedVariables, existingVariables = AbstractArrayList.arrayListTypes[self.type][:2]
            if sharedVariables != None and existingSharedVariables != sharedVariables:
                raise RuntimeError("The type of array list is already seen and the shared variables definition is being altered: %s %s" % (existingSharedVariables, sharedVariables))
            if variables != None and existingVariables[-len(variables):] != tuple(variables):
                raise RuntimeError("The type of array list is already seen and the list of variables/types being redefined: %s %s" % (existingVariables, variables))
        
        self.arrayWidth = len(self.getArrayNames())
        
    def getType(self):
        return self.type
    
    def getInherits(self):
        inherits = AbstractArrayList.arrayListTypes[self.getType()][-2]
        if inherits == None:
            return None
        return AbstractArrayList.arrayListTypes[inherits][-1]
    
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
        
    def _typeVariable(self, variable, type):
        #Not sure this is the right behaviour yet
        if type == "string":
            return string(variable)
        elif type == "int":
            return int(variable)
        elif type == "float":
            return float(variable)
        elif type == "array":
            if not isinstance(variable, [].__class__):
                raise RuntimeError("Trying to add a variable which should be of type array %s" % variable)
        elif type == "object":
            if not isinstance(variable, {}.__class__):
                raise RuntimeError("Trying to add a variable which should be of type object %s" % variable)
        else:
            raise RuntimeError("Unrecognised type: %s" % variable)
        return variable
    
    def addArray(self, array):
        array = array[:]
        if len(array) != self.getArrayWidth():
            raise RuntimeError("Got an unexpected number of variables for an array %i %i" % (len(array), self.getArrayWidth()))
        arrayTypes = self.getArrayTypes()
        for i in xrange(len(array)):
            self._array.append(self._typeVariable(array[i], arrayTypes[i]))
        
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
            return self
    
    def __iter__(self):
        return InMemoryArrayList._iter(self)
    
class OnDiskArrayList(InMemoryArrayList):
    """Array list class which writes to disk.
    """   
    def __init__(self, file, type, inherits=None, sharedVariables=None, variables=None, bufferSize=100000):
        InMemoryArrayList.__init__(self, type, inherits, sharedVariables, variables)
        self.file = file
        self.fileHandleWrite = open(file, "a")
        self.bufferSize = bufferSize
        
    def __del__(self):
        self.fileHandleWrite.close()
        
    def addArray(self, array):
        InMemoryArrayList.addArray(self, array)
        if len(self._array) > self.bufferSize:
            self.flush()
    
    def flush(self):
        for array in InMemoryArrayList._iter(self):
            json.dump(array, self.fileHandleWrite)
            self.fileHandleWrite.write("\n")
        self.fileHandleWrite.flush()
        self._array = []
        from sonLib.bioio import system
    
    def close(self):
        self.flush()
        self.fileHandleWrite.close()
    
    class _iter2():
        def __init__(self, arrayList):
            self.arrayList = arrayList
            self.fileHandleRead = open(arrayList.file, 'r')
    
        def next(self):
            line = self.fileHandleRead.readline()
            if line == '':
                self.fileHandleRead.close()
                raise StopIteration
            arrayTypes = self.arrayList.getArrayTypes()
            array = json.loads(line)
            if len(arrayTypes) != len(array):
                raise RuntimeError("Got an unexepected number of variables in an array")
            return [ self.arrayList._typeVariable(array[i], arrayTypes[i]) for i in xrange(len(array)) ]
    
    def __iter__(self):
        self.flush()
        return OnDiskArrayList._iter2(self)
    
    