#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_tna==0.5.2

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    force = session.find_forcediagram()
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    # =============================================================================
    # Pattern relax
    # =============================================================================

    rs.UnselectAllObjects()

    force.diagram.solve_fd()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    force.show_vertices = True
    force.show_free = False
    force.show_fixed = True
    force.show_supports = True
    force.show_edges = True

    force.redraw()

    if session.settings.autosave:
        session.record(name="Relax the FormDiagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
