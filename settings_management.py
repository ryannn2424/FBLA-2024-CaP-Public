import json
import tkinter as tk
import logger

settings_file = r"config/settings.json"
devlog_file = r"Logs/devlog.txt"
loggerObj = logger.Logger()

def load_settings(): #Outputs settings.json to a dictionary
    # Set global variables
    loggerObj.addToLog("settings_management.py - loading settings to dict...")
    global settings_file
    global settings_dictionary
    
    #Opening and returning the Settings file
    with open(settings_file) as f:
        settings_dictionary = json.load(f)
    return settings_dictionary

def convert_rgb_to_hex(red, green, blue): # Convert 3 RGB values into hex.
    loggerObj.addToLog("settings_management.py - Converting RGB to hex...")
    hex_value = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return hex_value

def change_setting(setting_name, new_value): # sets the value of a key in settins.json.
    loggerObj.addToLog("settings_management.py - Attempting to change settings...")
    global settings_dictionary
    settings_dictionary[setting_name] = new_value
    json_object = json.dumps(settings_dictionary, indent=4)
    with open(settings_file, "w") as outfile:
        outfile.write(json_object)
    loggerObj.addToLog("settings_management.py - Settings changed")
    load_settings()
    
    
def log_entry(custom_text): # Outputs a line to a devlog
    with open(devlog_file, "a") as file:
        file.write(custom_text)
    
def get_all_widgets(root): # Get & return all the widgets present in the root window
    loggerObj.addToLog("settings_management.py - gathering child widgets...")
    widgets = []

    def explore_widget(root):
        widgets.append(root)
        for child in root.winfo_children():
            explore_widget(child)

    explore_widget(root)
    return widgets

def switch_theme(root, new_theme, style): # Switch the theme of all windows to the new theme.
    # THIS SHOULD NOT BE USED ANYMORE!!!
    # USE CUSTOMTKINTER SETTINGS INSTEAD
    if new_theme == "light":
        log_entry("Attempting to switch to light mode...")
        style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", foreground="black", font=('Arial', 10))
        for root_children in get_all_widgets(root):
            try:
                if "button" not in str(root_children) or "radio" in str(root_children):
                    root_children.config(bg="#FFFFFF")
                
            except Exception as error:
                with open(devlog_file, "a") as file:
                    file.write(f"Exception: {str(error)}\n")
    else:
        log_entry("Attempting to switch to dark mode...")
        style.configure("Treeview", background="#121212", fieldbackground="#121212", foreground="white", font=('Arial', 10))
        for root_children in get_all_widgets(root):
            try:
                if "button" not in str(root_children) or "radio" in str(root_children):
                    root_children.config(bg="#121212")
            except Exception as error:
                with open(devlog_file, "a") as file:
                    file.write(f"Exception: {str(error)}\n")

def switch_text_color(root, new_text_color): # Switch the text colors of all elements in the root window
    # THIS SHOULD NOT BE USED ANYMORE!!!
    # USE CUSTOMTKINTER SETTINGS INSTEAD
    log_entry("Attempting to change text color...\n")
    load_settings()
    for root_children in get_all_widgets(root):
        try:
            if "toplevel" in str(root_children) and settings_dictionary["Theme"] == "dark":
                print(root_children)
                root_children.config(fg="white")
            elif "toplevel" in str(root_children) and settings_dictionary["Theme"] == "light":
                root_children.config(fg="black")
            else:
                if "radio" not in str(root_children) and "toplevel" not in str(root_children):
                    root_children.config(fg=new_text_color)
                else:
                    root_children.config(fg="white")
            
        except Exception as error:
            with open(devlog_file, "a") as file:
                file.write(f"Exception: {str(error)}\n")
    root.update_idletasks()
    
def switch_color(root, new_color): # Changes the colors of all buttons in the root window.
    log_entry("Attempting to change element colors...\n")
    for root_children in get_all_widgets(root):
        try:
            if "button" in str(root_children) and "radio" not in str(root_children):
                root_children.config(bg=new_color)
        except Exception as error:
            with open(devlog_file, "a") as file:
                file.write(f"Exception: {str(error)}\n")
    root.update_idletasks()
    
def apply_settings(root, style): # Keeps the customization of different widgets up to date when executed.
    loggerObj.addToLog("settings_management.py - Applying style settings...")
    switch_text_color(root, settings_dictionary["TextColor"])
    switch_color(root, settings_dictionary["ColorHEX"])
    switch_theme(root, settings_dictionary["Theme"], style)