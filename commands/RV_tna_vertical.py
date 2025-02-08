#! python3
# venv: brg-csd
# r: compas_rv>=0.8.1


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import ThrustDiagram
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

    thrust = session.find_thrustdiagram()
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    # =============================================================================
    # Compute horizontal
    # =============================================================================

    kmax = session.settings.tna.vertical_kmax
    zmax = session.settings.tna.vertical_zmax

    zmax = rs.GetReal("Set maximum height (zmax)", number=zmax, minimum=0)
    if zmax is None:
        return

    session.settings.tna.vertical_zmax = zmax

    # copy the vertical coordinates of the thrust diagram onto the form diagram
    for vertex in thrust.diagram.vertices_where(is_support=True):
        z = thrust.diagram.vertex_attribute(vertex, "z")
        form.diagram.vertex_attribute(vertex, "z", z)

    _, scale = vertical_from_zmax(form.diagram, zmax, kmax=kmax)

    if not _:  # this makes no sense
        print("Vertical equilibrium failed!")
        return

    force.diagram.attributes["scale"] = scale

    thrustdiagram: ThrustDiagram = form.diagram.copy(cls=ThrustDiagram)
    thrustdiagram.name = "ThrustDiagram"

    # flatten the formdiagram again
    form.diagram.vertices_attribute(name="z", value=0)

    # show the thrust diagram
    thrust.show = True

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    thrust.diagram = thrustdiagram
    thrust.redraw()

    print("Vertical equilibrium found!")
    print("ThrustDiagram object successfully created with target height of {}.".format(zmax))

    if session.settings.autosave:
        session.record(name="TNA Vertical")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
