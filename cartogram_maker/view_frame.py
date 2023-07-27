import customtkinter as ctk
from .point import Point

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

        print("[DEBUG]: Go Back button pressed")

    def create_on_edit(self, name):
        return lambda: self.edit(name)
    
    def edit(self, project_name):
        from .edit_data import EditData

        edit_data_partial = lambda new_master: EditData( # Create the EditData frame
            master=new_master, project_name=self.project_name
        )
        self.master.change_frame(edit_data_partial)

        print("[DEBUG]: Edit button pressed")

    def set_list_of_polygons(self, structure):
        # Temporary function to draw all points as ovals on the canvas and return as a `Point`
        def func(x, y):
            # draws as oval on canvas
            self.canvas_frame.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
            # converts to the `Point` `NamedTuple`
            return Point(x, y)
        
        for _, substructure in structure.items(): 
            # convert the vertex buffer (List[List[int]] -> List[Point])
            # also draw to canvas with `func`
            point_buffer = [func(x, y) for x, y in substructure['vertices']]
            
            # zip(a, a[1:]) -> [(a[0], a[1]), (a[1], a[2]), ..., (a[n - 1], a[n])]
            for (x1, y1), (x2, y2) in zip(point_buffer, point_buffer[1:]):
                print(f"{x1}, {y1} -> {x2}, {y2}")
                # creating lines from every value in the point buffer
                self.canvas_frame.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

            # creating a new polygon and appending it to the polygon list
            # storing the polygon id with the walrus operator (PEP 572)
            self.canvas_frame.polygon_list.append(
                (
                    id:=self.canvas_frame.canvas.create_polygon(
                        point_buffer, fill=substructure['color'], width=2
                    ),
                    point_buffer[:],
                )
            )
            # assigning the color associated to the id
            self.canvas_frame.colors[id] = substructure['color']
            # assigning the weight associate to the id
            self.canvas_frame.weights[id] = substructure['weight']
        