#! python3

from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")

    scene = session.scene()

    if session.redo():
        scene.clear()
        scene = session.scene()
        scene.draw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
