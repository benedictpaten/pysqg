"""Interface for writing into SQG a MongoDB.
"""

import pymongo

def mongoDBWrite(sqg, database):
    """Pushes an sqg into a database
    """
    jsonSQG = jsonSQGProperties(sqg)
    database["sqg"].insert(jsonSQG)
    
    #Make the array list properties
    arrayListsCollection = database["arrayLists"]
    for arrayListType, arrayList in sqg.getArrayLists().items():
        properties = jsonArrayListProperties(arrayList)
        properties["type"] = arrayListType
        arrayListsCollection.insert(properties)
        
    #Now add the arrays
    for arrayListType, arrayList in sqg.getArrayLists().items():
        arrays = database[arrayListType]
        arrayNames = arrayList.getArrayNames()
        for array in arrayList:
            arrays.insert(dict(zip(arrayNames, array)))
    
def mongoDBRead(database):
    """Parses an sqg from a database
    """
    pass