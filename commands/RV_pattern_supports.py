#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

    if form or force:
        return session.warn("Please remove all form and force diagrams before using pattern commands.")

    pattern = session.find_pattern()
    if not pattern:
        print("There is no Pattern in the scene.")
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

        pattern.redraw()

    # =============================================================================
    # Update supports manual
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["Add", "Remove"]
    option = rs.GetString("Add or Remove supports", strings=options)
    if not option:
        return

    if option == "Add":
        pattern.show_vertices = list(pattern.mesh.vertices())
        pattern.show_edges = list(pattern.mesh.edges())
        pattern.redraw()

        selected = pattern.select_vertices()

        if selected:
            pattern.mesh.vertices_attribute(name="is_support", value=True, keys=selected)

    elif option == "Remove":
        pattern.show_vertices = list(pattern.mesh.vertices())
        pattern.show_edges = list(pattern.mesh.edges())
        pattern.redraw()

        selected = pattern.select_vertices()

        if selected:
            pattern.mesh.vertices_attribute(name="is_support", value=False, keys=selected)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_vertices = list(set(list(pattern.mesh.vertices_where(is_support=True)) + list(pattern.mesh.vertices_where(is_fixed=True))))
    pattern.show_edges = False
    pattern.show_faces = True

    pattern.redraw()

    if session.settings.autosave:
        session.record(name="Update Pattern Supports")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
