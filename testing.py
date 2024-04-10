import overpy
from geopy.geocoders import Nominatim 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter
from PIL import Image, ImageTk
import customtkinter
import requests

# Create a Nominatim geocoder object
geolocator = Nominatim(user_agent="device-locator")

class BuisnessScanner(customtkinter.CTkToplevel):
    def __init__(self, addresses, smartAddCommand, custom_widgit_ref):
        super().__init__()
        self.title("Smart Scan")
        
        def get_amenities_within_radius(latitude, longitude, radius, amenities):
            def distance_between_points(lat1, lon1, lat2, lon2):
                # This function calculates the distance between two points using Haversine formula
                from math import radians, sin, cos, sqrt, atan2

                # Radius of the Earth in km
                R = 6371.0

                # Convert latitude and longitude from degrees to radians
                lat1 = radians(lat1)
                lon1 = radians(lon1)
                lat2 = radians(lat2)
                lon2 = radians(lon2)

                # Calculate the change in coordinates
                dlon = lon2 - lon1
                dlat = lat2 - lat1

                # Apply Haversine formula
                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                # Calculate distance
                distance = R * c
                return distance
            
            api = overpy.Overpass()

            # Define the bounding box based on the radius (this is just an approximation)
            offset = radius / 111.0
            bbox = (latitude - offset, longitude - offset, latitude + offset, longitude + offset)

            # Initialize an empty dictionary to store the results
            results = {}

            for amenity in amenities:
                # Build the query to search for the specified amenity within the bounding box
                query = f"""
                    node["amenity"="{amenity}"]
                        ({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
                    out;
                """

                # Send the query to the Overpass API
                result = api.query(query)

                # Extract relevant information from the query result
                results[amenity] = []
                for node in result.nodes:
                    # print(node.tags)
                    name = node.tags.get("name", "Unknown")
                    lat = float(node.lat)
                    lon = float(node.lon)
                    website = ""
                    for tag in node.tags:
                        # print(tag)
                        if tag == "website":
                            website = node.tags[tag]
                            # print(website)
                    distance = distance_between_points(latitude, longitude, lat, lon)
                    if distance <= radius:
                        if website != "":
                            results[amenity].append({"name": name, "latitude": lat, "longitude": lon, "distance": distance, "website": website})
                        else:
                            results[amenity].append({"name": name, "latitude": lat, "longitude": lon, "distance": distance})
                            
            # print(results)
            return results
        
        def get_address_from_coordinates(lat, lon):
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
            response = requests.get(url)
            data = response.json()
            
            if 'display_name' in data:
                address = data['display_name']
                return address
            else:
                return "Address not found"
            
        def get_checked_values():
            checked_values = []
            
            for var_list in [self.eduVars, self.recVars, self.comVars]:
                for var in var_list:
                    if var.get() != "None":
                        checked_values.append(var.get())
                        
            # print(checked_values)
                
            return checked_values
        
        def set_image(imageName):
            photo = ImageTk.PhotoImage(Image.open(self.addressImages[imageName]))
            return photo
        
        def get_coordinates(address):
            location = geolocator.geocode(address)
            locationTuple = (location.latitude, location.longitude)
            
            return locationTuple
        
        def process_address(address):
            if addressSelector.get() != "None":
                address = addressSelector.get()
            
            new_image = set_image("processing")
            self.addressImage.configure(image=new_image)
            self.addressImage.image = new_image
            
            try:
                locationTuple = get_coordinates(address)
            except:
                # Log the failure --------
                new_image = set_image("address_not_rec")
                self.addressImage.configure(image=new_image)
                self.addressImage.image = new_image
            else:
                organizationList = []
                self.buisnesses = get_amenities_within_radius(locationTuple[0], locationTuple[1], int(self.mileRange.get()), get_checked_values())
                new_image = set_image("address_found")
                self.addressImage.configure(image=new_image)
                self.addressImage.image = new_image
                
                for key, values in self.buisnesses.items():
                    for organization in values:
                        # print(organization['name'])
                        organizationList.append(organization['name'])
                self.orgList.configure(text="\n".join(organizationList))
                
        def smartAdd():
            new_dict = {}
            try:
                for restaurant in self.buisnesses["fast_food"]:
                    if "website" in restaurant:
                        new_dict[restaurant["name"]] = {
                        "Coordinates": {"Latitude": restaurant["latitude"],
                        "Longitude": restaurant["longitude"],},
                        "Distance": str(round(restaurant["distance"], 2)) + " miles",
                        "Address": get_address_from_coordinates(restaurant["latitude"], restaurant["longitude"]),
                        "Website": restaurant["website"]
                    }
                    else:
                        new_dict[restaurant["name"]] = {
                        "Coordinates": {"Latitude": restaurant["latitude"],
                        "Longitude": restaurant["longitude"],},
                        "Distance": str(round(restaurant["distance"], 2)) + " miles",
                        "Address": get_address_from_coordinates(restaurant["latitude"], restaurant["longitude"])
                }
            except: pass
            try:
                for cafe in self.buisnesses["cafe"]:
                    if "website" in cafe:
                        new_dict[cafe["name"]] = {
                        "Coordinates": {"Latitude": cafe["latitude"],
                        "Longitude": cafe["longitude"],},
                        "Distance": str(round(cafe["distance"], 2)) + " miles",
                        "Address": get_address_from_coordinates(cafe["latitude"], cafe["longitude"]),
                        "Website": cafe["website"]
                    }
                    else:
                        new_dict[cafe["name"]] = {
                        "Coordinates": {"Latitude": cafe["latitude"],
                        "Longitude": cafe["longitude"],},
                        "Distance": str(round(cafe["distance"], 2)) + " miles",
                        "Address": get_address_from_coordinates(cafe["latitude"], cafe["longitude"])
                }
            except: pass
            smartAddCommand(new_dict)
            custom_widgit_ref.populateWithTemp()
            messagebox.showinfo(title="Success", message="Smart add successful!")
            self.destroy()

        self.addressImages = {"address_found": "Resources/images/address_found.png", "address_not_rec": "Resources/images/address_not_rec.png", "no_address": "Resources/images/no_address.png", "processing": "Resources/images/processing.png"}

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        addressSearchingFrame = customtkinter.CTkFrame(self)
        addressSearchingFrame.grid(column=0, row=0, sticky="news", padx=10)
        
        amenityFrame = customtkinter.CTkFrame(self)
        amenityFrame.grid(column=0, row=1, sticky="news", padx=10)
        amenityFrame.rowconfigure(0, weight=1)
        
        orginizationViewFrame = customtkinter.CTkFrame(self)
        orginizationViewFrame.grid(column=0, row=2, sticky="news", padx=10, pady=5)
        
        addressFrame = customtkinter.CTkFrame(addressSearchingFrame)
        addressFrame.grid(column=0, row=0)
        
        customtkinter.CTkLabel(addressFrame, text="Enter Address:").grid(column=0, row=0)
        manualAddressEnter = customtkinter.CTkEntry(addressFrame)
        manualAddressEnter.grid(column=0, row=1)

        customtkinter.CTkLabel(addressFrame, text="Select Exsisting Address:").grid(column=0, row=2)
        addressSelector = customtkinter.CTkComboBox(addressFrame, values=addresses, state="readonly")
        addressSelector.grid(column=0, row=3)
        addressSelector.set("None")
        
        customtkinter.CTkLabel(addressFrame, text="Range (miles)").grid(column=0, row=4)
        
        self.mileRange = tk.Spinbox(addressFrame, from_=1, to=30, increment=1)
        self.mileRange.grid(column=0, row=5)
        
        processAddressButton = customtkinter.CTkButton(addressFrame, text="Find Buisnesses", command=lambda: process_address(manualAddressEnter.get())).grid(column=0, row=6)
        
        customimage = set_image("no_address")
        self.addressImage = customtkinter.CTkLabel(addressSearchingFrame, image=customimage, text="", justify="center")
        self.addressImage.grid(row=0,column=1)
        self.addressImage.image = customimage
        addressSearchingFrame.columnconfigure(1, weight=1)
        addressSearchingFrame.rowconfigure(0, weight=1)
        
        
        
        
        amenityEducationFrame = customtkinter.CTkLabel(amenityFrame)
        amenityEducationFrame.grid(column=0, row=0)
        amenityFoodFrame = customtkinter.CTkLabel(amenityFrame)
        amenityFoodFrame.grid(column=1, row=0)
        amenityEntertainmentFrame = customtkinter.CTkLabel(amenityFrame)
        amenityEntertainmentFrame.grid(column=2, row=0)
        
        #Education Buttons
        self.eduVars = [customtkinter.StringVar(), customtkinter.StringVar()]
        for var in self.eduVars:
            var.set("None")
        customtkinter.CTkCheckBox(amenityEducationFrame, text="College", onvalue="college", offvalue="None", variable=self.eduVars[0]).grid(column=0, row=0)
        customtkinter.CTkCheckBox(amenityEducationFrame, text="Library", onvalue="library", offvalue="None", variable=self.eduVars[1]).grid(column=0, row=1)
        print(self.eduVars[0].get())
        
        #Recreation Buttons
        self.recVars = [customtkinter.StringVar(), customtkinter.StringVar()]
        for var in self.recVars:
            var.set("None")
        box = customtkinter.CTkCheckBox(amenityFoodFrame, text="Cafe", onvalue="cafe", offvalue="None", variable=self.recVars[0]).grid(column=0, row=0)
        customtkinter.CTkCheckBox(amenityFoodFrame, text="Fast Food", onvalue="fast_food", offvalue="None", variable=self.recVars[1]).grid(column=0, row=1)
        
        #Community Buttons
        self.comVars = [customtkinter.StringVar(), customtkinter.StringVar()]
        for var in self.comVars:
            var.set("None")
        customtkinter.CTkCheckBox(amenityEntertainmentFrame, text="Arts Center", onvalue="arts_centre", offvalue="None", variable=self.comVars[0]).grid(column=0, row=0)
        customtkinter.CTkCheckBox(amenityEntertainmentFrame, text="Community Center", onvalue="community_centre", offvalue="None", variable=self.comVars[1]).grid(column=0, row=1)
        
        
        orginizationViewFrame.rowconfigure(0, weight=1)
        orginizationViewFrame.columnconfigure(0, weight=1)
        
        # canvas = tk.Canvas(orginizationViewFrame, width=250, height=150)
        # scrollbar = ttk.Scrollbar(orginizationViewFrame, command=canvas.yview)
        # scrollbar.grid(row=0, column=1, sticky="ns")
        # canvas.grid(row=0, column=0, sticky="news")
        # listFrame = tk.Frame(canvas)
        # listFrame.columnconfigure(0, weight=1)
        # listFrame.rowconfigure(0, weight=1)
        # canvas.create_window((0,0), window=listFrame, anchor="nw")
        # listFrame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))
        
        listFrame = customtkinter.CTkScrollableFrame(orginizationViewFrame)
        listFrame.grid(row=0, column=0, sticky="news")
        
        self.orgList = customtkinter.CTkLabel(listFrame, text="Address not processed. Enter an address above.")
        self.orgList.grid(row=1, column=0)
        
        customtkinter.CTkButton(self,text="Send to editor", command=smartAdd).grid(column=0, row=3, sticky="news", padx=10, pady=5)
        
        self.after(200, self.lift)
        
        

# root = tk.Tk()

# addresses = ["691 E Denim Trl", "32375 N Gantzel Rd"]

# BuisnessScanner(root, addresses=addresses).grid(column=0, row=0)

# root.mainloop()
