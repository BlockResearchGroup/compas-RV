#! python3
# venv: brg-csd
# r: compas_rv>=0.5.0

import rhinoscriptsyntax as rs  # type: ignore

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
