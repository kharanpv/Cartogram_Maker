import customtkinter as ctk
import random

def random_color():
    colors = ['#E40303','#FF8C00','#FFED00','#008026','#24408E', '#732982']
    return random.choice(colors)

class canvas_frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")  # Create a frame inside the application window

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=40, pady=(20, 0), sticky="nsew")

        self.plus_button = ctk.CTkButton(self, text="+", command=self.on_plus_click, width=40, fg_color="lightgray", text_color="black",
                                 font=("Arial", 30), corner_radius=0, hover_color="darkgray")
        self.plus_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 50), sticky="se")

        self.minus_button = ctk.CTkButton(self, text="-", command=self.on_minus_click, width=40, fg_color="lightgray", text_color="black",
                                 font=("Arial", 30), corner_radius=0, hover_color="darkgray")
        self.minus_button.grid(row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="se")

        self.point_buffer = []  # Buffer to store a pair of points

        self.canvas = ctk.CTkCanvas(self, width=800, height=800, background="white", highlightthickness=0)  # Create a canvas inside the frame
        self.canvas.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")  # Add padding for the canvas
        self.canvas.bind("<Button-1>", self.create_click_event)

    def on_plus_click(self):
        # Handle the plus button click event
        self.canvas.scale("all", 0, 0, 1.1, 1.1)  # Scale by 10%
        print("[DEBUG]: Plus button pressed")

    def on_minus_click(self):
        # Handle the minus button click event
        self.canvas.scale("all", 0, 0, 0.9, 0.9)
        print("[DEBUG]: Minus button pressed")

    # Function to handle the click event
    def create_click_event(self, event):
        self.click_event(event)

    def click_event(self, event):
        x = event.x
        y = event.y

        for i in range(0, len(self.point_buffer) - 1): # Check if the point is close to any of the points in the buffer
            if abs(self.point_buffer[i][0] - x) < 10 and abs(self.point_buffer[i][1] - y) < 10:
                self.point_buffer.append(self.point_buffer[i])
                x1, y1 = self.point_buffer[-2]
                x2, y2 = self.point_buffer[-1]
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
                self.canvas.create_polygon(self.point_buffer,fill=random_color(), width=2)
                self.point_buffer.clear()
                return

        self.point_buffer.append((x, y))
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

        if len(self.point_buffer) >= 2: # If the buffer has atleast 2 points, draw a line
            x1, y1 = self.point_buffer[-2]
            x2, y2 = self.point_buffer[-1]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

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

