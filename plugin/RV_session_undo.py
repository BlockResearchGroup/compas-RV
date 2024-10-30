#! python3
# venv: rhinovault
# r: compas, compas_rui, compas_rv, compas_session, compas_tna


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
