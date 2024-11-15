#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_tna==0.5.2

from compas_rui.forms import FileForm
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    filepath = FileForm.open(session.basedir)
    if not filepath:
        return

    session.scene.clear()
    session.load(filepath)

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

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
