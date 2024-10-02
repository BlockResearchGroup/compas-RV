#! python3
# venv: rhinovault
# r: compas>=2.4, compas_rui, compas_session, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas.scene import Scene
from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import ThrustDiagram
from compas_rv.scene import RhinoFormObject
from compas_session.namedsession import NamedSession
from compas_tna.equilibrium import vertical_from_zmax


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene: Scene = session.scene()

    formobj: RhinoFormObject = scene.find_by_itemtype(itemtype=FormDiagram)
    if not formobj:
        return

    form: FormDiagram = formobj.mesh

    # =============================================================================
    # Compute horizontal
    # =============================================================================

    kmax = compas_rv.settings.SETTINGS["TNA"]["vertical.kmax"]
    zmax = compas_rv.settings.SETTINGS["TNA"]["vertical.zmax"]
    zmax = rs.GetReal("Set maximum height (zmax)", number=zmax, minimum=0)

    # warn the user about nonsensical values

    _, scale = vertical_from_zmax(form, zmax, kmax=kmax)

    # store scale in force diagram

    thrust: ThrustDiagram = form.copy(cls=ThrustDiagram)
    thrust.name = "ThrustDiagram"

    form.vertices_attribute(name="z", value=0)

    # =============================================================================
    # Update scene
    # =============================================================================

    thrustobj = scene.find_by_itemtype(itemtype=ThrustDiagram)

    if not thrustobj:
        thrustobj = scene.add(thrust, name=thrust.name)
    else:
        thrustobj.mesh = thrust

    rs.UnselectAllObjects()
    rs.EnableRedraw(False)
    thrustobj.clear()
    thrustobj.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(name="TNA Vertical")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
