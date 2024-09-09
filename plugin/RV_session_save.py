#! python3

from compas_rui.forms import FileForm
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")

    filepath = FileForm.save(session.basedir, "RhinoVAULT.json")
    if not filepath:
        return

    session.save(filepath)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
