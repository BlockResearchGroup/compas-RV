#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.2, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas.geometry import Box
from compas.geometry import bounding_box
from compas_rv.datastructures import ForceDiagram
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram(warn=False)
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    force = session.find_forcediagram(warn=False)
    if force:
        print("ForceDiagram already exists in the scene.")
        return

    session.clear_all_forcediagrams()

    # =============================================================================
    # Init the force diagram
    # =============================================================================

    forcediagram: ForceDiagram = ForceDiagram.from_formdiagram(form.diagram)
    forcediagram.update_default_edge_attributes(lmin=0.1)

    bbox_form = Box.from_bounding_box(bounding_box(form.diagram.vertices_attributes("xyz")))
    bbox_force = Box.from_bounding_box(bounding_box(forcediagram.vertices_attributes("xyz")))

    y_form = bbox_form.ymin + 0.5 * (bbox_form.ymax - bbox_form.ymin)
    y_force = bbox_force.ymin + 0.5 * (bbox_force.ymax - bbox_force.ymin)
    dx = 1.3 * (bbox_form.xmax - bbox_form.xmin) + (bbox_form.xmin - bbox_force.xmin)
    dy = y_form - y_force

    forcediagram.translate([dx, dy, 0])
    forcediagram.update_angle_deviations()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.add(forcediagram, name=forcediagram.name)
    session.scene.redraw()

    rs.Redraw()

    print('ForceDiagram successfully created.')

    if session.settings.autosave:
        session.record(name="Create Force Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
