#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui==0.4.1, compas_session==0.4.4, compas_tna==0.5.1, compas_fd==0.5.3

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    pattern = session.find_pattern()
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    # =============================================================================
    # Pattern relax
    # =============================================================================

    rs.UnselectAllObjects()

    supports = len(list(pattern.mesh.vertices_where(is_support=True)))
    if supports < 4:
        if not session.confirm(f"You only have {supports} supports. Do you wan to proceed?"):
            return

    pattern.mesh.relax()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_vertices = list(set(list(pattern.mesh.vertices_where(is_support=True)) + list(pattern.mesh.vertices_where(is_fixed=True))))
    pattern.show_edges = False
    pattern.show_faces = True

    pattern.redraw()

    if session.settings.autosave:
        session.record(name="Relax the Pattern")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
