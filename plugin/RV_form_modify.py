#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui==0.4.1, compas_session==0.4.4, compas_tna==0.5.1, compas_fd==0.5.3

import rhinoscriptsyntax as rs  # type: ignore

from compas.geometry import Box
from compas.geometry import bounding_box
from compas_rv.datastructures import ForceDiagram
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    force = session.find_forcediagram(warn=False)
    thrust = session.find_thrustdiagram(warn=False)

    RECREATE_FORCE = False

    # =============================================================================
    # Modify form vertices
    # =============================================================================

    rs.UnselectAllObjects()

    options = ["Dropdowns", "Supports", "Loads", "Openings", "Boundaries", "EdgeConstraints", "ForceDensities"]
    option = rs.GetString("Modify the Form Diagram", strings=options)
    if not option:
        return

    # Dropdowns
    # adding and removing supports is only allowed for internal vertices

    if option == "Dropdowns":
        actions = ["Add", "Remove"]
        action = rs.GetString("Select operation", strings=actions)

        if not action:
            return

        if thrust:
            thrust.show_vertices = False
            thrust.redraw_vertices()

        if action == "Add":
            form.show_vertices = list(form.diagram.vertices_where(is_support=False, is_vertex_internal=True))
            form.redraw_vertices()
            selected = form.select_vertices()

            if selected:
                form.diagram.vertices_attribute(name="is_support", value=True, keys=selected)

        elif action == "Remove":
            selectable = list(form.diagram.vertices_where(is_support=True, is_vertex_internal=True))

            if not selectable:
                return session.warn("There are no internal supports.")

            form.show_vertices = selectable
            form.redraw_vertices()
            selected = form.select_vertices()

            if selected:
                form.diagram.vertices_attribute(name="is_support", value=False, keys=selected)

    # Boundary supports
    # can only be moved
    # they can't be removed or added
    # movement on the formdiagram is only permitted in XY

    elif option == "BoundarySupports":
        if thrust:
            thrust.show_vertices = False
            thrust.redraw_vertices()

        form.show_vertices = list(form.diagram.vertices_where(is_support=True, is_vertex_internal=False))
        form.redraw_vertices()
        selected = form.select_vertices()

        if selected:
            directions = ["X", "Y", "XY"]
            direction = rs.GetString(message="Direction", strings=directions)

            if direction:
                form.move_vertices_direction(selected, direction=direction)

    # Loads
    # point loads can be added to all internal vertices
    # positive values are in the negative z-direction

    elif option == "Loads":
        form.show_vertices = list(form.diagram.vertices_where(is_support=False))
        form.redraw_vertices()
        selected = form.select_vertices()

        if selected:
            form.update_vertex_attributes(selected, names=["pz", "t"])

    # Openings
    # create openings by marking faces as not loaded
    # edges between two adjacent not loaded faces will be marked as _is_edge=False => requires force re-init
    # NOTE: differentiate between _is_virtual and _is_loaded/_is_opening

    elif option == "Openings":
        actions = ["DeleteFaces", "DeleteVertex"]
        action = rs.GetString("Create opening.", strings=actions)
        if not action:
            return

        if action == "DeleteFaces":
            form.show_faces = list(form.diagram.faces_where(_is_loaded=True))
            form.redraw_faces()
            selected = form.select_faces_manual()

            if selected:
                for face in selected:
                    if form.diagram.has_face(face):
                        form.diagram.delete_face(face)
                    if thrust:
                        if thrust.diagram.has_face(face):
                            thrust.diagram.delete_face(face)
                if force:
                    RECREATE_FORCE = True

        elif action == "DeleteVertex":
            raise NotImplementedError

    # Boundaries
    # scale the sag of the boundaries
    # NOTE: perhaps not needed if interactive Q scaling is available

    elif option == "Boundaries":
        raise NotImplementedError

    # Edge constraints
    # min/max length
    # min/max dual length

    elif option == "EdgeConstraints":
        form.show_edges = list(form.diagram.edges_where(_is_edge=True))
        form.redraw_edges()
        selected = form.select_edges()
        if selected:
            form.update_edge_attributes(selected, names=["lmin", "lmax", "hmin", "hmax"])

    # Force densities
    # interactive scaling of force densities

    elif option == "ForceDensities":
        raise NotImplementedError

    # =============================================================================
    # Recreate force?
    # =============================================================================

    if RECREATE_FORCE:
        form.diagram.update_boundaries()

        if thrust:
            thrust.diagram.update_boundaries()

        forcediagram: ForceDiagram = ForceDiagram.from_formdiagram(form.diagram)

        forcediagram.update_position()
        forcediagram.update_angle_deviations()

        # forcediagram.solve_fd()  # this is very experimental

        force.diagram = forcediagram

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    form.show_vertices = True
    form.show_free = False
    form.show_fixed = True
    form.show_supports = True
    form.show_edges = True
    form.show_faces = False

    if RECREATE_FORCE:
        force.show_edges = True
        force.show_faces = False
        force.show_vertices = True

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Modify Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
