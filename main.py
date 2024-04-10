import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import customtkinter
from PIL import Image
import testing
# Custom Libraries

import file_management as filesmanage # This library deals and manages with the files that the program uses
import settings_management as settingsmanage # This library manages the settings.json file
import settings_page # Opens and manages the settings popup
import info_editor # The main editing window of the program
import custom_widgets
import logger
    
def main():
    logger.__name__ = "RanAtMain"
    loggerObj = logger.Logger()

    # Load settings
    settingsmanage.load_settings() # Stores the settings.json file as a dictionary
    customtkinter.set_appearance_mode(settingsmanage.settings_dictionary["Theme"])
    recent_files_dictionary = filesmanage.load_recents() # Loads the recent_files.json as a dictionary.

    # Window SettingsNow 
    root = customtkinter.CTk() # The actuall Tk window itself.
    loggerObj.addToLog("Creating root window")
    root.wm_geometry("1280x720") #720p (Can be changed)
    root.title("Infollect") # Name of the program
    # style = ttk.Style(root) # Style variable for ttk widget styling
    # style.theme_use("clam")
    
    # FUNCTIONS ------------------------------------------------------------------

    # Selecting a file
    def select_file():
        loggerObj.addToLog("Selecting File..")
        filesmanage.gui_select_file() # Opens a window for the user to select a file
        # print(filesmanage.file_path) DEBUG
        editing_frame.file_path.configure(text=filesmanage.file_path) # Sets the path shower 
        loggerObj.addToLog("Selected File: " + filesmanage.file_path)
        # info_editor.clear_treeview() # Clears the editor TreeView
        editingDict = info_editor.jsonToDict(filesmanage.file_path)
        spreadsheet_frame.custom_info_editor.clearEditor()
        spreadsheet_frame.custom_info_editor.editingDict=editingDict
        spreadsheet_frame.custom_info_editor.populateEditor(editingDictionary=editingDict) # Repopulates the editor TreeView
        spreadsheet_frame.update()
        update_recent_files() # Update the recent_files.json
        
    def save_file(): # Saves the temp file to the actuall file.
        loggerObj.addToLog("Saving File at .temp/temp.json")
        filesmanage.save_file(r'.temp/temp.json', filesmanage.file_path) # Runs the save file function with the temp file and the selected file
        
    def file_recover(): # Prompts the user to recover their file if they forgot to save it
        if not filesmanage.check_if_empty(r'.temp/temp.json'): # Runs if the temp file is NOT empty.
            # Prompts the user for a yes or no, and recovers the file if yes is picked
            if messagebox.askquestion("File Recovery", f"An unsaved temporary version of your file was detected. Would you like to recover your save file? ({settingsmanage.settings_dictionary['LastFile']})") == "yes":
                filesmanage.file_path = settingsmanage.settings_dictionary["LastFilePath"] # Returns the last path from the settings path
                editingDict = info_editor.jsonToDict(filesmanage.file_path) # Loads the selected file as a dictionary
                spreadsheet_frame.custom_info_editor.editingDict=editingDict # Sets the editingDict
                info_editor.updateTempDict()
                spreadsheet_frame.custom_info_editor.populateWithTemp()#Repopulates the main TreeView's contents/
            else:
                filesmanage.clear_json_file(r'.temp/temp.json')
        
    def open_settings_page(): # Opens the settings popup
        loggerObj.addToLog("Opening Settings Page")
        settings_page.SettingsPage()
        # settings_page.settings_page(root, style)
        # spreadsheet_viewer.columnconfigure(0, weight=1)
        # spreadsheet_viewer.columnconfigure(1, weight=9)
        
    # Update the contents of the recent files list
    def update_recent_files(): # Update the 
        loggerObj.addToLog("Updating recent files json")
        recent_files_list = side_panel.recent_files_list
        recent_files_list.update_recent_files(recent_files_dictionary)
        
    def load_recent_file(): # Takes the selected file in the recent files treeview and opens it.
        
        tree_widget = side_panel.recent_files_list
        
        selected_item = tree_widget.selectedFile
        path = selected_item[1] #!!!! VERIFY FILE
        if filesmanage.determine_file_type_compatability(path)[0]: # Checks if the file type is compatible
            editing_frame.file_path.configure(text=path)
            # info_editor.clear_treeview()
            loggerObj.addToLog("Found file & loading " + filesmanage.file_path)
            editingDict = info_editor.jsonToDict(filesmanage.file_path) # Loads the selected file as a dictionary
            spreadsheet_frame.custom_info_editor.clearEditor()
            spreadsheet_frame.custom_info_editor.editingDict=editingDict # Sets the editingDict
            spreadsheet_frame.custom_info_editor.populateEditor(editingDictionary=editingDict) # Repopulates the editor TreeView
        
    def create_new_file(): # Creates a new file and then selects it for use
        loggerObj.addToLog("Creating window for file creation")
        
        popup = customtkinter.CTkToplevel(root) # Creates the popup
        popup.geometry("300x130")
        popup.title("Enter New File Name") # Name of the popup
        
        customtkinter.CTkLabel(popup, text="File name").pack(padx=10, pady=5) # Label
        entry = customtkinter.CTkEntry(popup)# Entry
        entry.pack(padx=10, pady=10)
        
        def makefile(): # Executes when the confirm button is pressed, and creates the new file
            loggerObj.addToLog("Attempting to create file...")
            
            new_path = 'Files/' + entry.get() + '.json' # Creates the path of the new file
            with open(new_path, 'w') as json_file:
                json.dump({}, json_file, indent=2) # Creates the new file
                
            loggerObj.addToLog("File made. Loading to editor...")
            
            filesmanage.determine_file_type_compatability(new_path) # Checks if the file type is compatible
            editing_frame.file_path.configure(text=filesmanage.file_path) # Sets the path shower
            
            editingDict = info_editor.jsonToDict(filesmanage.file_path) # Loads the selected file as a dictionary
            spreadsheet_frame.custom_info_editor.clearEditor()
            spreadsheet_frame.custom_info_editor.editingDict=editingDict # Sets the editingDict
            spreadsheet_frame.custom_info_editor.populateEditor(editingDictionary=editingDict)
            
            update_recent_files() # Updates the recents
            
            loggerObj.addToLog("Topview destroyed")
            popup.destroy() # Destroys the popup window")
            
        close_button = customtkinter.CTkButton(popup, text="Confirm", command=makefile) # Button that executes makefile()
        close_button.pack(padx=10, pady=10)
        
        popup.wait_window() # Waits for the popup to be destroyed.
        

    # FRAME CONFIGURATION --------------------------------------------------------
    loggerObj.addToLog("Configuring root weights...")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=200)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)

    loggerObj.addToLog("Interaction panel instantiation...")
    interaction_panel = InteractionWidget(master=root)
    
    # Side panel (Contains most features pretaining to file management)
    loggerObj.addToLog("Side panel instantiation...")
    side_panel = SideWidget(master=interaction_panel, select_file_cmd=select_file, create_new_file_cmd=create_new_file, load_recent_file_cmd=load_recent_file)
    
    # Bottom panel
    loggerObj.addToLog("Bottom panel instantiation...")
    bottom_panel = BottomWidget(master=root, settings_page_cmd=open_settings_page)

    # Editing Frame (Contains all feautures relating to the augumentation of data)
    loggerObj.addToLog("Instantiating editing widgets....")
    editing_frame = EditingWidget(master=interaction_panel)
    spreadsheet_frame = SpreadsheetWidgit(editing_frame, save_file_cmd=save_file, editingWidgetRef=editing_frame) # Spreadsheet Widgit
    SearchWidget(master=editing_frame, editor_ref=spreadsheet_frame.custom_info_editor)

    # External Commands -----------
    #update_recent_files()
    side_panel.recent_files_list.update_recent_files(recent_files_dictionary)
    loggerObj.addToLog("Updated recent files list")
    
    
    # SPREEDSHEET WIDGET ---------------------------------------------
    ##############################################################
    # info_editor.json_editor(spreadsheet_frame.spreadsheet_lister)
    # Moved to SpreadsheetWidgit.
    
    # json_editor = custom_widgets.CtkInformationEditor(spreadsheet_frame.spreadsheet_lister)
    # json_editor.grid(sticky="nwes", column=0, row=0)
    
    
    # settingsmanage.apply_settings(root, style)
    loggerObj.addToLog("Looking for recoverable files...")
    file_recover() # Checks if there is a recoverable file

    loggerObj.addToLog("Running root window...")
    root.update_idletasks() # Update the GUI
    root.mainloop() # Run the GUI

