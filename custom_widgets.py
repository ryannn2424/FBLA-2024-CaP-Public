import tkinter as tk
import customtkinter

import filter_management
import info_editor
import logger

class CtkTable(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.logger = logger.Logger()
        
        class RecentCell(customtkinter.CTkFrame):
            def __init__(self, master=None, **kwargs):
                super().__init__(master, **kwargs)
                self.logger = logger.Logger()
                self.logger.addToLog("custom_widgits.py - creating RecentCell..")
                
                self.fileName = None
                self.filePath = None
                self.isSelected = False
                
                # self.bind("<Button-1>", command=self.pressed)
                
                fileNameLabel = customtkinter.CTkLabel(self, text="File Name")
                # fileNameLabel.bind("<Button-1>", command=self.pressed)
                fileNameLabel.grid(column=0, row=0, sticky="nsew")
                
                filePathLabel = customtkinter.CTkLabel(self, text="Path")
                # filePathLabel.bind("<Button-1>", command=self.pressed)
                filePathLabel.grid(column=10, row=0, sticky="nsew")
                
                self.columnconfigure(0, weight=4)
                self.columnconfigure(1, weight=3)
                
            
                    
            def other_pressed(self):
                self.logger.addToLog("custom_widgits.py - Recent Cell Pressed")
                self.isSelected = False
                self.configure(fg_color="Transparent")
        
        def CellPressed(cell):
            self.logger.addToLog("custom_widgits.py - Selection verification for RecentFiles")
            if not cell.isSelected and cell.fileName != "":
                if self.selectedCell is not None and self.selectedCell != cell:
                    self.selectedCell.configure(fg_color=self.defaultColorTuple)
                    self.selectedCell.isSelected = False
                print("run")
                cell.configure(fg_color="#144870")
                cell.isSelected = True
                self.selectedCell = cell
                self.selectedFile = [cell.fileName, cell.filePath]
               
        self.selectedCell = None
        self.selectedFile = [None, None] 

        self.defaultColorTuple = ("#dbdbdb", "#2b2b2b")
                        
        topFrame = customtkinter.CTkFrame(self, fg_color="#0078ff")
        topFrame.grid(column=0, row=0, sticky="nsew")
        
        customtkinter.CTkLabel(topFrame, text="File Name", bg_color="#006ce6").grid(column=0, row=0, sticky="nsew")
        customtkinter.CTkLabel(topFrame, text="Path", bg_color="#0078ff").grid(column=1, row=0, sticky="nsew")
        
        topFrame.columnconfigure(0, weight=4)
        topFrame.columnconfigure(1, weight=3)
        
        bottomFrame = customtkinter.CTkFrame(self)
        bottomFrame.grid(column=0, row=1, sticky="nsew")
        
        bottomFrame.columnconfigure(0, weight=1)
        bottomFrame.rowconfigure(0, weight=1)
        
        self.cellList = []
        
        for cell in range(5):
            self.logger.addToLog(f"custom_widgits.py - Itterating through cell creation ({cell})")
            # print(cell)
            self.cellList.append(RecentCell(bottomFrame))
            self.cellList[cell].grid(column=0, row=cell, sticky="nsew")
            self.cellList[cell].bind("<Button-1>", lambda event, cell=self.cellList[cell]: CellPressed(cell))
            for cellText in self.cellList[cell].winfo_children():
                cellText.bind("<Button-1>", lambda event, cell=self.cellList[cell]: CellPressed(cell))
            bottomFrame.rowconfigure(cell, weight=1)
        
        
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)
        
    def update_recent_files(self, recent_files_dictionary): # Update the
        self.logger.addToLog("custom_widgits.py - Updating Recents GUI")
        for cell in self.cellList:
            for textChildren in cell.winfo_children():
                textChildren.configure(text="")
        
        cellIndex = 0
        for key, values in recent_files_dictionary.items(): # Populate the Recent_files TreeView.
            localIndex = 0
            self.cellList[cellIndex].fileName = values[0]
            self.cellList[cellIndex].filePath = values[1]
            for textChildren in self.cellList[cellIndex].winfo_children():
                if localIndex == 0:
                    textChildren.configure(text=values[0])
                else:
                    if self.cellList[cellIndex].filePath != "":
                        trimmedValue = values[1][0:15] + "..."
                    else: 
                        trimmedValue = ""
                    
                    textChildren.configure(text=trimmedValue)
                localIndex += 1
            cellIndex += 1            
    
