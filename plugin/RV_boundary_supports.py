#! python3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.scene import Scene
from compas_rv.datastructures import Pattern
from compas_rv.scene import RhinoPatternObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene: Scene = session.scene()

    pattern: RhinoPatternObject = scene.find_by_itemtype(itemtype=Pattern)
    if not pattern:
        return

    # =============================================================================
    # Update supports auto
    # =============================================================================

    fixed = list(pattern.mesh.vertices_where(is_fixed=True))

    leaves = []
    for vertex in pattern.mesh.vertices():
        nbrs = pattern.mesh.vertex_neighbors(vertex)
        count = 0
        for nbr in nbrs:
            if pattern.mesh.edge_attribute((vertex, nbr), "_is_edge"):
                count += 1
        if count == 1:
            leaves.append(vertex)

    anchors = list(set(fixed) | set(leaves))

    if anchors:
        pattern.mesh.vertices_attribute(name="is_anchor", value=True, keys=anchors)

        pattern.clear()
        pattern.draw()

    # =============================================================================
    # Update supports manual
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["Add", "Remove"]
    option = rs.GetString("Add or Remove supports", strings=options)
    if not option:
        return

    if option == "Add":

        pattern.show_free = True
        pattern.show_fixed = True
        pattern.show_anchors = True

        rs.EnableRedraw(False)
        pattern.clear_vertices()
        pattern.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = pattern.select_vertices()
        pattern.mesh.vertices_attribute(name="is_anchor", value=True, keys=vertices)

    elif option == "Remove":

        pattern.show_free = False
        pattern.show_fixed = False
        pattern.show_anchors = True

        rs.EnableRedraw(False)
        pattern.clear_vertices()
        pattern.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = pattern.select_vertices()
        pattern.mesh.vertices_attribute(name="is_anchor", value=False, keys=vertices)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_anchors = True
    pattern.show_fixed = True
    pattern.show_free = False
    pattern.show_edges = False

    rs.EnableRedraw(False)
    pattern.clear()
    pattern.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.CONFIG["autosave.events"]:
        session.record(eventname="Identify Supports")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