class InteractionWidget(customtkinter.CTkFrame): 
    def __init__(self, master) -> None: 
        super().__init__(master)
        self.grid(sticky="snwe", column=0, row=0)
        
        def grid_configuration():
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=20)
            self.columnconfigure(1, weight=7)
            
        grid_configuration()
        
class BottomWidget(customtkinter.CTkFrame):
    def __init__(self, master, settings_page_cmd) -> None:
        super().__init__(master)
        self.grid(sticky="snwe", column=0, row=1)
        
        bottom_pnl_label = customtkinter.CTkLabel(self, text="Infollect v2.1.2") # Label for version
        

        settings_button = customtkinter.CTkButton(self, command=settings_page_cmd, text="Settings") # Settings button
        
        def grid_configuration():
            self.columnconfigure(0, weight=12)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(0, weight=1)
            
            bottom_pnl_label.grid(column=0, row=0, sticky="w", padx=2)
            
            settings_button.grid(sticky="news", column=1, row=0)
            
            
        grid_configuration()
        
class SideWidget(customtkinter.CTkFrame):
    def __init__(self, master, select_file_cmd, create_new_file_cmd, load_recent_file_cmd) -> None:
        super().__init__(master)
        self.grid(sticky="snwe", column=0, row=0)
        
        side_widget_seperator = customtkinter.CTkFrame(self, fg_color="transparent") # Side widget seperator
        logo = customtkinter.CTkImage(Image.open("Resources/images/logo.png"), size=(200, 200)) # Logo
        logoLabel = customtkinter.CTkLabel(side_widget_seperator, image=logo, text="") # Logo
        logoLabel.grid(sticky="nsew", column=0, row=0) 
        # logoLabel.image = logo
        
        
        # open_file_button = tk.Button(self, command=select_file_cmd, text="Open File")
        open_file_button = customtkinter.CTkButton(self, command=select_file_cmd, text="Open File", ) # Open file button
        new_file_button = customtkinter.CTkButton(self, command=create_new_file_cmd, text="New File") # New file button
        recent_files_label = customtkinter.CTkLabel(self, text="Recent Files", justify="center") # Recent files label

        self.recent_files_list = custom_widgets.CtkTable(master=self)
        
        load_recent_button = customtkinter.CTkButton(self, command=load_recent_file_cmd, text="Open Recent File") # Load recent file button
    
        
        def grid_configuration():
            self.rowconfigure(2, weight=1)
            self.columnconfigure(0, weight=1)
            
            side_widget_seperator.grid(row=2, column=0)
            
            open_file_button.grid(sticky="ew", column=0, row=0, padx=2, pady=1)
            new_file_button.grid(sticky="ew", column=0, row=1, padx=2, pady=1)
            recent_files_label.grid(column=0, row=4)
            
            self.recent_files_list.grid(sticky="ew", column=0, row=5)
            
            load_recent_button.grid(sticky="ew", column=0, row=6)
            
            
        grid_configuration()
            
