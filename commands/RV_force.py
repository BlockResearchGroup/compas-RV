#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_tna==0.5.2


import rhinoscriptsyntax as rs  # type: ignore

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

    forcediagram.update_position()
    forcediagram.update_angle_deviations()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    session.scene.add(forcediagram, name=forcediagram.name)
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