#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import ForceDiagram
from compas_rv.session import RVSession
from compas_rv.solvers import update_force_from_form


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

    update_force_from_form(forcediagram, form.diagram)

    forcediagram.update_position()
    forcediagram.update_angle_deviations()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.add(forcediagram, name=forcediagram.name, layer="RhinoVAULT::ForceDiagram")  # type: ignore
    session.scene.redraw()

    rs.Redraw()

    print("ForceDiagram successfully created.")

    if session.settings.autosave:
        session.record(name="Create Force Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
