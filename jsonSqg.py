"""Functions to read and write json-sqg representation to python sqg representation.
"""

import json
from pysqg.sqg import Sqg
from pysqg.arrayList import InMemoryArrayList, OnDiskArrayList

#################
#Generally useful functions
#################

def makeJsonSqgFromSqg(sqg):
    """Make json-sqg from sqg object
    """
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

def makeSqgFromJsonSqg(jsonSqg):
    """Make sqg object from json-sqg object
    """
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

def readJsonSqgFile(sqgFile):
    """Convenient function to convert json-sqg file into a sqg object
    """
    fileHandle = open(sqgFile, 'r')
    jsonSqg = json.load(fileHandle)
    sqg = makeSqgFromJsonSqg(jsonSqg)
    fileHandle.close()
    return sqg

def writeJsonSqgFile(sqg, sqgFile):
    """Convenient function to convert sqg file into a json-sqg file
    """
    fileHandle = open(sqgFile, 'w')
    jsonSqg = makeJsonSqgFromSqg(sqg)
    json.dump(jsonSqg, fileHandle)
    fileHandle.close()
    
#################
#Functions used by json-sqg manipulating functions
#################

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


