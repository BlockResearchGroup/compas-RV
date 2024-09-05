#! python3

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.datastructures import Pattern
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    pattern = scene.find_by_itemtype(itemtype=Pattern)
    if not pattern:
        return

    # =============================================================================
    # Modify pattern edges
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

    if session.CONFIG["autosave.events"]:
        session.record(eventname="Modify Pattern Edges")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
