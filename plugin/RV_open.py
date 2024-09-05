#! python3

from compas_rui.forms import FileForm
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")

    filepath = FileForm.open(session.basedir)
    if not filepath:
        return

    scene = session.scene()
    scene.clear()

    session.open(filepath)

    scene = session.scene()
    scene.draw()

    if session.CONFIG["autosave.events"]:
        session.record(eventname="Open Session")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
