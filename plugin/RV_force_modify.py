#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.2, compas_session>=0.4.1, compas_tna>=0.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        return

    force = session.find_forcediagram()
    if not force:
        return

    # =============================================================================
    # Modify force vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes", "MoveVertices"]
    option = rs.GetString("Modify the Force Diagram", strings=options)

    if not option:
        return

    if option == "VertexAttributes":
        force.show_vertices = list(force.diagram.vertices())
        force.redraw_vertices()

        selected = force.select_vertices()

        if selected:
            force.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        force.show_edges = list(force.diagram.edges())
        force.redraw_edges()

        selected = force.select_edges()

        if selected:
            force.update_edge_attributes(selected)

    elif option == "MoveVertices":
        force.show_vertices = list(force.diagram.vertices())
        force.redraw_vertices()

        selected = force.select_vertices()

        if not selected:
            return

        directions = ["X", "Y", "XY", "Free"]
        direction = rs.GetString(message="", strings=directions)

        if not direction:
            return

        if direction in ("X", "Y", "XY"):
            force.move_vertices_direction(selected, direction=direction)

        else:
            force.move_vertices(selected)

        # update angle deviations

    else:
        raise NotImplementedError

    if session.settings.autoupdate:
        rs.MessageBox("Automatic equilibrium updates are not available yet.", title="Info")

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
        session.record(name="Modify Force Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
