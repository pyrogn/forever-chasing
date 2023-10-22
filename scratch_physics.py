import numpy as np

acc = 4
m = 10
res = 1  # whatever it is

time_points = 100
v = np.array([0, 0])
coord = np.array([0, 0])
acc_direction = np.array([1, 0])
coords = []
for t in range(time_points):
    if t == 10:
        acc_direction = np.array([0, 1])
    if t == 30:
        acc_direction = np.array([0, -1])
    if t == 50:
        acc_direction = np.array([0, 0])
    f_inertia = m * v / 1
    f_forward = m * acc * acc_direction
    f_resistance = res * v
    f_diff = f_forward - f_resistance
    # print(v/MASS, f_forward, f_resistance, f_diff)

    coord = coord + v * 1
    coords.append(coord)
    v = v + f_diff / m

    coord, v, f_forward, f_resistance, f_diff, f_inertia = map(
        lambda x: np.round(x, 2), [coord, v, f_forward, f_resistance, f_diff, f_inertia]
    )
    print(
        f"s: {coord}, v: {v}, ff: {f_forward}, "
        f"fr: {f_resistance}, f_diff: {f_diff}, "
        f"v mag: {np.linalg.norm(v):.2f}"
        # f'inertia: {f_inertia}'
    )

# x, y = np.array(coords).T
# plt.scatter(x=x, y=y, linewidths=.0001)
