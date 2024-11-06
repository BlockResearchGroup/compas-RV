#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.1, compas_session>=0.4.1, compas_tna>=0.5

import rhinoscriptsyntax as rs  # type: ignore

from compas.itertools import flatten
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        return

    # =============================================================================
    # Pattern relax
    # =============================================================================

    rs.UnselectAllObjects()

    anchors = list(form.diagram.vertices_where(is_support=True))
    fixed = list(form.diagram.vertices_where(is_fixed=True))
    fixed = anchors + fixed

    options = ["True", "False"]
    option = rs.GetString("Press Enter to smooth or ESC to exit. Keep all boundaries fixed?", strings=options)
    if option is None:
        return

    if option == "True":
        # perhaps just redefine "vertices_on_boundaries"?
        fixed += list(flatten(form.diagram.vertices_on_boundaries()))
        fixed += list(flatten([form.diagram.face_vertices(face) for face in form.diagram.faces_where(_is_loaded=False)]))

    fixed = list(set(fixed))

    form.diagram.smooth_area(fixed=fixed)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    form.show_vertices = True
    form.show_free = False
    form.show_fixed = True
    form.show_supports = True
    form.show_edges = True

    form.redraw()

    if session.settings.autosave:
        session.record(name="Smooth the FormDiagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
