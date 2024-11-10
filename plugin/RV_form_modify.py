#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.2, compas_session>=0.4.1, compas_tna>=0.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    # =============================================================================
    # Modify form vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes"]
    option = rs.GetString("Modify the Form Diagram", strings=options)
    if not option:
        return

    if option == "VertexAttributes":
        form.show_vertices = list(form.diagram.vertices())
        form.redraw_vertices()

        selected = form.select_vertices()

        if selected:
            form.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        form.show_edges = list(form.diagram.edges_where(_is_edge=True))
        form.redraw_edges()

        selected = form.select_edges()

        if selected:
            form.update_edge_attributes(selected)

    else:
        raise NotImplementedError

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    form.show_vertices = True
    form.show_free = False
    form.show_fixed = True
    form.show_supports = True
    form.show_edges = True

    form.redraw()

    if session.settings.autosave:
        session.record(name="Modify Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
