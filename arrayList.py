"""The array list data structures
"""

import json

class AbstractArrayList:
    """Basic array list class
    """
    arrayListTypes = {} #This static set holds the set of array list types included, as abstract array lists.
    
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
        """The type of the array list.
        """
        return self.type
    
    def getInherits(self):
        """The array list type which this array list inherits from.
        """
        inherits = AbstractArrayList.arrayListTypes[self.getType()][-2]
        if inherits == None:
            return None
        return AbstractArrayList.arrayListTypes[inherits][-1]
    
    def getSharedVariables(self):
        """The shared attributes that array lists of this type all share. This is common to all array lists of this type.
        """
        return AbstractArrayList.arrayListTypes[self.getType()][0].copy()
    
    def getArrayNames(self):
        """The names of the variables in each array, listed according to position.
        """
        return AbstractArrayList.arrayListTypes[self.getType()][2][:]
    
    def getArrayTypes(self):
        """The types of the variables in each array, list according to position.
        """
        return AbstractArrayList.arrayListTypes[self.getType()][3][:]
    
    def getArrayWidth(self):
        """The number of variables in each array.
        """
        return self.arrayWidth
    
    def addArray(self, array):
        """Add an array to the array list.
        """
        raise RuntimeError("Calling an abstract method")
    
    def addDict(self, dict):
        """Add an array, organised as a dictionary { variableName1:value1, variableName2:value2 .. }
        """
        raise RuntimeError("Calling an abstract method")  
    
    def __iter__(self):
        """Used to iterate through the list of arrays, each being return as a list.
        """
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
            return str(variable)
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
        self.close()
        
    def addArray(self, array):
        InMemoryArrayList.addArray(self, array)
        if len(self._array) > self.bufferSize:
            self.flush()
    
    def flush(self):
        """Pushes all values in the array onto disk
        """
        for array in InMemoryArrayList._iter(self):
            json.dump(array, self.fileHandleWrite)
            self.fileHandleWrite.write("\n")
        self.fileHandleWrite.flush()
        self._array = []
    
    def close(self):
        """Flushes and closes the array list. Any subsequent adds will cause a failure.
        """
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
        
        def __del__(self):
            self.fileHandleRead.close()
    
    def __iter__(self):
        self.flush()
        return OnDiskArrayList._iter2(self)