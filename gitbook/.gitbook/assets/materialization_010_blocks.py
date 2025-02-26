
#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Polygon
from compas.geometry import Frame
from compas.geometry import bestfit_plane_numpy
from compas.itertools import pairwise
from compas.scene import Scene
from compas import json_dump

# =============================================================================
# Load data
# =============================================================================


IFILE = pathlib.Path(__file__).parent / "009_mesh.json"
dual = compas.json_load(IFILE)

# =============================================================================
# Blocks
# =============================================================================

blocks = []

for face in dual.faces():
    vertices = dual.face_vertices(face)
    normals = [dual.vertex_normal(vertex) for vertex in vertices]
    thickness = dual.vertices_attribute("thickness", keys=vertices)

    middle = dual.face_polygon(face)
    bottom = [point - vector * (0.5 * t) for point, vector, t in zip(middle, normals, thickness)]
    top = [point + vector * (0.5 * t) for point, vector, t in zip(middle, normals, thickness)]

    plane = Plane(*bestfit_plane_numpy(top))

    flattop = []
    for a, b in zip(bottom, top):
        b = plane.intersection_with_line(Line(a, b))
        flattop.append(b)

    sides = []
    for (a, b), (aa, bb) in zip(pairwise(bottom + bottom[:1]), pairwise(flattop + flattop[:1])):
        sides.append([a, b, bb, aa])

    polygons = [bottom[::-1]] + [flattop] + sides

    block = Mesh.from_polygons(polygons)
    block.update_default_face_attributes(is_support=False, is_interface=False)

    for index, (u, v) in enumerate(pairwise(vertices + vertices[:1])):
        is_support = dual.edge_attribute((u, v), name="is_support")
        if is_support:
            block.face_attribute(2 + index, "is_support", True)

    blocks.append(block)
    dual.face_attribute(face, "block", block)

    top_frame = Frame.from_plane(Plane.from_points(flattop))
    top_frame.flip()
    dual.face_attribute(face, "top_frame", top_frame)

    bottom_frame = Frame.from_plane(Plane.from_points(bottom))
    bottom_frame.flip()
    dual.face_attribute(face, "bottom_frame", bottom_frame)


# =============================================================================
# Serialize
# =============================================================================

json_dump(dual, pathlib.Path(__file__).parent / "010_mesh.json")

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(dual)
for block in blocks:
    scene.add(block, facecolor={face: Color.red() for face in block.faces_where(is_support=True)})
for face in dual.faces():
    scene.add(dual.face_attribute(face, "top_frame"), scale=20)
    scene.add(dual.face_attribute(face, "bottom_frame"), scale=20)
scene.draw()

