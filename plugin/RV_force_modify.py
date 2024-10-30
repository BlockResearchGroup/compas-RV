#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3, compas_rv>=0.1, compas_session>=0.4.1, compas_tna>=0.5


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
        selectable = list(force.mesh.vertices())
        selected = force.select_vertices(selectable)
        if selected:
            force.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        selectable = list(force.mesh.edges_where(_is_edge=True))
        selected = force.select_edges(selectable)
        if selected:
            force.update_edge_attributes(selected)

    else:
        raise NotImplementedError

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    force.show_vertices = True
    force.show_free = False
    force.show_fixed = True
    force.show_supports = True
    force.show_edges = True
    force.clear()
    force.draw()

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
