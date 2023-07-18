import customtkinter as ctk
import os
from datetime import datetime

class start_frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#EBEBEB")  # Create a frame inside the application window

        # configure the grid layout
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # create button
        self.create_button = ctk.CTkButton(self, text="Create", command=self.on_create_click)
        self.create_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # project list frame
        self.project_list = ctk.CTkFrame(self, fg_color="white")
        self.project_list.grid(row=0, column=1, padx=10, pady=10, sticky="new")

        #configure grid layout for project list
        self.project_list.grid_columnconfigure(0, weight=3)
        self.project_list.grid_columnconfigure(1, weight=2)
        self.project_list.grid_columnconfigure(2, weight=1)
        self.project_list.grid_columnconfigure(3, weight=2)

        # Table headings for the project list
        self.project_name = ctk.CTkLabel(self.project_list, text="Name", text_color="black")
        self.project_name.grid(row=0, column=0, padx=10, pady=(5,0), sticky="nsw")

        self.last_modified = ctk.CTkLabel(self.project_list, text="Last Modified", text_color="black")
        self.last_modified.grid(row=0, column=1, padx=10, pady=(5,0), sticky="nsw")

        self.project_size = ctk.CTkLabel(self.project_list, text="Size", text_color="black")
        self.project_size.grid(row=0, column=2, padx=10, pady=(5,0), sticky="nsw")

        #divider line between table headings and project list
        self.divider = ctk.CTkFrame(self.project_list, fg_color="black", height=1)
        self.divider.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        # the project list is updated on demand
        self.bind("<Configure>", self.display_project_list)
        self.display_project_list()
    
    def get_project_list(self, folder_path):
        project_list = []

        # get the list of projects in the projects folder
        for file in os.listdir(folder_path):
            if file.endswith(".json"):
                project_list.append([file, datetime.fromtimestamp(os.path.getmtime('projects\\' + file)).replace(microsecond=0), 
                                     os.path.getsize('projects\\' + file)])
        
        return project_list 
    
    def display_project_list(self, event=None):
        folder_path = os.path.join("projects")
        project_list = self.get_project_list(folder_path)

        row_num = 2 # starting row number for the project list
        for project in project_list:
            
            # appending the project name, last modified date and size to the project list
            project_name = ctk.CTkLabel(self.project_list, text=project[0], text_color="black")
            project_name.grid(row=row_num, column=0, padx=10, pady=(5,0), sticky="nsw")

            project_last_modified = ctk.CTkLabel(self.project_list, text=project[1], text_color="black")
            project_last_modified.grid(row=row_num, column=1, padx=10, pady=(5,0), sticky="nsw")

            project_size = ctk.CTkLabel(self.project_list, text=project[2], text_color="black")
            project_size.grid(row=row_num, column=2, padx=10, pady=(5,0), sticky="nsw")

            # create a frame for the buttons
            button_frame = ctk.CTkFrame(self.project_list, fg_color="transparent")
            button_frame.grid(row=row_num, column=3, padx=(5,0), pady=(5,0), sticky="nsw")

            #view button
            view_button = ctk.CTkButton(button_frame, text="View", command=lambda: self.on_view_click(project[0]), 
                                        fg_color="transparent", text_color="black", width=30)
            view_button.grid(row=0, column=0, padx=(0,5), pady=(5,0), sticky="nsw")

            #edit button
            edit_button = ctk.CTkButton(button_frame, text="Edit", command=lambda: self.on_edit_click(project[0]), 
                                        fg_color="transparent", text_color="black", width=30)
            edit_button.grid(row=0, column=1, padx=5, pady=(5,0), sticky="nsw")

            #Download button
            download_button = ctk.CTkButton(button_frame, text="Download", command=lambda: self.on_download_click(project[0]), 
                                            fg_color="transparent", text_color="black", width=60)
            download_button.grid(row=0, column=2, padx=(5,0), pady=(5,0), sticky="nsw")

            row_num += 1


    def on_create_click(self): 
        print("[DEBUG]: Create button pressed")

    def on_view_click(self, project_name):
        print("[DEBUG]: View button pressed on project: " + project_name)

    def on_edit_click(self, project_name):
        print("[DEBUG]: Edit button pressed on project: " + project_name)

    def on_download_click(self, project_name):
        print("[DEBUG]: Download button pressed on project: " + project_name)