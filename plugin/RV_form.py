#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3, compas_rv>=0.1, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas.geometry import Box
from compas.geometry import bounding_box
from compas.geometry import scale_vector
from compas.geometry import sum_vectors
from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import Pattern
from compas_rv.scene import RhinoPatternObject
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    pattern: RhinoPatternObject = session.scene.find_by_itemtype(Pattern)
    if not pattern:
        return

    # =============================================================================
    # Init the form diagram
    # =============================================================================

    rs.UnselectAllObjects()

    form = FormDiagram.from_pattern(pattern.mesh)
    form.name = "FormDiagram"

    form.vertices_attribute(name="z", value=0)

    normals = [form.face_normal(face) for face in form.faces_where(_is_loaded=True)]
    scale = 1 / len(normals)
    normal = scale_vector(sum_vectors(normals), scale)
    if normal[2] < 0:
        form.flip_cycles()

    form.vertices_attribute("is_fixed", False)

    fixed = list(pattern.mesh.vertices_where(is_fixed=True))

    if fixed:
        for vertex in fixed:
            if form.has_vertex(vertex):
                form.vertex_attribute(vertex, "is_support", True)

    bbox = Box.from_bounding_box(bounding_box(form.vertices_attributes("xyz")))
    diagonal = bbox.points[2] - bbox.points[0]
    zmax = 0.25 * diagonal.length

    session.settings.tna.vertical.zmax = zmax

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show = False

    session.scene.add(form, name=form.name)
    session.scene.redraw()

    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Init Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
