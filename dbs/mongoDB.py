"""Interface for writing into Sqg a MongoDB.
"""

import pymongo
from pysqg.jsonSqg import makeJsonSqgProperties, makeJsonArrayListProperties, makeSqgFromJsonSqg
from pysqg.arrayList import InMemoryArrayList, OnDiskArrayList

def mongoDBWrite(sqg, database):
    """Pushes an sqg into a database
    """
    #if database.count() != 0:
    #    raise RuntimeError("The database that we're writing the Sqg to is not empty")
    
    jsonSqg = makeJsonSqgProperties(sqg)
    database["sqg"].insert(jsonSqg)
    
    #Make the array list properties
    arrayListsCollection = database["arrayLists"]
    for arrayListType, arrayList in sqg.getArrayLists().items():
        properties = makeJsonArrayListProperties(arrayList)
        properties["type"] = arrayListType
        arrayListsCollection.insert(properties)
        
    #Now add the arrays
    for arrayListType, arrayList in sqg.getArrayLists().items():
        arrays = database[arrayListType]
        arrayNames = arrayList.getArrayNames()
        for array in arrayList:
            arrays.insert(dict(zip(arrayNames, array)))
    
def mongoDBRead(database, tempFileGenerator=None):
    """Parses an sqg from a database
    """
    #Get the core json sqg object
    jsonSqg = database.sqg.find_one()
    jsonSqg.pop("_id")
    
    #Now add the json array lists
    for arrayListProperties in database.arrayLists.find():
        arrayListProperties = arrayListProperties
        jsonArrayList = [ arrayListProperties, [] ]
        type = arrayListProperties["type"]
        arrayListProperties.pop("type")
        arrayListProperties.pop("_id")
        jsonSqg[type] = jsonArrayList
        if tempFileGenerator != None:
            jsonArrayList.append(tempFileGenerator())
    sqg = makeSqgFromJsonSqg(jsonSqg)
    
    #Now fill in the array lists
    for arrayListProperties in database.arrayLists.find():
        assert "type" in arrayListProperties
        type = arrayListProperties["type"]
        arrayList = sqg.getArrayList(type)
        assert arrayList != None
        for array in database.type.find():
            arrayList.addDict(array)
            
    return sqg