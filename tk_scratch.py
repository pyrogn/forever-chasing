# import tkinter as tk


# def onKeyPress(event):
#     text.insert("end", "You pressed %s|%s\n" % (event.char, event.keysym))
#
#
# root = tk.Tk()
# root.geometry("300x200")
# text = tk.Text(root, background="black", foreground="white", font=("Comic Sans MS", 12))
# text.pack()
# root.bind("<KeyPress>", onKeyPress)
# root.mainloop()

import numpy as np
import tkinter as tk

acc = 0.3
m = 100
res = 5  # whatever it is


class MoveCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.v = np.array([0, 0])
        self.acc_direction = np.array([0, 0])

        self.dx = 0
        self.dy = 0

        self.box = self.create_oval(0, 0, 10, 10, fill="black")

        self.dt = 10
        self.tick()

    def tick(self):
        print(self.acc_direction, np.round(self.v, 2))
        f_forward = m * acc * self.acc_direction
        f_resistance = res * self.v
        f_diff = f_forward - f_resistance
        self.v = self.v + f_diff / m
        self.dx, self.dy = self.v

        self.move(self.box, self.dx, self.dy)
        # self.acc_direction = np.array([0, 0])
        self.after(self.dt, self.tick)

    def change_heading(self, dx, dy):
        self.acc_direction = np.array([dx, dy])
        self.dx = dx
        self.dy = dy


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")

    cvs = MoveCanvas(root)
    cvs.pack(fill="both", expand=True)

    ds = 10

    root.bind("<KeyPress-Left>", lambda _: cvs.change_heading(-1, 0))
    root.bind("<KeyPress-Right>", lambda _: cvs.change_heading(1, 0))
    root.bind("<KeyPress-Up>", lambda _: cvs.change_heading(0, -1))
    root.bind("<KeyPress-Down>", lambda _: cvs.change_heading(0, 1))
    root.bind_all("<KeyRelease-Left>", lambda _: cvs.change_heading(0, 0))
    root.bind_all("<KeyRelease-Right>", lambda _: cvs.change_heading(0, 0))
    root.bind_all("<KeyRelease-Up>", lambda _: cvs.change_heading(0, 0))
    root.bind_all("<KeyRelease-Down>", lambda _: cvs.change_heading(0, 0))

    root.mainloop()


# brew install python-tk # for MacOS
# import tkinter as tk  # either in python 2 or in python 3
#
#
# def event_handle(event):
#     # Replace the window's title with event.type: input key
#     root.title("{}: {}".format(str(event.type), event.keysym))
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     event_sequence = "<KeyPress>"
#     root.bind(event_sequence, event_handle)
#     root.bind("<KeyRelease>", event_handle)
#     root.mainloop()
