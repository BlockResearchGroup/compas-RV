#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui==0.4.1, compas_session==0.4.4, compas_tna==0.5.1, compas_fd==0.5.3

import rhinoscriptsyntax as rs  # type: ignore

from compas.geometry import Box
from compas.geometry import bounding_box
from compas.geometry import scale_vector
from compas.geometry import sum_vectors
from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import ThrustDiagram
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    pattern = session.find_pattern(warn=False)
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    if not list(pattern.mesh.vertices_where(is_support=True)):
        print("Pattern has no supports! Please define supports vertices.")
        return

    form = session.find_formdiagram(warn=False)
    if form:
        print("FormDiagram already exists in the scene.")
        return

    session.clear_all_formdiagrams()

    # =============================================================================
    # Init the form diagram
    # =============================================================================

    rs.UnselectAllObjects()

    formdiagram = FormDiagram.from_pattern(pattern.mesh)
    formdiagram.name = "FormDiagram"

    formdiagram.vertices_attribute(name="z", value=0)

    normals = [formdiagram.face_normal(face) for face in formdiagram.faces_where(_is_loaded=True)]
    scale = 1 / len(normals)
    normal = scale_vector(sum_vectors(normals), scale)
    if normal[2] < 0:
        formdiagram.flip_cycles()

    formdiagram.vertices_attribute("is_fixed", False)

    fixed = list(pattern.mesh.vertices_where(is_fixed=True))

    if fixed:
        for vertex in fixed:
            if formdiagram.has_vertex(vertex):
                formdiagram.vertex_attribute(vertex, "is_support", True)

    thrustdiagram: ThrustDiagram = formdiagram.copy(cls=ThrustDiagram)
    thrustdiagram.name = "ThrustDiagram"

    # set an initial value for zmax
    bbox = Box.from_bounding_box(bounding_box(formdiagram.vertices_attributes("xyz")))
    diagonal = bbox.points[2] - bbox.points[0]
    zmax = 0.25 * diagonal.length
    session.settings.tna.vertical_zmax = zmax

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show = False

    session.scene.add(formdiagram, name=formdiagram.name)
    session.scene.add(thrustdiagram, name=thrustdiagram.name, show=False)

    session.scene.redraw()

    rs.Redraw()

    print('FormDiagram successfully created.')

    if session.settings.autosave:
        session.record(name="Init Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
