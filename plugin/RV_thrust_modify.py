#! python3
# venv: rhinovault
# r: compas, compas_rui, compas_rv, compas_session, compas_tna


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import ThrustDiagram
from compas_rv.scene import RhinoThrustObject
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    thrust: RhinoThrustObject = session.scene.find_by_itemtype(ThrustDiagram)
    if not thrust:
        return

    # =============================================================================
    # Modify pattern vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes"]
    option = rs.GetString("Modify the Thrust Diagram", strings=options)
    if not option:
        return

    if option == "VertexAttributes":
        thrust.show_vertices = True
        thrust.show_free = True
        thrust.show_fixed = True
        thrust.show_supports = True

        rs.EnableRedraw(False)
        thrust.clear_vertices()
        thrust.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = thrust.select_vertices()
        thrust.show_vertices = vertices

        rs.EnableRedraw(False)
        thrust.clear_vertices()
        thrust.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        thrust.update_vertex_attributes(vertices)

    elif option == "EdgeAttributes":
        thrust.show_edges = True

        rs.EnableRedraw(False)
        thrust.clear_edges()
        thrust.draw_edges()
        rs.EnableRedraw(True)
        rs.Redraw()

        edges = thrust.select_edges()
        thrust.update_edge_attributes(edges)

    else:
        raise NotImplementedError

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    thrust.show_vertices = True
    thrust.show_free = False
    thrust.show_fixed = True
    thrust.show_supports = True
    thrust.show_edges = True

    rs.EnableRedraw(False)
    thrust.clear()
    thrust.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Modify Thrust Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
