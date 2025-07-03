#! python3
# venv: brg-csd
# r: compas_rv>=0.9.4

import pathlib

from compas_rui.forms import FileForm
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    basedir = session.basedir or pathlib.Path().home()
    filepath = FileForm.open(str(basedir))
    if not filepath:
        return

    session.scene.clear()
    session.load(filepath)

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

    session.scene.draw()

    if session.settings.autosave:
        session.record(name="Open Session")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
