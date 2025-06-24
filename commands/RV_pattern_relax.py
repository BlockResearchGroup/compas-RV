#! python3
# venv: brg-csd
# r: compas_rv>=0.9.2

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

    if form or force:
        return session.warn("Please remove all form and force diagrams before using pattern commands.")

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
