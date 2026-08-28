#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

from compas_rui.forms.meshinfo import MeshInfoForm
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    form_info = MeshInfoForm(
        form.diagram,
        vertex_attr_names=["x", "y", "z", "px", "py", "pz", "is_support", "_rx", "_ry", "_rz"],
        edge_attr_names=["q"],
        face_attr_names=["_is_loaded"],
        title="Form Diagram Info (3D Thrust Surface)",
    )

    form_info.show()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
