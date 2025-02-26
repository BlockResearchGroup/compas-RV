#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.datastructures import Mesh
from compas.scene import Scene
from compas_tna.diagrams import FormDiagram
from compas import json_dump
from compas.itertools import pairwise


def break_boundary(mesh: Mesh, breakpoints: list[int]) -> tuple[list[list[int]], list[int]]:

    # Get the list of vertices on the boundary (first boundary from the mesh)
    # If the first and last vertices in the boundary are the same, remove the last vertex (close loop)
    boundary: list[int] = mesh.vertices_on_boundaries()[0]
    
    if boundary[0] == boundary[-1]:
        del boundary[-1]

    # Sort the breakpoints based on their index in the boundary
    # Find the starting point in the boundary for the first breakpoint
    # Rearrange the boundary to start from the first breakpoint
    breakpoints = sorted(breakpoints, key=lambda s: boundary.index(s))
    start = boundary.index(breakpoints[0])
    boundary = boundary[start:] + boundary[:start]

    # Iterate over pairs of breakpoints and create sub-boundaries from the main boundary
    borders = []
    
    for a, b in pairwise(breakpoints):
        start = boundary.index(a)  # Find index of the first breakpoint in the boundary
        end = boundary.index(b)    # Find index of the second breakpoint in the boundary
        borders.append(boundary[start : end + 1])  # Add the sub-boundary from start to end

    # Add the last segment from the last breakpoint to the first one to close the loop
    borders.append(boundary[end:] + boundary[:1])

    # Return the sub-boundaries and the breakpoints
    return borders, breakpoints


# =============================================================================
# Load data
# =============================================================================

IFILE = pathlib.Path(__file__).parent / "rhinovault_session.json"

rv_session = compas.json_load(IFILE)
rv_scene: Scene = rv_session["scene"]

thrustobject = rv_scene.find_by_name("ThrustDiagram")
thrustdiagram: FormDiagram = thrustobject.mesh

# =============================================================================
# Mesh
#
# - make a copy of the thrustdiagram
# - remove the "TNA" faces cooresponding to boundary openings
# - compute the average edge length for remeshing
# =============================================================================

mesh: Mesh = thrustdiagram.copy(cls=Mesh)

for face in list(mesh.faces_where(_is_loaded=False)):
    mesh.delete_face(face)

# =============================================================================
# Mesh: Borders
# =============================================================================

supports = list(mesh.vertices_where(is_support=True))
borders, supports = break_boundary(mesh, supports)
print(borders)
print(supports)

mesh.attributes["supports"] = supports
mesh.attributes["borders"] = borders

# =============================================================================
# Serialize
# =============================================================================

json_dump(mesh, pathlib.Path(__file__).parent / "001_mesh.json")

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
# scene.clear_context()
scene.add(mesh)
scene.draw()