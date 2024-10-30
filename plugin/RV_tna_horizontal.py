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
from compas_tna.equilibrium import horizontal_nodal


def RunCommand():
    session = RVSession()

    formobj: RhinoFormObject = session.scene.find_by_itemtype(FormDiagram)
    if not formobj:
        return

    forceobj: RhinoForceObject = session.scene.find_by_itemtype(ForceDiagram)
    if not forceobj:
        return

    # =============================================================================
    # Compute horizontal
    # =============================================================================

    kmax = session.settings.tna.horizontal.kmax
    alpha = session.settings.tna.horizontal.alpha

    horizontal_nodal(formobj.mesh, forceobj.mesh, kmax=kmax, alpha=alpha)

    bbox_form = Box.from_bounding_box(bounding_box(formobj.mesh.vertices_attributes("xyz")))
    bbox_force = Box.from_bounding_box(bounding_box(forceobj.mesh.vertices_attributes("xyz")))

    y_form = bbox_form.ymin + 0.5 * (bbox_form.ymax - bbox_form.ymin)
    y_force = bbox_force.ymin + 0.5 * (bbox_force.ymax - bbox_force.ymin)
    dx = 1.3 * (bbox_form.xmax - bbox_form.xmin) + (bbox_form.xmin - bbox_force.xmin)
    dy = y_form - y_force

    forceobj.mesh.translate([dx, dy, 0])
    forceobj.mesh.update_angle_deviations()

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

    session.scene.redraw()
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="TNA Horizontal")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
