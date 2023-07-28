import customtkinter as ctk

class ViewFrame(ctk.CTkFrame):
    def __init__(self, master, project_name):
        from .canvas_frame import CanvasFrame

        super().__init__(
            master, fg_color="#EBEBEB"
        ) # Call the parent class constructor

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )

        self.project_name = project_name 

        self.canvas_frame = CanvasFrame(self) # Create a frame inside the application window
        
        self.exit_button = ctk.CTkButton( # Create the Exit button
            self, text="Go Back", command=self.go_back, fg_color="red"
        )
        self.exit_button.grid(row=1, column=0, padx=10, pady=10, sticky="se") # Position the Exit button in the bottom left corner

        self.edit_button = ctk.CTkButton( # Create the Edit button
            self, text="Edit", command=self.create_on_edit(self.project_name)
        )
        self.edit_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw") # Position the Edit button in the bottom right corner

    def go_back(self):
        from .start_frame import StartFrame

        # call main_app to change frame
        self.master.change_frame(StartFrame)

    def create_on_edit(self, name):
        return lambda: self.edit(name)
    
    def edit(self, project_name):
        from .edit_data import EditData

        edit_data_partial = lambda new_master: EditData( # Create the EditData frame
            master=new_master, project_name=self.project_name
        )
        self.master.change_frame(edit_data_partial)

    def set_list_of_polygons(self, structure):
        self.canvas_frame.set_list_of_polygons(structure)
        