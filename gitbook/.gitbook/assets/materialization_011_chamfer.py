
#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.datastructures import Mesh
from compas.geometry import Plane
from compas.scene import Scene
from compas import json_dump

# =============================================================================
# Load data
# =============================================================================

IFILE = pathlib.Path(__file__).parent / "010_mesh.json"
dual = compas.json_load(IFILE)

# =============================================================================
# Chamfering
# =============================================================================

MAX_CHAMFER_ANGLE = 145
CHAMFER_OFFSET = 2

face_block = {face: dual.face_attribute(face, "block").copy() for face in dual.faces()}

for vertex in dual.vertices():
    if dual.is_vertex_on_boundary(vertex):
        continue

    point = dual.vertex_point(vertex)
    normal = dual.vertex_normal(vertex)
    plane = Plane(point, normal)

    nbrs = dual.vertex_neighbors(vertex, ordered=True)

    for index, nbr in enumerate(nbrs):
        ancestor = nbrs[index - 1]
        left = plane.projected_point(dual.vertex_point(ancestor))
        right = plane.projected_point(dual.vertex_point(nbr))
        v1 = (left - plane.point).unitized()
        v2 = (right - plane.point).unitized()
        if v1.angle(v2, degrees=True) > MAX_CHAMFER_ANGLE:
            continue

        direction = (v1 + v2).unitized()
        cutter = Plane(plane.point, direction).offset(CHAMFER_OFFSET)

        face = dual.halfedge_face((vertex, nbr))
        temp: Mesh = face_block[face]
        a, b = temp.slice(cutter)
        face_block[face] = a

for face in dual.faces():
    dual.face_attribute(face, "block", face_block[face])

# =============================================================================
# Serialize
# =============================================================================

json_dump(dual, pathlib.Path(__file__).parent / "011_mesh.json")

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
for block in face_block.values():
    scene.add(block)
scene.draw()

