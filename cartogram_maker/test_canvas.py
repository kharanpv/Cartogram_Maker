import customtkinter as ctk
import random
from .canvas_frame import canvas_frame

class main_app(ctk.CTk):
    def __init__(self):
        super().__init__() # Call the parent class constructor

        self.title('Cartogram Maker')
        self.geometry('800x600')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)   

        self.frame = canvas_frame(self) # Create a frame inside the application window

        self.generate_button = ctk.CTkButton(self, text="Generate", command=self.generate)  # Create the Generate button
        self.generate_button.grid(row=1, column=0, padx=10, pady=10, sticky="se")  # Position the button in the bottom right corner

        self.exit_button = ctk.CTkButton(self, text="Go Back", command=self.go_back, fg_color="red")  # Create the Exit button
        self.exit_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")  # Position the Exit button in the bottom left corner

    def generate(self): #placeholder for future Generate button functionality
        
        print("[DEBUG]: Generate button pressed")

    def go_back(self): #placeholder for future Go Back button functionality

        print("[DEBUG]: Go Back button pressed")

    def drag(event, canvas): # Drag around the canvas when zooming in
        # canvas.scan_dragto(event.x, event.y, gain=1)
        print("[DEBUG]: Dragging the canvas")


def main():

    app = main_app()
    app.mainloop()

