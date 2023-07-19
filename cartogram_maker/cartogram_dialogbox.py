import customtkinter as ctk
from .creation_tool import creation_tool

class cartogram_dialogbox(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        # Frame for the dialog box
        self.frame = ctk.CTkFrame(self, fg_color="#EBEBEB")
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

        # Label that says "Upload JSON file"
        self.upload_label = ctk.CTkLabel(
            self.frame, text="Upload JSON file", text_color="black")
        self.upload_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsw")

        # Button that says "Browse"
        self.browse_button = ctk.CTkButton(
            self.frame, text="Browse", command=self.on_browse_click)
        self.browse_button.grid(row=1, column=0, padx=10, pady=5, sticky="nsw")
        
        # Label that says "Or"
        self.or_label = ctk.CTkLabel(
            self.frame, text="OR", text_color="gray")
        self.or_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsw")
        
        # Button that says "Create with Creation Tool"
        self.create_button = ctk.CTkButton(
            self.frame, text="Create with Creation Tool", command=self.on_create_click, fg_color="#FFEF00", text_color="black")
        self.create_button.grid(row=3, column=0, padx=10, pady=5, sticky="nsw")

    def on_browse_click(self):
        print("[DEBUG]: Browse button pressed")

    def on_create_click(self):
        self.destroy()
        self.master.master.change_frame(creation_tool)

        print("[DEBUG]: Create button pressed")