class CtkInformationEditor(customtkinter.CTkScrollableFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = logger.Logger()
        self.logger.addToLog("custom_widgits.py - Instancing CtkInformationEditor")

        self.editingDict = None

        self.columnconfigure(0, weight=1)
        
        self.selectedCell = [False, object]
        # self.rowconfigure(0, weight=1)
        # self.CollapsableCell(self, contentText="Information Editor").grid(column=0, row=0, sticky="we")
        # self.ContentCell(self, contentText="text1", treeLevel=0).grid(column=0, row=1, sticky="we")
        # self.ContentCell(self, contentText="text2", treeLevel=1).grid(column=0, row=2, sticky="we")
        # self.ContentCell(self, contentText="text3", treeLevel=2).grid(column=0, row=3, sticky="we")

    class CollapsableCell(customtkinter.CTkFrame):
        
        def __init__(self, master=None, state="collapsed", editingDict={}, contentText="", treeLevel=0, jsonlocation=[], populateTreeFunc=None, parentRefrence=None, contentCellClass=None, CollapsableCellClass=None, **kwargs):
            super().__init__(master, height=5, fg_color="transparent", **kwargs)
            
            self.logger = logger.Logger()

            self.state = state
            self.populateCellCount = 0
            self.jsonlocation = jsonlocation
            self.populateTreeFunc = populateTreeFunc
            self.editingDict = editingDict
            self.treeLevel = treeLevel
            self.parentRefrence = parentRefrence
            self.selectedCellList = self.parentRefrence.selectedCell
            self.ContentCellClass = contentCellClass
            self.CollapsableCellClass = CollapsableCellClass

            self.columnconfigure(0, weight=1)
            
            # print(jsonlocation)
            self.treeIndicator = ""
            
            if treeLevel == 0:
                self.treeIndicator = ""
            else:
                indicateRoot = "└─"
                for lineWidth in range(treeLevel):
                    if lineWidth != 0:
                        self.treeIndicator += "         "
                self.treeIndicator += indicateRoot

            self.containingFrame = customtkinter.CTkFrame(self, fg_color='transparent')
            self.containingFrame.grid(column=0, row=0, sticky="ew")
            self.containingFrame.columnconfigure(0, weight=1)
            
            self.containingFrame.columnconfigure(0, weight=1)
            self.containingFrame.columnconfigure(1, weight=100)
            
            self.arrow = customtkinter.CTkLabel(self.containingFrame, text=f"{self.treeIndicator}▼ ")
            self.arrow.grid(column=0, row=0, sticky="ew")

            self.content = customtkinter.CTkLabel(self.containingFrame, text=contentText, justify="left")
            self.content.grid(column=1, row=0, sticky="w")

            self.arrow.bind("<Button-1>", lambda event: self.collapseCell())
            self.content.bind("<Button-1>", lambda event: self.collapseCell())
            
            self.containingFrame.bind("<Button-1>", lambda event: self.selectSelf())    
            # self.configure(fg_color="red") 
            
            self.containingFrame.bind("<Button-3>", self.rightClickmenu)
            self.arrow.bind("<Button-3>", self.rightClickmenu)
            self.content.bind("<Button-3>", self.rightClickmenu)
            
        def collapseCell(self):
            self.logger.addToLog("custom_widgits.py - Collapsable Cell left clicked")
            if self.state == "collapsed":
                self.state = "uncollapsed"
                self.arrow.configure(text=f"{self.treeIndicator}▲ ")
                self.populateTreeFunc(parent=self, editingDictionary=self.editingDict, ranAtRoot=False)
            else:
                self.state = "collapsed"
                self.arrow.configure(text=f"{self.treeIndicator}▼ ")
                
                widgetIndex = 0
                for widget in self.winfo_children():
                    if widgetIndex != 0:
                        # print(f"{widgetIndex} - {widget}")
                        widget.destroy()
                    widgetIndex += 1
                # direct_children = [child for child in self.winfo_children() if child.master == self]
                # # print(len(direct_children))
                # for row in range(len(direct_children)):
                #     for widget in self.grid_slaves(column=0):
                #         if int(widget.grid_info()["row"]) == row + 1:
                #             widget.destroy()
                
        def rightClickmenu(self, event):
            self.logger.addToLog("custom_widgits.py - Collapsable Cell Right Clicked")
            self.selectSelf()
            menu = tk.Menu(self, tearoff=0)
            menu.focus_set()
            menu.add_command(label='Delete Cell', command=self.destroySelf)
            menu.add_command(label='Add Info To Dropdown', command=self.addContentCell)
            menu.add_command(label='Add New Dropdown', command=self.addCollapsableCell)
            menu.post(event.x_root, event.y_root)
            menu.bind('<FocusOut>', lambda event: menu.destroy())
            
        def destroySelf(self):
            self.logger.addToLog("custom_widgits.py - Deleting Collapsable Cell...")
            self.parentRefrence.selectedCell = [False, None]
            info_editor.deleteCellData(self)
            self.destroy()
            
        def addContentCell(self):
            self.logger.addToLog("custom_widgits.py - Adding Content Cell from Collapsable Cell...")
            def addInfo():
                self.populateCellCount += 1
                newContentCell = self.ContentCellClass(self, keyText=entry1.get(), valueText=entry2.get(), parentRefrence=self, jsonlocation=self.jsonlocation + [entry1.get()],treeLevel=self.treeLevel + 1)
                newContentCell.grid(column=0, row=self.populateCellCount, sticky="ew")
                info_editor.newContentInfo(newContentCell, entry1.get(), entry2.get())
                toplevel.destroy()
                
            if self.state == "collapsed":
                self.collapseCell()
            
            toplevel = customtkinter.CTkToplevel(self)
            toplevel.title("Add Info")
            
            customtkinter.CTkLabel(toplevel, text="Info Label: ").grid(column=0, row=0)

            entry1 = customtkinter.CTkEntry(toplevel, placeholder_text="Enter Text...")
            entry1.grid(column=0, row=1)
                
            customtkinter.CTkLabel(toplevel, text="Info Content: ").grid(column=0, row=2)

            entry2 = customtkinter.CTkEntry(toplevel, placeholder_text="Enter Text...")
            entry2.grid(column=0, row=3)
            
            buttomFrame = customtkinter.CTkFrame(toplevel)
            buttomFrame.grid(column=0, row=4, padx=5, pady=3)
            
            closeButton = customtkinter.CTkButton(buttomFrame, text="Close", command=toplevel.destroy).grid(column=0, row=0, padx=2)
            createButton = customtkinter.CTkButton(buttomFrame, text="Create", command=addInfo).grid(column=1, row=0, padx=2)
            
            toplevel.after(100, toplevel.lift)
            
        def addCollapsableCell(self):
            self.logger.addToLog("custom_widgits.py - Adding Collapsable Cell from Collapsable Cell...")
            def addCollapse():
                self.populateCellCount += 1
                newCell = self.CollapsableCellClass(self, contentCellClass=self.ContentCellClass, CollapsableCellClass=self.CollapsableCellClass, contentText=entry1.get(), parentRefrence=self.parentRefrence, jsonlocation=self.jsonlocation + [entry1.get()],treeLevel=self.treeLevel + 1, populateTreeFunc=self.populateTreeFunc)
                newCell.grid(column=0, row=self.populateCellCount, sticky="ew")
                print(newCell.editingDict)
                    # cell = self.CollapsableCell(parent, contentCellClass=self.ContentCell, CollapsableCellClass=self.CollapsableCell, jsonlocation=newJsonLocation, parentRefrence=self, editingDict=parent.editingDict[key], contentText=key, treeLevel=parent.treeLevel + 1, populateTreeFunc=self.populateEditor)
                info_editor.NewCollapsableInfo(newCell, entry1.get())
                customEditingDict = self.editingDict
                customEditingDict[entry1.get()] = {}
                newCell.editingDict = customEditingDict[entry1.get()]
                newCell.jsonlocation = self.jsonlocation + [entry1.get()]
                toplevel.destroy()
                
            
            if self.state == "collapsed":
                self.collapseCell()
            
            toplevel = customtkinter.CTkToplevel(self)
            toplevel.title("Add Collapse")
            
            customtkinter.CTkLabel(toplevel, text="Collapsable Name:").grid(column=0, row=0)

            entry1 = customtkinter.CTkEntry(toplevel, placeholder_text="Enter Text...")
            entry1.grid(column=0, row=1)
            
            buttomFrame = customtkinter.CTkFrame(toplevel)
            buttomFrame.grid(column=0, row=2, padx=5, pady=3)
            
            closeButton = customtkinter.CTkButton(buttomFrame, text="Close", command=toplevel.destroy).grid(column=0, row=0, padx=2)
            createButton = customtkinter.CTkButton(buttomFrame, text="Create", command=addCollapse).grid(column=1, row=0, padx=2)
            
            toplevel.after(100, toplevel.lift)

        def unselectSelf(self):
            self.logger.addToLog(f"custom_widgits.py - {self} unselected")
            # self.selectedCellList
            print('Running')
            self.containingFrame.configure(fg_color="transparent")
            
        def selectSelf(self):
            self.logger.addToLog(f"custom_widgits.py - {self} selected")
            self.parentRefrence.selectedCell
            # print("Pressed")
            # print(self.parentRefrence.selectedCell)
            # self.selectedCellList
            if self.parentRefrence.selectedCell[0] == False:
                self.containingFrame.configure(fg_color="#2288D7")
                self.parentRefrence.selectedCell = [True, self]
            else:
                print(self.parentRefrence.selectedCell[1])
                self.parentRefrence.selectedCell[1].unselectSelf()
                self.containingFrame.configure(fg_color="#2288D7")
                self.parentRefrence.selectedCell = [True, self]
                

    class ContentCell(customtkinter.CTkFrame):
        def __init__(self, master=None, keyText="", valueText="", treeLevel=0, jsonlocation=[], parentRefrence=None, **kwargs):
            super().__init__(master, height=5, fg_color="transparent", **kwargs)
            self.logger = logger.Logger()

            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=101)
            self.treeLevel = treeLevel
            self.parentRefrence = parentRefrence
            self.jsonlocation = jsonlocation


            
            self.treeIndicator = ""

            if treeLevel == 0:
                self.treeIndicator = ""
            else:
                indicateRoot = "└─"
                for lineWidth in range(treeLevel):
                    if lineWidth != 0:
                        self.treeIndicator += "         "
                self.treeIndicator += indicateRoot

            self.treeIndicatorLabel = customtkinter.CTkLabel(self, text=self.treeIndicator)
            self.treeIndicatorLabel.grid(column=0, row=0, sticky="ew")

            self.keyContent = customtkinter.CTkLabel(self, text=f"{keyText}:", justify="left", font=customtkinter.CTkFont(family="Arial", size=12, weight="bold"))
            self.keyContent.grid(column=1, row=0, sticky="w")
            
            self.valueContent = customtkinter.CTkLabel(self, text=valueText, justify="left", )
            self.valueContent.grid(column=2, row=0, sticky="w")
            
            self.bind("<Button-1>", lambda event: self.selectSelf())
            self.keyContent.bind("<Button-1>", lambda event: self.selectSelf())
            self.treeIndicatorLabel.bind("<Button-1>", lambda event: self.selectSelf())
            self.valueContent.bind("<Button-1>", lambda event: self.selectSelf())
            
            self.bind("<Button-3>", self.rightClickmenu)
            self.keyContent.bind("<Button-3>", self.rightClickmenu)
            self.treeIndicatorLabel.bind("<Button-3>", self.rightClickmenu)
            self.valueContent.bind("<Button-3>", self.rightClickmenu)
            
            
        def rightClickmenu(self, event):
            self.logger.addToLog("custom_widgits.py - Content Cell Right Clicked")
            self.selectSelf()
            menu = tk.Menu(self, tearoff=0)
            menu.focus_set()
            menu.add_command(label='Delete Cell', command=self.destroySelf)
            menu.add_command(label='Add Info To Dropdown', command=self.addContentCell)
            menu.add_command(label='Add New Dropdown', command=self.addCollapsableCell)
            menu.add_command(label='Edit Cell', command=self.editCell) 
            menu.tk_popup(event.x_root, event.y_root)
            menu.bind('<FocusOut>', lambda event: menu.destroy())
            
        def destroySelf(self):
            self.logger.addToLog("custom_widgits.py - Content Cell Destroyed")
            self.parentRefrence.selectedCell = [False, None]
            info_editor.deleteCellData(self)
            self.destroy()
            
        def editCell(self):
            popup = customtkinter.CTkToplevel(self)
            popup.title("Edit Cell")
            popup.columnconfigure(0, weight=1)
            
            def continues():
                newKey = entry1.get()
                newValue = entry2.get()
                info_editor.updateCellData(self, newKey, newValue)
                self.keyContent.configure(text=f"{newKey}:")
                self.valueContent.configure(text=newValue)
                popup.destroy()
            
            customtkinter.CTkLabel(popup, text="Content Label:").grid(column=0, row=0)
            entry1 = customtkinter.CTkEntry(popup, placeholder_text="Content Label")
            entry1.grid(column=0, row=1)
            
            customtkinter.CTkLabel(popup, text="Content:").grid(column=0, row=2)
            entry2 = customtkinter.CTkEntry(popup, placeholder_text="Content")
            entry2.grid(column=0, row=3)
            
            buttonframe = customtkinter.CTkFrame(popup)
            buttonframe.grid(column=0, row=4)
            customtkinter.CTkButton(buttonframe, text="Cancel", command=popup.destroy).grid(column=0, row=0)
            customtkinter.CTkButton(buttonframe, text="Confirm", command=continues).grid(column=1, row=0)
            
            
        def addContentCell(self):
            self.logger.addToLog("custom_widgits.py - Content Cell Info Added")
            def addInfo():
                self.master.populateCellCount += 1
                newContentCell = self.master.ContentCellClass(self.master, keyText=entry1.get(), valueText=entry2.get(), parentRefrence=self.master, jsonlocation=self.master.jsonlocation + [entry1.get()],treeLevel=self.master.treeLevel + 1)
                newContentCell.grid(column=0, row=self.master.populateCellCount, sticky="ew")
                info_editor.newContentInfo(newContentCell, entry1.get(), entry2.get())
                toplevel.destroy()
                
            if self.master.state == "collapsed":
                self.master.collapseCell()
            
            toplevel = customtkinter.CTkToplevel(self)
            toplevel.title("Add Info")
            
            customtkinter.CTkLabel(toplevel, text="Info Label: ").grid(column=0, row=0)

            entry1 = customtkinter.CTkEntry(toplevel, placeholder_text="Enter Text...")
            entry1.grid(column=0, row=1)
                
            customtkinter.CTkLabel(toplevel, text="Info Content: ").grid(column=0, row=2)

            entry2 = customtkinter.CTkEntry(toplevel, placeholder_text="Enter Text...")
            entry2.grid(column=0, row=3)
            
            buttomFrame = customtkinter.CTkFrame(toplevel)
            buttomFrame.grid(column=0, row=4, padx=5, pady=3)
            
            closeButton = customtkinter.CTkButton(buttomFrame, text="Close", command=toplevel.destroy).grid(column=0, row=0, padx=2)
            createButton = customtkinter.CTkButton(buttomFrame, text="Create", command=addInfo).grid(column=1, row=0, padx=2)
            
            toplevel.after(100, toplevel.lift)

        def addCollapsableCell(self):
            self.logger.addToLog("custom_widgits.py - Collapsable Cell Info Added")
            def addCollapse():
                self.master.populateCellCount += 1
                newCell = self.master.CollapsableCellClass(self.master, contentCellClass=self.master.ContentCellClass, CollapsableCellClass=self.master.CollapsableCellClass, contentText=entry1.get(), parentRefrence=self.master.parentRefrence, jsonlocation=self.master.jsonlocation + [entry1.get()],treeLevel=self.master.treeLevel + 1, populateTreeFunc=self.master.populateTreeFunc)
                newCell.grid(column=0, row=self.master.populateCellCount, sticky="ew")
                print(newCell.editingDict)
                    # cell = self.master.CollapsableCell(parent, contentCellClass=self.ContentCell, CollapsableCellClass=self.CollapsableCell, jsonlocation=newJsonLocation, parentRefrence=self, editingDict=parent.editingDict[key], contentText=key, treeLevel=parent.treeLevel + 1, populateTreeFunc=self.populateEditor)
                info_editor.NewCollapsableInfo(newCell, entry1.get())
                customEditingDict = self.master.editingDict
                customEditingDict[entry1.get()] = {}
                newCell.editingDict = customEditingDict[entry1.get()]
                newCell.jsonlocation = self.master.jsonlocation + [entry1.get()]
                toplevel.destroy()
                
            
            if self.master.state == "collapsed":
                self.master.collapseCell()
            
            toplevel = customtkinter.CTkToplevel(self)
            toplevel.title("Add Collapse")
            
            customtkinter.CTkLabel(toplevel, text="Collapsable Name:").grid(column=0, row=0)

            entry1 = customtkinter.CTkEntry(toplevel, placeholder_text="Enter Text...")
            entry1.grid(column=0, row=1)
            
            buttomFrame = customtkinter.CTkFrame(toplevel)
            buttomFrame.grid(column=0, row=2, padx=5, pady=3)
            
            closeButton = customtkinter.CTkButton(buttomFrame, text="Close", command=toplevel.destroy).grid(column=0, row=0, padx=2)
            createButton = customtkinter.CTkButton(buttomFrame, text="Create", command=addCollapse).grid(column=1, row=0, padx=2)
            
            toplevel.after(100, toplevel.lift)
            
        def unselectSelf(self):
            self.logger.addToLog("custom_widgits.py - Content Cell uneselected")
            # self.selectedCellList
            print('Running')
            self.configure(fg_color="transparent")
            
        def selectSelf(self):
            self.logger.addToLog("custom_widgits.py - Content Cell selected")
            self.parentRefrence.selectedCell
            print("Pressed")
            print(self.parentRefrence.selectedCell)
            # self.selectedCellList
            if self.parentRefrence.selectedCell[0] == False:
                self.configure(fg_color="#2288D7")
                self.parentRefrence.selectedCell = [True, self]
            else:
                print(self.parentRefrence.selectedCell[1])
                self.parentRefrence.selectedCell[1].unselectSelf()
                self.configure(fg_color="#2288D7")
                self.parentRefrence.selectedCell = [True, self]

    def populateEditor(self, parent=None, editingDictionary=None, tLevel=0, ranAtRoot=True) -> None:
        self.logger = logger.Logger()
        self.logger.addToLog("custom_widgits.py - Populating editor...")
        if ranAtRoot:
            self.populateCellCount = 0
            parent = self
            for key, value in editingDictionary.items():
                if type(value) is dict:
                    # print("Is A dictioanry")
                    print(value)
                    cell = self.CollapsableCell(parent, contentCellClass=self.ContentCell, CollapsableCellClass=self.CollapsableCell, jsonlocation=[key], editingDict=self.editingDict[key], contentText=key, treeLevel=tLevel, parentRefrence=self, populateTreeFunc=self.populateEditor)
                    self.populateCellCount +=1
                    cell.grid(column=0, row=parent.populateCellCount, sticky="ew")
                else:
                    cell = self.ContentCell(self, keyText=key, jsonlocation=[key], valueText=value, parentRefrence=self, treeLevel=tLevel)
                    cell.grid(column=0, row=self.populateCellCount, sticky="ew")
                    self.populateCellCount +=1
        else:
            parent.populateCellCount +=1
            for key, value in editingDictionary.items():
                if type(value) is dict:
                    # print("Is A dictioanry")
                    newJsonLocation = parent.jsonlocation + [key]
                    # print(parent.editingDict[key])
                    cell = self.CollapsableCell(parent, contentCellClass=self.ContentCell, CollapsableCellClass=self.CollapsableCell, jsonlocation=newJsonLocation, parentRefrence=self, editingDict=parent.editingDict[key], contentText=key, treeLevel=parent.treeLevel + 1, populateTreeFunc=self.populateEditor)
                    cell.grid(column=0, row=parent.populateCellCount, sticky="ew")
                else:
                    newJsonLocation = parent.jsonlocation + [key]
                    cell = self.ContentCell(parent, keyText=key, jsonlocation=newJsonLocation, valueText=value, parentRefrence=self, treeLevel=parent.treeLevel + 1)
                    cell.grid(column=0, row=parent.populateCellCount, sticky="ew")
                parent.populateCellCount +=1

    def updateStoredDict(self, newDict):
        self.logger.addToLog("custom_widgits.py - Updating local dictionary accsess")
        self.editingDict = newDict
        info_editor.jsonDict = self.editingDict
            

        # print(self.winfo_children())
        self.update_idletasks()
                
    def clearEditor(self):
        self.logger.addToLog("custom_widgits.py - Clearing editor...")
        for widget in self.winfo_children():
            widget.destroy()
            
    def populateWithTemp(self):
        self.logger.addToLog("custom_widgits.py - Populating editor with temp dictionary...")
        # info_editor.updateTempDict()
        self.clearEditor()
        self.editingDict = info_editor.updateTempDict()
        # info_editor.updateTempDict()
        self.populateEditor(editingDictionary=self.editingDict, ranAtRoot=True)
        
    def populateWithFilter(self, whitelist):
        self.logger.addToLog("custom_widgits.py - Populating editor with filter dictionary...")
        # info_editor.updateTempDict()
        self.clearEditor()
        self.editingDict = info_editor.createFilterDictionary(whitelist_term=whitelist)
        # info_editor.updateTempDict()
        self.populateEditor(editingDictionary=self.editingDict, ranAtRoot=True)
        
