#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui==0.4.1, compas_session==0.4.4, compas_tna==0.5.1, compas_fd==0.5.3

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    oldscene = session.scene

    if not session.undo():
        return

    oldscene.clear()
    session.scene.draw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
