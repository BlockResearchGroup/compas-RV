#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui==0.4.1, compas_session==0.4.4, compas_tna==0.5.1, compas_fd==0.5.3

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    # =============================================================================
    # Pattern relax
    # =============================================================================

    rs.UnselectAllObjects()

    form.diagram.solve_fd()

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
        session.record(name="Relax the FormDiagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()