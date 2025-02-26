
#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.scene import Scene
from scipy.interpolate import griddata
from compas import json_dump
from compas.geometry import Sphere

# =============================================================================
# Load data
# =============================================================================

IFILE = pathlib.Path(__file__).parent / "001_mesh.json"
mesh = compas.json_load(IFILE)

IFILE = pathlib.Path(__file__).parent / "008_mesh.json"
dual = compas.json_load(IFILE)

# =============================================================================
# Blocks: Thickness interpolation griddata
# =============================================================================

points = []
values = []

supports_by_height = sorted(mesh.attributes["supports"], key=lambda v: mesh.vertex_attribute(v, "z"))

for support in supports_by_height[:4]:
    points.append(mesh.vertex_attributes(support, "xy"))
    values.append(30)

for support in supports_by_height[4:]:
    points.append(mesh.vertex_attributes(support, "xy"))
    values.append(20)

for border in mesh.attributes["borders"]:
    if len(border) > 4:
        midspan = border[len(border) // 2]
        points.append(mesh.vertex_attributes(midspan, "xy"))
        values.append(15)

vertices_by_height = sorted(mesh.vertices(), key=lambda v: mesh.vertex_attribute(v, "z"))

for vertex in vertices_by_height[-5:]:
    points.append(mesh.vertex_attributes(vertex, "xy"))
    values.append(10)

# =============================================================================
# Blocks: Thickness interpolation sampling
# =============================================================================

samples = dual.vertices_attributes("xy")
thickness = griddata(points, values, samples)

points = []
weights = []
for vertex, t in zip(dual.vertices(), thickness):
    dual.vertex_attribute(vertex, "thickness", t)
    points.append(dual.vertex_point(vertex))
    weights.append(t)


# =============================================================================
# Serialize
# =============================================================================

json_dump(dual, pathlib.Path(__file__).parent / "009_mesh.json")

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(dual)
for idx, point in enumerate(points):
    print(weights[idx] / 2)
    sphere = Sphere(point=point, radius=weights[idx] / 2)
    scene.add(sphere, color=(255, 0, 0))
scene.draw()

