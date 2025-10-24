#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession
from compas_rv.solvers import update_force_from_form
from compas_tna.equilibrium import vertical_from_zmax


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    force = session.find_forcediagram()
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    # Note: ThrustDiagram functionality is now integrated into FormDiagram
    # The form diagram now contains the 3D thrust surface information

    # =============================================================================
    # Modify pattern vertices
    # =============================================================================

    kmax = session.settings.tna.vertical_kmax
    zmax = session.settings.tna.vertical_zmax

    rs.UnselectAllObjects()

    options = ["VertexAttributes", "EdgeAttributes", "FaceAttributes", "MoveSupports", "ScaleForceDensities"]
    option = rs.GetString("Modify the Thrust Diagram", strings=options)
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

    elif option == "MoveSupports":
        form.show_vertices = list(form.diagram.vertices_where(is_support=True))
        form.redraw_vertices()
        selected = form.select_vertices()
        if selected:
            form.move_vertices_direction(selected, direction="Z")

    elif option == "ScaleForceDensities":
        form.show_edges = list(form.diagram.edges_where(_is_edge=True))
        form.redraw_edges()
        selected = form.select_edges()
        if selected:
            selected = list(set(selected))
            factor = rs.GetReal("Scale factor", number=1.0, minimum=0)
            if not factor:
                return
            for edge in selected:
                q = factor * form.diagram.edge_attribute(edge, "q")

                form.diagram.edge_attribute(edge, "q", q)

                form.diagram.solve_fd()
                update_force_from_form(force.diagram, form.diagram)
                _, scale = vertical_from_zmax(form.diagram, zmax, kmax=kmax)
                force.diagram.attributes["scale"] = scale
                force.diagram.update_position()

                # The form diagram now contains the 3D thrust surface information
                # No need to sync between separate diagrams

    else:
        raise NotImplementedError

    if session.settings.autoupdate:
        rs.MessageBox("Automatic equilibrium updates are not available yet.", title="Info")

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    form.show_vertices = True
    form.show_free = False
    form.show_fixed = True
    form.show_supports = True
    form.show_edges = True

    force.show_vertices = True
    force.show_free = False
    force.show_fixed = True
    force.show_supports = True
    force.show_edges = True

    # Set 3D display parameters for thrust surface visualization
    form.show_vertices_3d = True
    form.show_free_3d = False
    form.show_fixed_3d = True
    form.show_supports_3d = True
    form.show_edges_3d = False

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Modify Thrust Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
