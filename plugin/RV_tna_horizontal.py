#! python3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas.geometry import Box
from compas.geometry import bounding_box
from compas.scene import Scene
from compas_rv.datastructures import ForceDiagram
from compas_rv.datastructures import FormDiagram
from compas_rv.scene import RhinoForceObject
from compas_rv.scene import RhinoFormObject
from compas_session.namedsession import NamedSession
from compas_tna.equilibrium import horizontal_nodal


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene: Scene = session.scene()

    formobj: RhinoFormObject = scene.find_by_itemtype(itemtype=FormDiagram)
    if not formobj:
        return

    forceobj: RhinoForceObject = scene.find_by_itemtype(itemtype=ForceDiagram)
    if not forceobj:
        return

    form: FormDiagram = formobj.mesh
    force: ForceDiagram = forceobj.mesh

    # =============================================================================
    # Compute horizontal
    # =============================================================================

    kmax = compas_rv.settings.SETTINGS["TNA"]["horizontal.kmax"]
    alpha = compas_rv.settings.SETTINGS["TNA"]["horizontal.alpha"]

    horizontal_nodal(form, force, kmax=kmax, alpha=alpha)

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

    # max_angle = max(form.diagram.edges_attribute("_a"))
    # tol = ui.registry["RV3"]["tol.angles"]

    # if max_angle < tol:
    #     print("Horizontal equilibrium found!\nMaximum angle deviation: {}".format(max_angle))
    # else:
    #     compas_rhino.display_message("Horizontal equilibrium NOT found! Consider running more iterations.\nMaximum angle deviation: {}".format(max_angle))

    rs.UnselectAllObjects()
    rs.EnableRedraw(False)
    scene.redraw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="TNA Horizontal")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
