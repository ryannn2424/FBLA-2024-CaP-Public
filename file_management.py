import json
import settings_management
import logger

loggerObj = logger.Logger()
recents_file = r"config/recent_files.json"
recents_dict = {}

#
# IMPORTING -----------------------------------------------------------------------
#

file_path = "" # Empty decloration for later use
supported_files = ["json"] # Change for more support

def determine_file_type_compatability(file): #Determine compatability of file type and its extension
    loggerObj.addToLog("file_management.py - determining file type compatability...")
    global file_path
    file_path = file
    extension_start = file.rfind('.') + 1  # Gets rid of the period to make file extensionr eading easier
    path_length = len(file)
    file_extension = file[extension_start:path_length] # Slices file path to extension only

    for supported_types in supported_files:
        if file_extension == supported_types:
            
            settings_management.change_setting("LastFile", file_path[file.rfind('/') + 1:path_length])
            settings_management.change_setting("LastFilePath", file_path)
            loggerObj.addToLog("file_management.py - File found compatible")
            return [True, file_extension] # Says that the file is compatible
        
    loggerObj.addToLog("file_management.py - ERROR - File found not compatible")
    return [False, "Not Supported"] # Says that the file is not compatible
    
def gui_select_file(): # Uses Tkinter to open a file dialog
    loggerObj.addToLog("file_management.py - creating GUI for file selection...")
    global file_path # Forces function to store file path in the global variable
    import tkinter as tk # Imports Tkinter here to reduce memory load
    from tkinter import filedialog
    file_path = filedialog.askopenfile(title="Select file", filetypes= [("Information File","*.json")]).name # Returns file path
    if determine_file_type_compatability(file_path)[0]: # Determine File's compatability
        # If importing is succesful, return the file path.
        change_recents(file_path)
        return
    else:
        #If importing is not, print the failure.
        loggerObj.addToLog("file_management.py - ERROR - import failed")
        # print("import failed")
#
# RECENT FILES ----------------------------------------------------------------------
#

def load_recents(): # function that returns recent_files.json as a dictionary.
    loggerObj.addToLog("file_management.py - Returning recent files json as dict...")
    global recents_dict
    
    with open(recents_file) as f:
        recents_dictionary = json.load(f)
    
    recents_dict = recents_dictionary
    return recents_dictionary

def change_recents(new_file_path, ): # Updates the recent files json
    loggerObj.addToLog("file_management.py - updating recent files...")
    global recents_dict
    
    load_recents() # Ensures local dict value is up to date
    
    current_index = 0
    key_names = ["File 1", "File 2", "File 3", "File 4", "File 5"]
    
    for key, values in recents_dict.items():
        if values[1] == new_file_path:
            break
        else:
            current_index += 1
            
    # Shift all values down by a key and adds the new file to the dictionary
    if current_index == 5:
        print("changing dict...")
        
        for i in range(len(key_names)-1, 0, -1):
            current_key = key_names[i]
            previous_key = key_names[i-1] if i > 0 else None

            if previous_key in recents_dict:
                recents_dict[current_key] = recents_dict[previous_key]
            else:
                recents_dict.pop(current_key, None)
        
        recents_dict["File 1"] = [new_file_path[new_file_path.rfind('/') + 1:len(new_file_path)], new_file_path]
    
    # Convert back to JSON and write to file
    json_object = json.dumps(recents_dict, indent=4)
    with open(recents_file, "w") as outfile:
        outfile.write(json_object)
        
    loggerObj.addToLog("file_management.py - Recent Files .json updated.")

#
# FILE SAVING ---------------------------------------------------------------------------------
#

def save_file(temp_json, save_file):
    loggerObj.addToLog("file_management.py - Initiating file save...")
    loggerObj.addToLog("file_management.py - Opening temp file...")
    with open(temp_json, 'r') as source: # This copies the data to a variable to save to the actuall file
        data = json.load(source)

    loggerObj.addToLog("file_management.py - copying temp data to main file")
    with open(save_file, 'w') as destination:
        json.dump(data, destination, indent=2) # Copies the data to the file
        
    loggerObj.addToLog("file_management.py - wiping temp file...")
    with open(temp_json, 'w') as wiping:
        pass
    
#
# Other ---------------------------------------------
#    

def check_if_empty(file):
    loggerObj.addToLog("file_management.py - Checking if file is empty")
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            return not bool(data)
    except json.decoder.JSONDecodeError:
        return True
    
def clear_json_file(file_path):
    loggerObj.addToLog("file_management.py - Clearing json")
    with open(file_path, 'w') as file:
        pass