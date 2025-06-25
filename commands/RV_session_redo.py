#! python3
# venv: brg-csd
# r: compas_rv>=0.9.3, tessagon

from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    oldscene = session.scene

    if not session.redo():
        return

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

    if form and force:
        form.diagram.dual = force.diagram
        force.diagram.primal = form.diagram

    oldscene.clear()
    session.scene.draw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
