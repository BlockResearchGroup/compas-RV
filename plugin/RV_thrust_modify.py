#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3, compas_rv>=0.1, compas_session>=0.4.1, compas_tna>=0.5


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
        selectable = list(thrust.mesh.vertices())
        selected = thrust.select_vertices(selectable)
        if selected:
            thrust.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        selectable = list(thrust.mesh.edges_where(_is_edge=True))
        selected = thrust.select_edges(selectable)
        if selected:
            thrust.update_edge_attributes(selected)

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
    thrust.clear()
    thrust.draw()

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
