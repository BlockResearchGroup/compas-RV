#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

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
