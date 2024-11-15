#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_tna==0.5.2

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession
from compas_rv.solvers import InteractiveScaleHorizontal


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    force = session.find_forcediagram()
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    thrust = session.find_thrustdiagram()
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    # =============================================================================
    # Modify pattern vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes", "FaceAttributes", "MoveSupports", "ScaleForces"]
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
        if selected:
            thrust.move_vertices_direction(selected, direction="Z")

    # interactively change the scale of the force diagram
    # recompute vertical equilibrium accordingly
    # use vertical_from_q

    elif option == "ScaleForces":
        scalehorizontal = InteractiveScaleHorizontal(thrust.diagram)
        if scalehorizontal():
            force.diagram.attributes["scale"] = scalehorizontal.scale

            for index, vertex in enumerate(thrust.diagram.vertices()):
                thrust.diagram.vertex_attribute(vertex, "z", scalehorizontal.numdata.xyz[index, 2])

            for index, edge in enumerate(thrust.diagram.edges_where(_is_edge=True)):
                q = scalehorizontal.scale * scalehorizontal.numdata.q[index, 0]
                form.diagram.edge_attribute(edge, "q", q)
                thrust.diagram.edge_attribute(edge, "q", q)

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
