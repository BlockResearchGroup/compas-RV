#! python3
# venv: rhinovault
# r: compas>=2.4, compas_rui, compas_session, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas_rv.datastructures import ForceDiagram
from compas_rv.scene import RhinoForceObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    force: RhinoForceObject = scene.find_by_itemtype(itemtype=ForceDiagram)
    if not force:
        return

    # =============================================================================
    # Modify pattern vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes"]
    option = rs.GetString("Modify the Force Diagram", strings=options)
    if not option:
        return

    if option == "VertexAttributes":

        force.show_free = True
        force.show_fixed = True
        force.show_supports = True

        rs.EnableRedraw(False)
        force.clear_vertices()
        force.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = force.select_vertices()
        force.update_vertex_attributes(vertices)

    elif option == "EdgeAttributes":

        force.show_edges = True

        rs.EnableRedraw(False)
        force.clear_edges()
        force.draw_edges()
        rs.EnableRedraw(True)
        rs.Redraw()

        edges = force.select_edges()
        force.update_edge_attributes(edges)

    else:
        raise NotImplementedError

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    force.show_free = False
    force.show_fixed = True
    force.show_supports = True
    force.show_edges = True

    rs.EnableRedraw(False)
    force.clear()
    force.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(name="Modify Force Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
