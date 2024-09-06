#! python3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas.geometry import Box
from compas.geometry import bounding_box
from compas.scene import Scene
from compas_rv.datastructures import ForceDiagram
from compas_rv.datastructures import FormDiagram

# from compas_rv.datastructures import ThrustDiagram
from compas_rv.scene import RhinoFormObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene: Scene = session.scene()

    formobj: RhinoFormObject = scene.find_by_itemtype(itemtype=FormDiagram)
    if not formobj:
        return

    # =============================================================================
    # Init the force diagram
    # =============================================================================

    form: FormDiagram = formobj.mesh

    force: ForceDiagram = ForceDiagram.from_formdiagram(form)
    force.default_edge_attributes.update({"lmin": 0.1})

    bbox_form = Box.from_bounding_box(bounding_box(form.vertices_attributes("xyz")))
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

    scene.add(force, show_faces=False, show_edges=True)

    rs.UnselectAllObjects()
    rs.EnableRedraw(False)
    scene.redraw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="Init Force Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
