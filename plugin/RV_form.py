#! python3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas.geometry import Box
from compas.geometry import bounding_box
from compas.geometry import scale_vector
from compas.geometry import sum_vectors
from compas.scene import Scene
from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import Pattern
from compas_rv.datastructures import ThrustDiagram
from compas_rv.scene import RhinoPatternObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene: Scene = session.scene()

    pattern: RhinoPatternObject = scene.find_by_itemtype(itemtype=Pattern)
    if not pattern:
        return

    # =============================================================================
    # Init the form diagram
    # =============================================================================

    rs.UnselectAllObjects()

    form = FormDiagram.from_pattern(pattern.mesh)
    form.name = "FormDiagram"

    # flip the diagram if the normals are pointing down

    normals = [form.face_normal(face) for face in form.faces_where(_is_loaded=True)]
    scale = 1 / len(normals)
    normal = scale_vector(sum_vectors(normals), scale)
    if normal[2] < 0:
        form.flip_cycles()

    # add also the fixed vertices as anchors

    form.vertices_attribute("is_fixed", False)

    fixed = list(pattern.mesh.vertices_where(is_fixed=True))

    if fixed:
        for vertex in fixed:
            if form.has_vertex(vertex):
                form.vertex_attribute(vertex, "is_support", True)

    # init the thrust diagram

    bbox = Box.from_bounding_box(bounding_box(form.vertices_attributes("xyz")))
    diagonal = bbox.points[2] - bbox.points[0]
    zmax = 0.25 * diagonal.length

    compas_rv.settings.SETTINGS["TNA"]["vertical.zmax"] = zmax

    # =============================================================================
    # Update scene
    # =============================================================================

    pattern.show = False

    scene.add(form)

    rs.UnselectAllObjects()
    rs.EnableRedraw(False)
    scene.redraw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="Init Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
