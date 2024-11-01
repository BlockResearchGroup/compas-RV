#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.1, compas_session>=0.4.1, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import Pattern
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    pattern = session.scene.find_by_itemtype(Pattern)
    if not pattern:
        return

    # =============================================================================
    # Update openings
    # =============================================================================

    rs.UnselectAllObjects()

    # =============================================================================
    # Update scene
    # =============================================================================

    # =============================================================================
    # Save session
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Update Pattern Openings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
