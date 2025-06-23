#! python3
# venv: brg-csd
# r: compas_rv>=0.9.1

import rhinoscriptsyntax as rs  # type: ignore
from compas_dem.models import BlockModel

from compas.datastructures import Mesh
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    thrust = session.find_thrustdiagram()
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    option = rs.GetString(message="DEM Blocks From", strings=["Dual", "MeshPattern"])

    if option == "Dual":
        mesh: Mesh = thrust.diagram.copy()
        for face in list(mesh.faces_where(_is_loaded=False)):
            mesh.delete_face(face)
        model = BlockModel.from_meshdual(mesh)

    elif option == "MeshPattern":
        raise NotImplementedError

    else:
        raise NotImplementedError

    # =============================================================================
    # Scene
    # =============================================================================

    for block in model.blocks():
        session.scene.add(block.modelgeometry)

    session.scene.redraw()

    # =============================================================================
    # Autosave
    # =============================================================================

    if session.settings.autosave:
        session.record(name="Create BlockModel")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
