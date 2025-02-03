#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_rui==0.4.2, compas_tna==0.5.2, compas_rv==0.5.0

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    if session.confirm("Note that this will remove all RhinoVAULT data and objects. Do you wish to proceed?"):
        session.scene.clear()

        if session.settings.autosave:
            session.record(name="Clear")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
