import numpy as np
import tkinter as tk

acc = 0.3
m = 100
res = 5  # whatever it is


class MoveCanvas:
    def __init__(self, canvas):
        # super().__init__(*args, **kwargs)
        self.canvas = canvas

        self.v = np.array([0, 0])
        self.acc_direction = np.array([0, 0])

        self.dx = 100
        self.dy = 100

        self.box = self.canvas.create_oval(1, 1, 10, 10, fill="black")
        self.canvas.move(self.box, self.dx, self.dy)

        self.dt = 50
        self.tick()

    def tick(self):
        f_forward = m * acc * self.acc_direction
        f_resistance = res * self.v
        f_diff = f_forward - f_resistance
        self.v = self.v + f_diff / m
        self.dx, self.dy = self.v

        # print(
        #     self.acc_direction,
        #     np.round(f_forward, 2),
        #     np.round(f_resistance, 2),
        #     np.round(f_diff, 2),
        #     np.round(self.v, 2),
        # )

        self.canvas.move(self.box, self.dx, -self.dy)
        self.canvas.after(self.dt, self.tick)

    def change_heading(self, dx, dy):
        self.acc_direction = np.array([dx, dy])
        self.dx = dx
        self.dy = dy


class Bot:
    def __init__(self, chase_to, canvas):
        self.canvas = canvas
        self.target = chase_to
        # x1, y1, x2, y2 = self.coords(self.target)

        self.v = np.array([0, 0])
        self.acc_direction = np.array([0, 0])

        self.dx = 10
        self.dy = 10

        self.box = self.canvas.create_oval(1, 1, 10, 10, fill="red")
        self.canvas.move(self.box, self.dx, self.dy)

        self.dt = 50
        self.tick()

    def tick(self):
        x1, y1, x2, y2 = self.canvas.coords(self.box)
        x1t, y1t, x2t, y2t = self.canvas.coords(self.target.box)
        vec_move = np.array([x1t, y1t]) - np.array([x1, y1])
        vec_move = vec_move / np.linalg.norm(vec_move)
        self.acc_direction = vec_move
        f_forward = m * acc * self.acc_direction
        f_resistance = res * self.v
        f_diff = f_forward - f_resistance
        self.v = self.v + f_diff / m
        self.dx, self.dy = self.v

        self.canvas.move(self.box, self.dx, self.dy)  # don't know why y negative
        self.canvas.after(self.dt, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, bg="black", width=400, height=400)
    canvas.pack(fill="both", expand=True)

    cvs = MoveCanvas(canvas)
    bot = Bot(canvas=canvas, chase_to=cvs)

    root.bind("<KeyPress-Left>", lambda _: cvs.change_heading(-1, 0))
    root.bind("<KeyPress-Right>", lambda _: cvs.change_heading(1, 0))
    root.bind("<KeyPress-Up>", lambda _: cvs.change_heading(0, 1))
    root.bind("<KeyPress-Down>", lambda _: cvs.change_heading(0, -1))
    root.bind_all("<KeyRelease>", lambda _: cvs.change_heading(0, 0))

    root.mainloop()
