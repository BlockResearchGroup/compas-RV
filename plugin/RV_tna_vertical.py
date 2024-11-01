#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.1, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import ThrustDiagram
from compas_rv.scene import RhinoFormObject
from compas_rv.scene import RhinoThrustObject
from compas_rv.session import RVSession
from compas_tna.equilibrium import vertical_from_zmax


def RunCommand():
    session = RVSession()

    formobj: RhinoFormObject = session.scene.find_by_itemtype(FormDiagram)
    if not formobj:
        return

    # =============================================================================
    # Compute horizontal
    # =============================================================================

    kmax = session.settings.tna.vertical.kmax
    zmax = session.settings.tna.vertical.zmax
    zmax = rs.GetReal("Set maximum height (zmax)", number=zmax, minimum=0)

    # warn the user about nonsensical values

    _, scale = vertical_from_zmax(formobj.mesh, zmax, kmax=kmax)

    # store scale in force diagram

    thrust: ThrustDiagram = formobj.mesh.copy(cls=ThrustDiagram)
    thrust.name = "ThrustDiagram"

    formobj.mesh.vertices_attribute(name="z", value=0)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    thrustobj = session.scene.find_by_itemtype(ThrustDiagram)

    if not thrustobj:
        thrustobj: RhinoThrustObject = session.scene.add(thrust, name=thrust.name)
    else:
        thrustobj.mesh = thrust

    thrustobj.clear()
    thrustobj.draw()
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="TNA Vertical")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
