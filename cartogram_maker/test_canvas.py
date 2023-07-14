import customtkinter as ctk

# Function to handle the click event
def create_click_event(canvas):
    point_buffer = [] # Buffer to store a pair of points

    def click_event(e):
        x = e.x
        y = e.y

        for i in range(len(point_buffer)): # Check if the point is close to any of the points in the buffer
            if abs(point_buffer[i][0] - x) < 5 and abs(point_buffer[i][1] - y) < 5:
                point_buffer.append(point_buffer[i])
                x1, y1 = point_buffer[-2]
                x2, y2 = point_buffer[-1]
                canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

                point_buffer.clear()
                return

        point_buffer.append((x, y))
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

        if len(point_buffer) >= 2: # If the buffer has atleast 2 points, draw a line
            x1, y1 = point_buffer[-2]
            x2, y2 = point_buffer[-1]
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    return click_event


def main():
    app = ctk.CTk()  # Create the application window
    app.geometry("800x600")  # Set the window size
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    print("[DEBUG]: created app")

    frame = ctk.CTkFrame(app)  # Create a frame inside the application window
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)  
    frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew") 

    print("[DEBUG]: created frame")

    canvas = ctk.CTkCanvas(frame, width=800, height=800)  # Create a canvas inside the frame
    canvas.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")  # Add padding for the canvas

    canvas.bind("<Button-1>", create_click_event(canvas=canvas))

    print("[DEBUG]: created canvas and bound on click event")

    app.mainloop()  # Start the application's main event loop
