#! python3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas_rv.datastructures import ThrustDiagram
from compas_rv.scene import RhinoThrustObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    thrust: RhinoThrustObject = scene.find_by_itemtype(itemtype=ThrustDiagram)
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

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="Modify Thrust Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
