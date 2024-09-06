#! python3

import rhinoscriptsyntax as rs  # type: ignore

import compas_rv.settings
from compas_rv.datastructures import Pattern
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    pattern = scene.find_by_itemtype(itemtype=Pattern)
    if not pattern:
        return

    # =============================================================================
    # Modify pattern vertices
    # =============================================================================

    rs.UnselectAllObjects()

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_anchors = True
    pattern.show_fixed = True
    pattern.show_free = False
    pattern.show_edges = False

    rs.EnableRedraw(False)
    pattern.clear()
    pattern.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="Modify Force diagram")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
