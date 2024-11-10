#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_tna==0.5.2

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
