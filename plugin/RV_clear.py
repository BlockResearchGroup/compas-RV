#! python3

import rhinoscriptsyntax as rs  # type: ignore

from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    result = rs.MessageBox(
        "Note that this will remove all RhinoVAULT data and objects. Do you wish to proceed?",
        buttons=4 | 32 | 256 | 0,
        title="Clear RhinoVAULT",
    )

    if result == 6:
        scene.clear()

        if session.CONFIG["autosave.events"]:
            session.record(eventname="Clear")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)