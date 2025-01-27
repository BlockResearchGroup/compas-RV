#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_tna==0.5.2

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    session.scene.redraw()
    rs.Redraw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
