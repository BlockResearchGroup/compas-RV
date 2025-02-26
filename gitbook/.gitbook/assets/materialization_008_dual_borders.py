
#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.datastructures import Mesh
from compas.itertools import pairwise
from compas.geometry import Cylinder, Frame, Plane
from compas.scene import Scene
from compas import json_dump


def break_boundary(mesh: Mesh, breakpoints: list[int]) -> tuple[list[list[int]], list[int]]:
    boundary: list[int] = mesh.vertices_on_boundaries()[0]
    if boundary[0] == boundary[-1]:
        del boundary[-1]

    breakpoints = sorted(breakpoints, key=lambda s: boundary.index(s))

    start = boundary.index(breakpoints[0])
    boundary = boundary[start:] + boundary[:start]

    borders = []
    for a, b in pairwise(breakpoints):
        start = boundary.index(a)
        end = boundary.index(b)
        borders.append(boundary[start : end + 1])
    borders.append(boundary[end:] + boundary[:1])

    return borders, breakpoints


# =============================================================================
# Load data
# =============================================================================


IFILE = pathlib.Path(__file__).parent / "007_mesh.json"
dual = compas.json_load(IFILE)

# =============================================================================
# Dual: Borders
# =============================================================================

corners = list(dual.vertices_where(is_corner=True))
borders, corners = break_boundary(dual, corners)

lines = []
for border in borders:
    if len(border) < 5:
        dual.vertices_attribute(name="is_support", value=True)
        for edge in pairwise(border):
            dual.edge_attribute(edge, name="is_support", value=True)
            lines.append(dual.edge_line(edge))


# =============================================================================
# Serialize
# =============================================================================

json_dump(dual, pathlib.Path(__file__).parent / "008_mesh.json")

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(dual)
for line in lines:
    plane = Plane(line.midpoint, line.direction)
    frame = Frame.from_plane(plane)
    cylinder = Cylinder(10, line.length, frame)
    scene.add(cylinder, color=(0, 255, 0))
scene.draw()

