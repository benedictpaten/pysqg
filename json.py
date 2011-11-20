"""Parser/writer for JSON formatted SQGs
"""

import json
from unittest import isinstance

def jsonWrite(sqg, fileHandle): 
    raise RuntimeError("Not implemented yet")

def jsonRead(fileHandle):
    jsonSQG = json.load(fileHandle)
    
    #Fn to parse out variables from top level json
    def fn(name, classObj):
        obj = None
        if name in jsonSQG:
            obj = jsonSQG[name]
            assert isinstance(obj, classObj)
        return obj
    
    sqg = SQG(name=i["name"], includes=fn("include", [].__class__), 
              parents=fn("parents", [].__class__), 
              sharedVariables=fn("sharedVariables", {}.__class__))
    
    for arrayListType in jsonSQG.keys():
        if arrayListType not in ("name", "include", "parents", "sharedVariables"):
            
            jsonArrayList = jsonSQG[arrayListType]
            assert isinstance(jsonArrayList, [].__class__)
            properties = jsonArrayList[0]
            
            def fn(name):
                if name in properties:
                    return properties[name]
                return None
            
            arrayList = InMemoryArrayList(arrayListType, 
                                          inherits=fn("inherits"), 
                                          arrayNames=fn("arrayNames"),
                                          sharedVariables=fn("sharedVariables"))
            
            sqg.setArrayList(arrayList)
            if len(jsonArrayList) == 2:
                arrays = jsonArrayList[1]
                arrayWidth = arrayList.getArrayWidth()
                #Now parse in the different arrays
                assert len(arrays) % arrayWidth == 0 #Otherwise the length of the array is not divisible by the length of each entry
                for j in xrange(0,len(arrays),arrayWidth):
                    arrayList.addArray(arrays[j:j+arrayWidth])
                         