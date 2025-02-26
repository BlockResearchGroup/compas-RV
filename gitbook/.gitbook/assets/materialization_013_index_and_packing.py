
#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.datastructures import Mesh
from compas.geometry import Frame, Sphere, Brep, Transformation
from compas_rhino.conversions import frame_to_rhino_plane
from compas.scene import Scene
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc


scene = Scene()
scene.clear_context()

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
# Create Index Texts
# =============================================================================


def create_3d_text(text, plane, group_name, height=8.0, extrusion_distance=0.5):
    """Create 3D text geometry in Rhino and add it to a group.

    Args:
        text (str): The text to create
        plane: Rhino plane for text placement
        group_name (str): Name of the group to add text objects to
        height (float): Text height
        extrusion_distance (float): Depth of the 3D text

    Returns:
        list: List of COMPAS Brep objects representing the 3D text
    """
    # Create 2D text
    text_obj = rs.AddText(text, plane, height, justification=2)

    # Explode text into curves
    text_curves = rs.ExplodeText(text_obj, True)

    # Create surfaces from the curves
    text_surfaces = rs.AddPlanarSrf(text_curves)

    # Convert surfaces to Rhino geometry
    rhino_surfaces = [rs.coercesurface(srf) for srf in text_surfaces]

    # Create extruded 3D text
    text_3d = []

    for srf in rhino_surfaces:
        brep = rg.Brep.CreateFromOffsetFace(srf, extrusion_distance, 0.01, True, True)
        text_3d.append(sc.doc.Objects.AddBrep(brep))

    # Clean up temporary objects
    rs.DeleteObjects(text_curves + text_surfaces + [text_obj])

    # Group the 3D text objects
    rs.AddObjectsToGroup(text_3d, group_name)


rs.AddGroup("index_in_place")
for i, face in enumerate(dual.faces()):
    top_frame = dual.face_attribute(face, "top_frame").copy()
    top_frame.flip()
    plane = frame_to_rhino_plane(top_frame)
    create_3d_text(str(i), plane, "index_in_place")

# =============================================================================
# Packing
# =============================================================================

# Create a grid layout for the blocks
grid_size = 120  # spacing between blocks
blocks_per_row = int(len(block_breps) ** 0.5) + 1  # approximate square grid

rs.AddGroup("index_packed")

blocks_transformed = []
for i, face in enumerate(dual.faces()):

    block = block_breps[face]

    top_face_frame = dual.face_attribute(face, "top_frame")

    # Calculate grid position
    row = i // blocks_per_row
    col = i % blocks_per_row

    # Create target frame with Z pointing up (top face will be down)
    target_point = [col * grid_size + 1200, row * grid_size, 0]
    target_frame = Frame.worldXY()
    target_frame.point = target_point

    T = Transformation.from_frame_to_frame(top_face_frame, target_frame)
    blocks_transformed.append(block.transformed(T))

    # Add index text
    bottom_frame = dual.face_attribute(face, "bottom_frame")
    bottom_frame_packed = bottom_frame.transformed(T)
    plane = frame_to_rhino_plane(bottom_frame_packed)
    create_3d_text(str(i), plane, "index_packed")


# =============================================================================
# Visualisation
# =============================================================================

for block in block_breps.values():
    scene.add(block)

for block in blocks_transformed:
    scene.add(block)

scene.draw()

