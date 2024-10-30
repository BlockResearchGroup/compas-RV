#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3, compas_rv>=0.1, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import Pattern
from compas_rv.scene import RhinoPatternObject
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    pattern: RhinoPatternObject = session.scene.find_by_itemtype(Pattern)
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
        pattern.mesh.vertices_attribute(name="is_support", value=True, keys=anchors)

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
        selectable = list(pattern.mesh.vertices())
        selected = pattern.select_vertices(selectable)
        if selected:
            pattern.mesh.vertices_attribute(name="is_support", value=True, keys=selected)

    elif option == "Remove":
        selectable = list(pattern.mesh.vertices_where(is_support=True))
        selected = pattern.select_vertices(selectable)
        if selected:
            pattern.mesh.vertices_attribute(name="is_support", value=False, keys=selected)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_vertices = list(set(list(pattern.mesh.vertices_where(is_support=True)) + list(pattern.mesh.vertices_where(is_fixed=True))))
    pattern.show_edges = False
    pattern.show_faces = True

    pattern.clear()
    pattern.draw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Update Pattern Supports")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
