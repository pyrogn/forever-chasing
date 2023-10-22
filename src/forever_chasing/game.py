import numpy as np
import tkinter as tk
import enum

# Environmental parameters
ACCELERATION = 0.3
MASS = 100
RESISTANCE_COEF = 5
TICK_MS = 50


class MoveDirection(enum.Enum):
    LEFT = -1, 0
    RIGHT = 1, 0
    UP = 0, -1
    DOWN = 0, 1


class Circle:
    def __init__(
        self,
        canvas: tk.Canvas,
        init_coord=(0, 0),
        size=10,
        fill_color="black",
    ):
        self.canvas = canvas
        self.acc_direction = np.array([0, 0])
        self.speed = np.array([0, 0])
        self.circle = self.canvas.create_oval(
            1, 1, size, size, fill=fill_color
        )  # or zeros in first two coordinates?
        self.canvas.move(self.circle, *init_coord)
        self.move()

    def get_coord(self):
        """Average coordinate of object"""
        x0, y0, x1, y1 = self.canvas.coords(self.circle)
        x = (x0 + x1) / 2
        y = (y0 + y1) / 2
        return np.array([x, y])

    @staticmethod
    def make_step(acc_direction, speed):
        """Returns new speed which is equal of moving"""
        f_forward = MASS * ACCELERATION * acc_direction
        f_resistance = RESISTANCE_COEF * speed
        f_diff = f_forward - f_resistance
        new_speed = speed + f_diff / MASS
        # dx, dy = new_speed
        # maybe we should move with old speed and calc new speed
        return new_speed

    def move(self):
        self.speed = self.make_step(self.acc_direction, self.speed)
        self.speed = self.cap_speed(self.speed)
        self.canvas.move(self.circle, *self.speed)
        self.canvas.after(TICK_MS, self.move)

    def change_acceleration_direction(self, direction) -> None:
        self.acc_direction = np.array(direction.value)

    def stop_acceleration(self) -> None:
        self.acc_direction = np.array([0, 0])

    def cap_speed(self, speed: np.array):
        lower_bound = 0.05  # to stop wiggling indefinitely
        upper_bound = 100
        speed[np.abs(speed) < lower_bound] = 0
        speed[np.abs(speed) > upper_bound] = upper_bound
        return speed


def is_collision_circles(circle1, circle2) -> bool:
    """Should appreciate borders of objects"""
    return False


def direction_to_target(circle_from: Circle, circle_to: Circle):
    """Vector with length of 1"""
    x1, y1 = circle_from.get_coord()
    x1t, y1t = circle_to.get_coord()
    vec_move = np.array([x1t, y1t]) - np.array([x1, y1])
    vec_move = vec_move / np.linalg.norm(vec_move)
    return vec_move


class CircleBot(Circle):
    """Might be poor design"""

    def __init__(self, target, *args, **kwargs):
        self.target = target
        super().__init__(*args, **kwargs)

    def move(self):
        self.acc_direction = direction_to_target(self, self.target)
        super().move()


if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, bg="black", width=400, height=400)
    canvas.pack(fill="both", expand=True)

    cvs = Circle(canvas, init_coord=(200, 200))
    bot = CircleBot(target=cvs, canvas=canvas, fill_color="red", init_coord=(10, 10))

    def move_fn(en):
        return lambda _: cvs.change_acceleration_direction(en)

    root.bind("<KeyPress-Left>", move_fn(MoveDirection.LEFT))
    root.bind("<KeyPress-Right>", move_fn(MoveDirection.RIGHT))
    root.bind("<KeyPress-Up>", move_fn(MoveDirection.UP))
    root.bind("<KeyPress-Down>", move_fn(MoveDirection.DOWN))
    root.bind_all("<KeyRelease>", lambda _: cvs.stop_acceleration())

    root.mainloop()
