#! python3
# venv: rhinovault
# r: compas, compas_rui, compas_rv, compas_session, compas_tna


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import ForceDiagram
from compas_rv.scene import RhinoForceObject
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    force: RhinoForceObject = session.scene.find_by_itemtype(ForceDiagram)
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

    if session.settings.autosave:
        session.record(name="Modify Force Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
