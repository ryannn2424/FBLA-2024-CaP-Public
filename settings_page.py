import customtkinter
import settings_management
import subprocess
import os


class SettingsPage(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Settings")
        self.geometry("500x300")
        self.resizable(False, False)
        
        self.after(200, self.lift)
        
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=99)
        
        switchingFrame = customtkinter.CTkFrame(self)
        switchingFrame.grid(column=0, row=0, sticky="nsew")
        switchingFrame.columnconfigure(0, weight=1)
        switchingFrame.columnconfigure(1, weight=1)
        switchingFrame.columnconfigure(2, weight=1)
        
        customtkinter.CTkButton(switchingFrame, text="Theming", command=lambda: switchFrame("Theming")).grid(column=0, row=0, sticky="nsew")
        customtkinter.CTkButton(switchingFrame, text="Logging", command=lambda: switchFrame("Logging")).grid(column=1, row=0, sticky="nsew")
        customtkinter.CTkButton(switchingFrame, text="About", command=lambda: switchFrame("About")).grid(column=2, row=0, sticky="nsew")
        
        def switchFrame(frameName):
            if frameName == "Theming":
                themingFrame = ThemingFrame(self)
                themingFrame.grid(column=0, row=1, sticky="nsew")
                
            elif frameName == "Logging":
                loggingFrame = LoggingFrame(self)
                loggingFrame.grid(column=0, row=1, sticky="nsew")
                
            elif frameName == "About":
                aboutFrame = AboutFrame(self)
                aboutFrame.grid(column=0, row=1, sticky="nsew")
        
        class ThemingFrame(customtkinter.CTkFrame):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                self.grid(column=0, row=1, sticky="nsew")
                
                self.themeMode = customtkinter.StringVar()
                self.themeMode.set("light")
                def changeTheme():
                    if self.themeMode.get() == "light":
                        customtkinter.set_appearance_mode("light")
                        settings_management.change_setting("Theme", "light")
                    elif self.themeMode.get() == "dark":
                        customtkinter.set_appearance_mode("dark")
                        settings_management.change_setting("Theme", "dark")
                    self.after(1000, self.lift())
                
                # Title
                customtkinter.CTkLabel(self, text="Theming:", font=("Arial", 17)).grid(column=0, row=0, sticky="nsew")
                
                # Mode options
                customtkinter.CTkLabel(self, text="Mode:", font=("Arial", 14)).grid(column=0, row=1, sticky="nsew")
                
                customtkinter.CTkRadioButton(self, text="Light", variable=self.themeMode, value="light", command=changeTheme).grid(column=0, row=2, sticky="nsew", padx=10)
                customtkinter.CTkRadioButton(self, text="Dark", variable=self.themeMode, value="dark",  command=changeTheme).grid(column=1, row=2, sticky="nsew", padx=10)
                
                
        
        class LoggingFrame(customtkinter.CTkFrame):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                self.grid(column=0, row=1, sticky="nsew")
                
                # Title
                customtkinter.CTkLabel(self, text="Logging", font=("Arial", 20)).grid(column=0, row=0, sticky="nsew")
                self.rowconfigure(1, weight=1)
                self.columnconfigure(0, weight=1)
                
                logFrame = customtkinter.CTkFrame(self)
                logFrame.grid(column=0, row=1, sticky="nsew")
                
                fileCount = 0
                files = [f for f in os.listdir('./Logs') if os.path.isfile(os.path.join('./Logs', f))]
                for file in files:
                    customtkinter.CTkLabel(logFrame, text=file).grid(column=0, row=fileCount, sticky="nsew")
                    fileCount += 1
                    
                customtkinter.CTkButton(self, text="Open Log Folder", command=lambda: subprocess.Popen(['xdg-open', './Logs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)).grid(column=0, row=2, sticky="nsew", padx=4, pady=2)
                    
                
                
        
        class AboutFrame(customtkinter.CTkFrame):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                self.grid(column=0, row=1, sticky="nsew")
                self.columnconfigure(0, weight=1)
                self.rowconfigure(1, weight=1)
                self.rowconfigure(2, weight=1)
                self.rowconfigure(3, weight=1)
                # Title
                customtkinter.CTkLabel(self, text="About", font=("Arial", 20)).grid(column=0, row=0, sticky="nsew")
                customtkinter.CTkLabel(self, text="Infollect", font=("Arial", 15)).grid(column=0, row=1, sticky="nsew")
                customtkinter.CTkLabel(self, text="By Ryan, Justin, & Aiden", font=("Arial", 15)).grid(column=0, row=2, sticky="nsew")
                customtkinter.CTkLabel(self, text="FBLA 2024", font=("Arial", 15)).grid(column=0, row=3, sticky="nsew")
                
                
        ThemingFrame(self).grid(column=0, row=1, sticky="nsew")
                
    