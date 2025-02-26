
#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.datastructures import Mesh
from compas.geometry import Frame, Sphere, Brep
from compas.scene import Scene

# =============================================================================
# Load data
# =============================================================================

IFILE = pathlib.Path(__file__).parent / "011_mesh.json"
dual: Mesh = compas.json_load(IFILE)

block_breps = {face: Brep.from_mesh(dual.face_attribute(face, "block")) for face in dual.faces()}


# =============================================================================
# Making Sphere Joinery
# =============================================================================

for edge in dual.edges():
    face1, face2 = dual.edge_faces(edge)
    if face1 is not None and face2 is not None:
        line = dual.edge_line(edge)
        z_axis = line.direction
        x_axis = dual.vertex_normal(edge[0]) + dual.vertex_normal(edge[1])
        y_axis = x_axis.cross(z_axis)

        # Create frames at 0.3 and 0.7 along the edge
        p1 = line.point_at(0.3)
        p2 = line.point_at(0.7)

        sphere1a = Sphere(2.5, point=p1)
        sphere1b = Sphere(2.5, point=p2)

        sphere2a = Sphere(2.3, point=p1)
        sphere2b = Sphere(2.3, point=p2)

        block1 = block_breps[face1]
        block2 = block_breps[face2]

        # make two spheres along the edge
        block1 = block1 - sphere1a.to_brep()
        block1 = block1 - sphere1b.to_brep()
        block2 = block2 + sphere2a.to_brep()
        block2 = block2 + sphere2b.to_brep()

        block_breps[face1] = block1
        block_breps[face2] = block2

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(dual)
for block in block_breps.values():
    scene.add(block)
scene.draw()