class CtkFilterOptions(customtkinter.CTkToplevel):
    def __init__(self, parent, **kwargs):
        self.logger = logger.Logger()
        self.logger.addToLog("custom_widgits.py - Initializing CtkFilterOptions...")
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.title("Filter Options")
        
        customtkinter.CTkLabel(self, text="Elements to include in filter search:").pack(pady=10, padx=10)
        
        # self.dropdown = customtkinter.BooleanVar()
        # self.label = customtkinter.BooleanVar()
        # self.content = customtkinter.BooleanVar()
        self.filterType = customtkinter.StringVar()
        
        for key, value in filter_management.loadFilterSettings().items():
            if key == "dropdown":
                self.filterType.set('dropdown')
                break
            elif key == "label":
                self.filterType.set('label')
                break
            elif key == "content":
                self.filterType.set('content')
                break
        
        customtkinter.CTkRadioButton(self, text="Dropdown Names", variable=self.filterType, value='dropdown').pack(pady=3, padx=10)
        customtkinter.CTkRadioButton(self, text="Information Labels", variable=self.filterType, value='label').pack(pady=3, padx=10)
        customtkinter.CTkRadioButton(self, text="Information Content", variable=self.filterType, value='content').pack(pady=3, padx=10)
        
        close_button = customtkinter.CTkButton(self, text="Close", command=self.close).pack(pady=10, padx=10)
        
        self.after(100, self.lift)
        
    def close(self):
        print(self.filterType.get())
        
        if self.filterType.get() == "dropdown":
                filter_management.updateFilterSettings(settingName="dropdown", settingValue=True)
                filter_management.updateFilterSettings(settingName="label", settingValue=False)
                filter_management.updateFilterSettings(settingName="content", settingValue=False)
                
        elif self.filterType.get() == "label":
            filter_management.updateFilterSettings(settingName="label", settingValue=True)
            filter_management.updateFilterSettings(settingName="dropdown", settingValue=False)
            filter_management.updateFilterSettings(settingName="content", settingValue=False)
            
        elif self.filterType.get() == "content":
            filter_management.updateFilterSettings(settingName="content", settingValue=True)
            filter_management.updateFilterSettings(settingName="label", settingValue=False)
            filter_management.updateFilterSettings(settingName="dropdown", settingValue=False)
            
        self.logger.addToLog("custom_widgits.py - New filter settings set")
        self.destroy()
        
        
        # self.wait_window()