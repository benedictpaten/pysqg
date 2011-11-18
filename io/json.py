"""Parser/writer for JSON formatted SQGs
"""

import json

def jsonWrite(sqg, fileHandle):
    for 
    pass

def jsonRead(fileHandle):
    i = json.load(fileHandle)
    parents = None
    if "parents" in i:
        parents = i["parents"]
        assert parents.__class__ == [].__class__
    sqg = SQG(name=i["name"],includes=i["include"], type=i["type"], parents=parents) 
    for key in i.keys():
        if key not in ("name", "include", "type", "parents"):
            value = i[key]
            assert value.__class__ == [].__class__
            properties = value[0]
            def fn(name):
                if name in properties:
                    return properties["name"]
                return None
            arrayList = ArrayList(key, inherits=fn("inherits"), allowedTypes=fn("allowedTypes"), variables=fn("variables"))
            sqg.setArrayList(arrayList)
            if len(value) == 2:
                arrays = value[1]
                variables = arrayList.getVariables()
                #Now parse in the different variables
                