#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.1, compas_session>=0.4.1, compas_tna>=0.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    result = rs.MessageBox(
        "Note that this will remove all RhinoVAULT data and objects. Do you wish to proceed?",
        buttons=4 | 32 | 256 | 0,
        title="Clear RhinoVAULT",
    )
    if result == 6:
        session.scene.clear()

        if session.settings.autosave:
            session.record(name="Clear")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
