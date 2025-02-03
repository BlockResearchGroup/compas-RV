#! python3
# venv: brg-csd
# r: compas_rv>=0.5.0

from compas_rui.forms import FileForm
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    filepath = FileForm.save(session.basedir, "RhinoVAULT.json")
    if not filepath:
        return

    session.dump(filepath)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
