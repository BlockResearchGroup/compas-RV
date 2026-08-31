#! python3
# venv: brg-csd
# r: compas_rv>=0.10.1


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession
from compas_tna.equilibrium import vertical_from_zmax


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    force = session.find_forcediagram()
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    # =============================================================================
    # Compute vertical
    # =============================================================================

    kmax = session.settings.tna.vertical_kmax
    zmax = session.settings.tna.vertical_zmax

    zmax = rs.GetReal("Set maximum height (zmax)", number=zmax, minimum=0)
    if zmax is None:
        return

    session.settings.tna.vertical_zmax = zmax

    # Compute vertical equilibrium directly on the form diagram
    density = 0.0 if form.diagram.attributes.get("loads_from_envelope") else 1.0
    _, scale = vertical_from_zmax(form.diagram, zmax, kmax=kmax, density=density)

    force.diagram.attributes["scale"] = scale

    # Enable 3D mode for the form diagram to show the thrust surface
    form.show_thrust = True

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    # Redraw the form diagram to show the updated 3D geometry
    form.redraw()

    print("Vertical equilibrium found!")
    print("FormDiagram object updated with target height of {}.".format(zmax))

    if session.settings.autosave:
        session.record(name="TNA Vertical")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
