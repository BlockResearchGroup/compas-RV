#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.1, compas_session>=0.4.1, compas_tna>=0.5

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

    thrust = session.find_thrustdiagram()
    if not thrust:
        return

    # =============================================================================
    # Modify pattern vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes", "FaceAttributes", "MoveSupports"]
    option = rs.GetString("Modify the Thrust Diagram", strings=options)
    if not option:
        return

    if option == "VertexAttributes":
        thrust.show_vertices = list(thrust.diagram.vertices())
        thrust.redraw_vertices()

        selected = thrust.select_vertices()

        if selected:
            thrust.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        thrust.show_edges = list(thrust.diagram.edges_where(_is_edge=True))
        thrust.redraw_edges()

        selected = thrust.select_edges()

        if selected:
            thrust.update_edge_attributes(selected)

    elif option == "MoveSupports":
        form.show_vertices = False
        form.redraw_vertices()

        thrust.show_vertices = list(thrust.diagram.vertices_where(is_support=True))
        thrust.redraw_vertices()

        selected = thrust.select_vertices()

        if not selected:
            return

        thrust.move_vertices_direction(selected, direction="Z")

    else:
        raise NotImplementedError

    if session.settings.autoupdate:
        rs.MessageBox("Automatic equilibrium updates are not available yet.", title="Info")

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    form.show_vertices = True
    form.redraw_vertices()

    thrust.show_vertices = True
    thrust.show_free = False
    thrust.show_fixed = True
    thrust.show_supports = True
    thrust.show_edges = False

    thrust.redraw()

    if session.settings.autosave:
        session.record(name="Modify Thrust Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