class SearchWidget(customtkinter.CTkFrame):
    def __init__(self, master, editor_ref) -> None:
        super().__init__(master)
        self.grid(sticky="snwe", column=0, row=2)
        self.after_id = None
        self.editor_ref = editor_ref
        
        # Widgets contained within the search frame
        self.search_filter = customtkinter.CTkEntry(self) # Search filter
        self.search_filter.bind("<KeyRelease>", self.search_filter.bind("<KeyRelease>", self.on_entry_change))
        button_exit_filter = customtkinter.CTkButton(self, text="", font=("Hack Nerd Font", 15), command=lambda: custom_widgets.CtkFilterOptions(self))
        
        # tooltips.ToolTip(button_exit_filter, "Exit Filter Mode")
        
        def grid_configuration():
            self.columnconfigure(0, weight=500)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=0)
            
            # Controls the size of contained widgets
            self.search_filter.grid(sticky="nsew", column=0, row=0)
            button_exit_filter.grid(sticky="nsew", column=1, row=0)
            
        grid_configuration()
    
    def on_entry_change(self, event):
            if self.after_id is not None:
                self.after_cancel(self.after_id)  # Cancel previous scheduled event
            self.after_id = self.after(1000, self.process_entry_change, event.widget)

    def process_entry_change(self, entry_widget):
        # print(info_editor.createFilterDictionary(entry_widget.get()))
        self.editor_ref.populateWithFilter(entry_widget.get())
        
        
