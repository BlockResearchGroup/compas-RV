#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

import pathlib

from compas_rui.forms import FileForm
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    basedir = session.basedir or pathlib.Path().home()
    filepath = FileForm.save(str(basedir), "RhinoVAULT.json")
    if not filepath:
        return

    session.dump(filepath)


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
