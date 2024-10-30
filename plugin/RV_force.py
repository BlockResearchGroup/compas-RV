#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3, compas_rv>=0.1, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas.geometry import Box
from compas.geometry import bounding_box
from compas_rv.datastructures import ForceDiagram
from compas_rv.datastructures import FormDiagram
from compas_rv.scene import RhinoForceObject
from compas_rv.scene import RhinoFormObject
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    formobj: RhinoFormObject = session.scene.find_by_itemtype(FormDiagram)
    if not formobj:
        return

    forceobj: RhinoForceObject = session.scene.find_by_itemtype(ForceDiagram)
    if forceobj:
        session.scene.remove(forceobj)
        session.scene.redraw()
        rs.Redraw()

    # =============================================================================
    # Init the force diagram
    # =============================================================================

    force: ForceDiagram = ForceDiagram.from_formdiagram(formobj.mesh)
    force.update_default_edge_attributes(lmin=0.1)

    bbox_form = Box.from_bounding_box(bounding_box(formobj.mesh.vertices_attributes("xyz")))
    bbox_force = Box.from_bounding_box(bounding_box(force.vertices_attributes("xyz")))

    y_form = bbox_form.ymin + 0.5 * (bbox_form.ymax - bbox_form.ymin)
    y_force = bbox_force.ymin + 0.5 * (bbox_force.ymax - bbox_force.ymin)
    dx = 1.3 * (bbox_form.xmax - bbox_form.xmin) + (bbox_form.xmin - bbox_force.xmin)
    dy = y_form - y_force

    force.translate([dx, dy, 0])
    force.update_angle_deviations()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.add(force, name=force.name)
    session.scene.redraw()

    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Init Force Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
