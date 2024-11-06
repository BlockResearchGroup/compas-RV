#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.2, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas.geometry import Box
from compas.geometry import bounding_box
from compas_rv.session import RVSession
from compas_tna.equilibrium import horizontal_nodal


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        return

    force = session.find_forcediagram()
    if not force:
        return

    # =============================================================================
    # Compute horizontal
    # =============================================================================

    kmax = session.settings.tna.horizontal_kmax
    alpha = session.settings.tna.horizontal_alpha

    horizontal_nodal(form.diagram, force.diagram, kmax=kmax, alpha=alpha)

    bbox_form = Box.from_bounding_box(bounding_box(form.diagram.vertices_attributes("xyz")))
    bbox_force = Box.from_bounding_box(bounding_box(force.diagram.vertices_attributes("xyz")))

    y_form = bbox_form.ymin + 0.5 * (bbox_form.ymax - bbox_form.ymin)
    y_force = bbox_force.ymin + 0.5 * (bbox_force.ymax - bbox_force.ymin)
    dx = 1.3 * (bbox_form.xmax - bbox_form.xmin) + (bbox_form.xmin - bbox_force.xmin)
    dy = y_form - y_force

    force.diagram.translate([dx, dy, 0])

    # =============================================================================
    # Update scene
    # =============================================================================

    max_angle = max(form.diagram.edges_attribute("_a"))
    tol_angles = session.settings.tna.horizontal_max_angle

    if max_angle < tol_angles:
        print(f"Horizontal equilibrium found!\nMaximum angle deviation: {max_angle} < {tol_angles}")
    else:
        rs.MessageBox(f"Horizontal equilibrium NOT found! Consider running more iterations.\nMaximum angle deviation: {max_angle} > {tol_angles}")

    rs.UnselectAllObjects()

    session.scene.redraw()
    rs.Redraw()

    if session.settings.autosave:
        session.record(name="TNA Horizontal")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
