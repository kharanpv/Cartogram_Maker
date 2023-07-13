import customtkinter as ctk


def create_click_event(canvas):
    def click_event(e):
        x = e.x
        y = e.y
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")

    return click_event


def main():
    app = ctk.CTk()
    app.geometry("500x400")
    app.grid_columnconfigure(0, weight=1)

    print("[DEBUG]: created app")

    frame = ctk.CTkFrame(app)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

    print("[DEBUG]: created frame")

    canvas = ctk.CTkCanvas(frame, width=200, height=500)
    canvas.grid(row=0, column=0)
    canvas.bind("<Button-1>", create_click_event(canvas=canvas))

    print("[DEBUG]: created canvas and bound on click event")

    app.mainloop()
