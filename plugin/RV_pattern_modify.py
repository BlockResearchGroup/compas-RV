#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.2, compas_session>=0.4.1, compas_tna>=0.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    pattern = session.find_pattern()
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    # =============================================================================
    # Modify pattern vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes"]
    option = rs.GetString("Modify the Form Diagram", strings=options)
    if not option:
        return

    if option == "VertexAttributes":
        pattern.show_vertices = list(pattern.mesh.vertices())
        pattern.redraw_vertices()

        selected = pattern.select_vertices()

        if selected:
            pattern.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        pattern.show_edges = list(pattern.mesh.edges())
        pattern.redraw_edges()

        selected = pattern.select_edges()

        if selected:
            pattern.update_edge_attributes(selected)

    else:
        raise NotImplementedError

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_vertices = list(set(list(pattern.mesh.vertices_where(is_support=True)) + list(pattern.mesh.vertices_where(is_fixed=True))))
    pattern.show_edges = False
    pattern.show_faces = True

    pattern.redraw()

    if session.settings.autosave:
        session.record(name="Modify Pattern")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
