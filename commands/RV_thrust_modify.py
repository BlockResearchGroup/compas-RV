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

    thrust = session.find_thrustdiagram()
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

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
        thrust.show_vertices = list(thrust.diagram.vertices())
        thrust.redraw_vertices()
        selected = thrust.select_vertices()
        if selected:
            thrust.update_vertex_attributes(selected)

    elif option == "EdgeAttributes":
        thrust.show_edges = list(thrust.diagram.edges_where(_is_edge=True))
        thrust.redraw_edges()
        selected = thrust.select_edges()
        if selected:
            thrust.update_edge_attributes(selected)

    elif option == "MoveSupports":
        form.show_vertices = False
        form.redraw_vertices()
        thrust.show_vertices = list(thrust.diagram.vertices_where(is_support=True))
        thrust.redraw_vertices()
        selected = thrust.select_vertices()
        if selected:
            thrust.move_vertices_direction(selected, direction="Z")

    elif option == "ScaleForceDensities":
        thrust.show_edges = list(thrust.diagram.edges_where(_is_edge=True))
        thrust.redraw_edges()
        selected = thrust.select_edges()
        if selected:
            selected = list(set(selected))
            factor = rs.GetReal("Scale factor", number=1.0, minimum=0)
            if not factor:
                return
            for edge in selected:
                q = factor * thrust.diagram.edge_attribute(edge, "q")

                form.diagram.edge_attribute(edge, "q", q)

                form.diagram.solve_fd()
                update_force_from_form(force.diagram, form.diagram)
                _, scale = vertical_from_zmax(form.diagram, zmax, kmax=kmax)
                force.diagram.attributes["scale"] = scale
                force.diagram.update_position()

                for vertex in form.diagram.vertices():
                    form_attr = form.diagram.vertex_attributes(vertex)
                    thrust_attr = thrust.diagram.vertex_attributes(vertex)
                    thrust_attr.update(form_attr)  # type: ignore

                for edge in form.diagram.edges():
                    form_attr = form.diagram.edge_attributes(edge)
                    thrust_attr = thrust.diagram.edge_attributes(edge)
                    thrust_attr.update(form_attr)  # type: ignore

                form.diagram.vertices_attribute(name="z", value=0)

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

    thrust.show_vertices = True  # type: ignore
    thrust.show_free = False
    thrust.show_fixed = True
    thrust.show_supports = True
    thrust.show_edges = False

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Modify Thrust Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