class EditingWidget(customtkinter.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.grid(sticky="snwe", column=1, row=0)
        
        # Contained widgets
        # path_frame = customtkinter.CTkFrame(self)
        self.file_path = customtkinter.CTkLabel(self, text="No file selected!")
        
        def grid_configuration():
            # Grid configuration for the encapsulating frame
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(2, weight=2)
            self.rowconfigure(3, weight=140)
            
            # path_frame.grid(sticky="snwe", column=0, row=1)
            self.file_path.grid(column=0, row=0, sticky="ew")
            
        
        grid_configuration()
        
class SpreadsheetWidgit(customtkinter.CTkFrame):
    def __init__(self, master, save_file_cmd, editingWidgetRef) -> None:
        super().__init__(master)
        self.grid(sticky="snwe", column=0, row=3)
        
        def checkIfFileOpened():
            if editingWidgetRef.file_path._text == "No file selected!": # If no file is opened
                tk.messagebox.showinfo(title=None, message="Please open or create a file before using this function.") # Show error message
            else:
                testing.BuisnessScanner(addresses=["None"], smartAddCommand=info_editor.SmartAdd, custom_widgit_ref=self.custom_info_editor) # Open Buisness Scanner
                
        spreadsheet_editor_side = customtkinter.CTkFrame(self)
        
        self.spreadsheet_lister = customtkinter.CTkFrame(self)
                
        self.custom_info_editor = custom_widgets.CtkInformationEditor(self.spreadsheet_lister)
        
        # Information edit buttons
        customtkinter.CTkButton(spreadsheet_editor_side, text="Add Dropdown", command=lambda: self.custom_info_editor.selectedCell[1].addCollapsableCell()).grid(column=0, row=0, sticky="news", padx=2, pady=1)
        customtkinter.CTkButton(spreadsheet_editor_side, text="Add Information", command=lambda: self.custom_info_editor.selectedCell[1].addContentCell()).grid(column=0, row=1, sticky="news", padx=2, pady=1)
        customtkinter.CTkButton(spreadsheet_editor_side, text="Delete Cell", command=lambda: self.custom_info_editor.selectedCell[1].destroySelf()).grid(column=0, row=2, sticky="news", padx=2, pady=1)
        customtkinter.CTkButton(spreadsheet_editor_side, text="Smart Insert", command=lambda: checkIfFileOpened()).grid(column=0, row=3, sticky="news", padx=2, pady=1)
        # customtkinter.CTkButton(spreadsheet_editor_side, text="Clear Editor", command=lambda: self.custom_info_editor.clearEditor()).grid(column=0, row=4, sticky="news", padx=2, pady=1)
        # customtkinter.CTkButton(spreadsheet_editor_side, text="repop", command=lambda: self.custom_info_editor.populateWithTemp()).grid(column=0, row=5, sticky="news", padx=2, pady=1)
        
        customtkinter.CTkFrame(spreadsheet_editor_side).grid(column=0, row=4, sticky="news") # Serves as a seperator 
        
        customtkinter.CTkButton(spreadsheet_editor_side, text="Save File", command=save_file_cmd).grid(column=0, row=5, sticky="news", padx=2, pady=1) # Save button
        
        self.custom_info_editor.grid(sticky="news", column=0, row=0)

        def grid_configuration():
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=30)
            
            spreadsheet_editor_side.grid(sticky="news", column=0, row=0)
            spreadsheet_editor_side.columnconfigure(0, weight=1)
            spreadsheet_editor_side.columnconfigure(0, weight=1)
            spreadsheet_editor_side.rowconfigure(4, weight=1)
            
            self.spreadsheet_lister.grid(sticky="news", column=1, row=0)
            self.spreadsheet_lister.columnconfigure(0, weight=1)
            self.spreadsheet_lister.rowconfigure(0, weight=1)
            
        grid_configuration()
    
if __name__ == "__main__":
    main() #Ensures the file is ran alone.