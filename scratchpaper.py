import numpy as np
from pathlib import Path
import pickle


def make_line(p0, p1, width=0.05, start_color=(0.0, 1.0, 0.0, 1.0), end_color=(0.0, 0.0, 1.0, 1.0)):
    direction = p1 - p0
    direction = direction / (direction ** 2).sum() ** 0.5
    normal = direction[::-1] * np.array([-1, 1])
    pad = 3 * width
    u0 = p0 - pad * normal - pad * direction
    v0 = p0 + pad * normal - pad * direction
    u1 = p1 - pad * normal + pad * direction
    v1 = p1 + pad * normal + pad * direction
    
    return [
        [
            # x_box, y_box, x_ref, y_refred, green, blue, alpha
            *u0, *p0, *p1 ,width, *start_color, *end_color,
            *v0, *p0, *p1 ,width, *start_color, *end_color,
            *u1, *p0, *p1 ,width, *start_color, *end_color,
        ],
        [
            # x_box, y_box, x_ref, y_refred, green, blue, alpha
            *u1, *p0, *p1, width, *start_color, *end_color,
            *v1, *p0, *p1, width, *start_color, *end_color,
            *v0, *p0, *p1, width, *start_color, *end_color,
        ],
    ]

def make_point(p, margin=0.1):
    corners = []
    for i in range(3):
        corner_coords = p + 3 * margin * circle_coords(i, 3)
        corner = [*corner_coords, margin, *p]
        corners.extend(corner)
    return corners

def random_positions(n):
    positions = []
    for _ in range(n):
        positions.extend(make_point(np.random.randn(2)))
    return positions

def _color(i, n):
    x = _idx_to_angle(i, n)
    return np.array([0.2, 0.5 * (1 + np.cos(x)), 0.5 * (1 + np.sin(x)), 1.0])

def _idx_to_angle(i, n):
    return 2 * np.pi * i / n

def distance_color(points):
    distances = ((points[1:] - points[:-1]) ** 2).sum(axis=1) ** 0.5
    distance_travesed = distances.cumsum()
    D = distances.sum()
    colors = [_color(0,D), *[_color(dt, D) for dt in distance_travesed]]
    return colors

def circle_coords(i, n):
    x = _idx_to_angle(i, n)
    return np.array([np.cos(x), np.sin(x)])

def random_route(n, width=0.01):
    points = 1 - 2 * np.random.rand(n + 1, 2)
    colors = distance_color(points)
    lines = []
    for i, (p1, p0) in enumerate(zip(points[1:], points[:-1])):
        line = make_line(
            p0,
            p1,
            start_color=colors[i],
            end_color=colors[i+1],
            width=width,
        )
        lines.extend(line)
    return lines

def create_circle(n):
    lines = []
    for i in range(n):
        line = make_line(
            circle_coords(i, n),
            circle_coords(i+1, n),
            start_color=_color(i, n),
            end_color=_color(i+1, n),
            width=0.05,
        )
        lines.extend(line)
    return lines


if __name__ == '__main__':
    trace_vertices = create_circle(700)
    # trace_vertices = random_route(170, width=0.005)
    position_vertices = random_positions(117)

    vertices = [trace_vertices, position_vertices]
    with open(Path(__file__).parent / "renderer/vertices/vertices.pkl", "wb") as f:
        pickle.dump(vertices, f)
