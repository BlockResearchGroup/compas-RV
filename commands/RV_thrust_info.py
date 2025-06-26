#! python3
# venv: brg-csd
# r: compas_rv>=0.9.4

from compas_rui.forms.meshinfo import MeshInfoForm
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    thrust = session.find_thrustdiagram()
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    form = MeshInfoForm(
        thrust.diagram,
        vertex_attr_names=["x", "y", "z", "px", "py", "pz", "is_support", "_rx", "_ry", "_rz"],
        edge_attr_names=["q"],
        face_attr_names=["_is_loaded"],
        title="Thrust Diagram Info",
    )

    form.show()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
