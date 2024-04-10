import json

def updateFilterSettings(filterSettingsJson="./config/filter.json", settingName=None, settingValue=None):
    with open(filterSettingsJson, 'r') as json_file:
        data = json.load(json_file)
        
    data[settingName] = settingValue
    
    # print(data) # debug
    
    with open(filterSettingsJson, 'w') as json_file:
        json.dump(data, json_file)
        
def loadFilterSettings(filterSettingsJson="./config/filter.json"):
    with open(filterSettingsJson, 'r') as json_file:
        data = json.load(json_file)
        
    return data

def filterSettings(filterSettingsJson="./config/filter.json"):
    with open(filterSettingsJson, 'r') as json_file:
        data = json.load(json_file)
        
    return data

def filter_nested_dict(nested_dict, whitelist_term, settingsJson=filterSettings()):
    filtered_dict = {}
    
    if settingsJson["dropdown"] == True:

        for key, value in nested_dict.items():
            if whitelist_term.lower() in str(key).lower():
                filtered_dict[key] = value
            elif isinstance(value, dict):
                nested_filtered = filter_nested_dict(value, whitelist_term)
                if nested_filtered:
                    filtered_dict[key] = nested_filtered

        # return filtered_dict
    if settingsJson['label'] == True:

        for key, value in nested_dict.items():
            if whitelist_term in str(key).lower() or (not isinstance(value, dict) and whitelist_term.lower() in str(value).lower()):
                filtered_dict[key] = value
            elif isinstance(value, dict):
                nested_filtered = filter_nested_dict(value, whitelist_term)
                if nested_filtered:
                    filtered_dict[key] = nested_filtered
                    
    if settingsJson['content'] == True:
        
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                filtered_value = filter_nested_dict(value, whitelist_term)
                if filtered_value:
                    filtered_dict[key] = filtered_value
            elif isinstance(value, str) and whitelist_term.lower() in value.lower():
                filtered_dict[key] = value
                
    return filtered_dict
        
# print(filter_nested_dict(nested_dict, 'New York'))