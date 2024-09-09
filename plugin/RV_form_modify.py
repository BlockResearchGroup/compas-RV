#! python3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas_rv.datastructures import FormDiagram
from compas_rv.scene import RhinoFormObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    form: RhinoFormObject = scene.find_by_itemtype(itemtype=FormDiagram)
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

        form.show_vertices = True
        form.show_free = True
        form.show_fixed = True
        form.show_supports = True

        rs.EnableRedraw(False)
        form.clear_vertices()
        form.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        vertices = form.select_vertices()
        form.show_vertices = vertices

        rs.EnableRedraw(False)
        form.clear_vertices()
        form.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

        form.update_vertex_attributes(vertices)

    elif option == "EdgeAttributes":

        form.show_edges = True

        rs.EnableRedraw(False)
        form.clear_edges()
        form.draw_edges()
        rs.EnableRedraw(True)
        rs.Redraw()

        edges = form.select_edges()
        form.update_edge_attributes(edges)

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

    rs.EnableRedraw(False)
    form.clear()
    form.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="Modify Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
