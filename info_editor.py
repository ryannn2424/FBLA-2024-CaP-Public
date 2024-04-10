import json
import file_management
import filter_management
import logger

isTemp = not file_management.check_if_empty('.temp/temp.json')
jsonDict = {}
tempDict = {}
FilteredDict = {}
loggerObj = logger.Logger()

def jsonToDict(json_file) -> dict:
    loggerObj.addToLog("info_editor.py - jsonToDict - " + json_file)
    global jsonDict
    with open(json_file) as f:
        json_dictionary = json.load(f)
        jsonDict = json_dictionary
    return json_dictionary

def sendToTemp(json_dict) -> None:
    loggerObj.addToLog("info_editor.py - Sending JSON to Temp")
    global isTemp
    json_object = json.dumps(json_dict, indent=4)
    with open('.temp/temp.json', 'w') as f:
        f.write(json_object)
    isTemp = True
    updateTempDict()
    
def updateTempDict(temp_json_file='.temp/temp.json') -> None:
    loggerObj.addToLog("info_editor.py - updating tempDict")
    global tempDict
    with open(temp_json_file) as f:
        tempDict = json.load(f)
    return tempDict
        
def writeToTemp(tempDict=tempDict) -> None:
    loggerObj.addToLog("info_editor.py - Writing to Temp")
    json_object = json.dumps(tempDict, indent=4)
    with open('.temp/temp.json', 'w') as f:
        f.write(json_object)
        
def deleteCellData(cellRefrence=object) -> None:
    loggerObj.addToLog("info_editor.py - ensuring proper cell deletion")
    global jsonDict, tempDict
    isTemp = not file_management.check_if_empty('.temp/temp.json')
    if not isTemp:
        sendToTemp(jsonDict)
        
    keys = cellRefrence.jsonlocation
    # print(keys)
    nested_data_point = tempDict

    for key in keys[:-1]:
        nested_data_point = nested_data_point.get(key)
        if nested_data_point is None:
            break
        
    if nested_data_point is not None and keys[-1] in nested_data_point:
        del nested_data_point[keys[-1]]
        
    # print(tempDict)

    writeToTemp(tempDict)

    print("Deleted Cell!")
    
def updateCellData(cellReference=object, newKey="yuh", newValue="guh") -> None:
    loggerObj.addToLog("info_editor.py - updating cell data")
    global jsonDict, tempDict
    isTemp = not file_management.check_if_empty('.temp/temp.json')
    if not isTemp:
        sendToTemp(jsonDict)
        
    keys = cellReference.jsonlocation
    nested_data_point = tempDict

    for key in keys[:-1]:
        nested_data_point = nested_data_point.get(key)
        if nested_data_point is None:
            break
    
    if nested_data_point is not None and keys[-1] in nested_data_point:
        nested_data_point[newKey] = newValue
        del nested_data_point[keys[-1]]

    writeToTemp(tempDict)

    print("Updated Cell Data!")
    
    
def newContentInfo(cellRefrence=object, newKey=str, newValue=str) -> None:
    loggerObj.addToLog("info_editor.py - adding new contentInfo to temp")
    global jsonDict, tempDict
    isTemp = not file_management.check_if_empty('.temp/temp.json')
    if not isTemp:
        sendToTemp(jsonDict)
        
    keys = cellRefrence.jsonlocation
    keys.pop()
    # print(keys)
    
    nested_data_point = tempDict

    # print(nested_data_point)
    for key in keys:
        nested_data_point = nested_data_point[key]
        
    nested_data_point[newKey] = newValue
    # print(tempDict)

    writeToTemp(tempDict)

    print("New Content!")

def NewCollapsableInfo(cellRefrence=object, newKey=str) -> None:
    loggerObj.addToLog("info_editor.py - adding new collapseableInfo to temp")
    global jsonDict, tempDict
    isTemp = not file_management.check_if_empty('.temp/temp.json')
    if not isTemp:
        sendToTemp(jsonDict)
        
    keys = cellRefrence.jsonlocation
    keys.pop()
    # print(keys)
    
    nested_data_point = tempDict

    # print(nested_data_point)
    for key in keys:
        nested_data_point = nested_data_point[key]
        
    nested_data_point[newKey] = {}
    # print(tempDict)

    writeToTemp(tempDict)

    print("New Content!")
    
def SmartAdd(newDict=dict):
    loggerObj.addToLog("info_editor.py - SmartAdd")
    global jsonDict, tempDict
    isTemp = not file_management.check_if_empty('.temp/temp.json')
    if not isTemp:
        sendToTemp(jsonDict)
        
    for key, value in newDict.items():
        tempDict[key] = value
        
    writeToTemp(tempDict)
    
def createFilterDictionary(whitelist_term):
    loggerObj.addToLog("info_editor.py - Creating filter dictionary...")
    global jsonDict, tempDict, FilteredDict
    isTemp = not file_management.check_if_empty('.temp/temp.json')
    if not isTemp:
        sendToTemp(jsonDict)
        
    updateTempDict()
    FilteredDict = filter_management.filter_nested_dict(tempDict, whitelist_term)
    
    with open('.temp/filter.json', 'w') as f:
        f.write(json.dumps(FilteredDict, indent=4))
        
    return FilteredDict
        
    
        
        
        
    