#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3, compas_rv>=0.1, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import FormDiagram
from compas_rv.scene import RhinoFormObject
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form: RhinoFormObject = session.scene.find_by_itemtype(FormDiagram)
    if not form:
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
        selectable = list(form.mesh.vertices())
        selected = form.select_vertices(selectable)
        if selected:
            form.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        selectable = list(form.mesh.edges_where(_is_edge=True))
        selected = form.select_edges(selectable)
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
    form.clear()
    form.draw()

    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Modify Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
