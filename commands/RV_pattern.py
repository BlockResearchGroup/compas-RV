#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.commands import make_pattern_from_meshgrid
from compas_rv.commands import make_pattern_from_rhinolines
from compas_rv.commands import make_pattern_from_rhinomesh
from compas_rv.commands import make_pattern_from_rhinosurface
from compas_rv.commands import make_pattern_from_skeleton
from compas_rv.commands import make_pattern_from_triangulation
from compas_rv.commands import make_pattern_from_template
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

    if form or force:
        return session.warn("Please remove all form and force diagrams before using pattern commands.")

    patternobj = session.find_pattern(warn=False)

    if patternobj:
        if not session.confirm("This will remove all current RhinoVAULT data and objects. Do you wish to proceed?"):
            return

    session.scene.clear()

    # =============================================================================
    # Make a Force "Pattern"
    # =============================================================================

    option = rs.GetString(
        message="Pattern From",
        strings=[
            "RhinoLines",
            "RhinoMesh",
            "RhinoSurface",
            "MeshGrid",
            "Triangulation",
            "Skeleton",
            "Json",
            "Template",
        ],
    )

    if option == "RhinoLines":
        pattern = make_pattern_from_rhinolines()

    elif option == "RhinoMesh":
        pattern = make_pattern_from_rhinomesh()

    elif option == "RhinoSurface":
        pattern = make_pattern_from_rhinosurface()

    elif option == "MeshGrid":
        pattern = make_pattern_from_meshgrid()

    elif option == "Triangulation":
        pattern = make_pattern_from_triangulation()

    elif option == "Skeleton":
        pattern = make_pattern_from_skeleton()

    elif option == "Json":
        raise NotImplementedError

    elif option == "Template":
        pattern = make_pattern_from_template()

    else:
        return

    # =============================================================================
    # Update scene
    # =============================================================================

    session.scene.add(pattern, name=pattern.name, layer="RhinoVAULT::Pattern")  # type: ignore
    session.scene.draw()

    print("Pattern successfully created.")

    if session.settings.autosave:
        session.record(name="Make Pattern")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
