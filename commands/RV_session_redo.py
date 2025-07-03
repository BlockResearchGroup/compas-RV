#! python3
# venv: brg-csd
# r: compas_rv>=0.9.4

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    oldscene = session.scene

    if not session.redo():
        return

    pattern = session.find_pattern(warn=False)
    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)
    thrust = session.find_thrustdiagram(warn=False)

    if pattern:
        pattern.layer = "RhinoVAULT::Pattern"

    if form:
        form.layer = "RhinoVAULT::FormDiagram"

    if force:
        force.layer = "RhinoVAULT::ForceDiagram"

    if thrust:
        thrust.layer = "RhinoVAULT::ThrustDiagram"

    if form and force:
        form.diagram.dual = force.diagram
        force.diagram.primal = form.diagram

    oldscene.clear()
    session.scene.draw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
