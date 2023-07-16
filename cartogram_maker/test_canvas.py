import customtkinter as ctk

# Function to handle the click event
def create_click_event(canvas):
    point_buffer = [] # Buffer to store a pair of points

    def click_event(e):
        x = e.x
        y = e.y

        for i in range(0, len(point_buffer) - 1): # Check if the point is close to any of the points in the buffer
            if abs(point_buffer[i][0] - x) < 10 and abs(point_buffer[i][1] - y) < 10:
                point_buffer.append(point_buffer[i])
                x1, y1 = point_buffer[-2]
                x2, y2 = point_buffer[-1]
                canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
                canvas.create_polygon(point_buffer,fill='green', width=2)
                point_buffer.clear()
                return

        point_buffer.append((x, y))
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

        if len(point_buffer) >= 2: # If the buffer has atleast 2 points, draw a line
            x1, y1 = point_buffer[-2]
            x2, y2 = point_buffer[-1]
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    return click_event

def on_plus_click(canvas): #placeholder for future Plus button functionality
    canvas.scale("all", 0, 0, 1.1, 1.1)     # Scale by 10%
    print("[DEBUG]: Plus button pressed")

def on_minus_click(canvas): #placeholder for future Minus button functionality
    canvas.scale("all", 0, 0, 0.9, 0.9)
    print("[DEBUG]: Minus button pressed")

def on_button_release(event): #placeholder for future Left mouse button functionality
    print("[DEBUG]: Left mouse button released")

def generate(): #placeholder for future Generate button functionality
    
    print("[DEBUG]: Generate button pressed")

def go_back(): #placeholder for future Go Back button functionality

    print("[DEBUG]: Go Back button pressed")

def start_drag(event, canvas): # Place holder for dragging around functionality

    print("[DEBUG]: ")

def drag(event, canvas):

    print("[DEBUG]: ")

def main():
    app = ctk.CTk()  # Create the application window
    app.title("Cartogram Maker") # Add title to this app
    app.geometry("800x600")  # Set the window size
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=0)

    print("[DEBUG]: created app")

    frame = ctk.CTkFrame(app, fg_color="white")  # Create a frame inside the application window
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_rowconfigure(0, weight=1)  
    frame.grid(row=0, column=0, padx=40, pady=(20,0), sticky="nsew") 

    print("[DEBUG]: created frame")

    canvas = ctk.CTkCanvas(frame, width=800, height=800, background="white", highlightthickness=0)  # Create a canvas inside the frame
    canvas.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")  # Add padding for the canvas

    canvas.bind("<Button-1>", create_click_event(canvas=canvas))
    # button.bind("<ButtonRelease-1>", create_)

    print("[DEBUG]: created canvas and bound on click event")

    button = ctk.CTkButton(app, text="Generate", command=generate)  # Create the Generate button
    button.grid(row=1, column=0, padx=10, pady=10, sticky="se")  # Position the button in the bottom right corner

    print("[DEBUG]: created Generate button")

    exit_button = ctk.CTkButton(app, text="Go Back", command=go_back, fg_color="red")  # Create the Exit button
    exit_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")  # Position the Exit button in the bottom left corner

    print("[DEBUG]: created Go Back button")

    plus_button = ctk.CTkButton(frame, text="+", command=lambda: on_plus_click(canvas), width=40, fg_color="lightgray", text_color="black",
                                 font=("Arial", 30), corner_radius=0, hover_color="darkgray")
    plus_button.grid(row=0, column=1, padx=(0, 5), pady=(0,50), sticky="se")

    minus_button = ctk.CTkButton(frame, text="-", command=lambda: on_plus_click(canvas), width=40, fg_color="lightgray", text_color="black",
                                 font=("Arial", 30), corner_radius=0, hover_color="darkgray")
    minus_button.grid(row=0, column=1, padx=(0,5), pady=(0,5), sticky="se")

    print("[DEBUG]: created Plus and Minus buttons")


    app.mainloop()  # Start the application's main event loop