#! python3
# venv: brg-csd
# r: compas_rv>=0.9.3, tessagon

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import ThrustDiagram
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    pattern = session.find_pattern(warn=False)
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    if not list(pattern.mesh.vertices_where(is_support=True)):
        print("Pattern has no supports! Please define supports vertices.")
        return

    form = session.find_formdiagram(warn=False)
    if form:
        print("FormDiagram already exists in the scene.")
        return

    session.clear_all_formdiagrams()

    # =============================================================================
    # Init the form diagram
    # =============================================================================

    rs.UnselectAllObjects()

    formdiagram = FormDiagram.from_pattern(pattern.mesh)
    formdiagram.name = "FormDiagram"

    formdiagram.vertices_attribute(name="z", value=0)
    formdiagram.flip_cycles_if_normal_down()

    thrustdiagram: ThrustDiagram = formdiagram.copy(cls=ThrustDiagram)
    thrustdiagram.name = "ThrustDiagram"

    # set an initial value for zmax
    session.settings.tna.vertical_zmax = thrustdiagram.compute_zmax()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show = False

    session.scene.add(formdiagram, name=formdiagram.name)  # type: ignore
    session.scene.add(thrustdiagram, name=thrustdiagram.name, show=False)  # type: ignore
    session.scene.redraw()
    rs.Redraw()

    print("FormDiagram successfully created.")

    if session.settings.autosave:
        session.record(name="Init Form Diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
