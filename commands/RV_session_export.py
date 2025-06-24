#! python3
# venv: brg-csd
# r: compas_rv>=0.9.2

import pathlib

import rhinoscriptsyntax as rs  # type: ignore

import compas
from compas.datastructures import Mesh
from compas_rui.forms import FileForm
from compas_rv.session import RVSession


def RunCommand():
    session = RVSession()

    option = rs.GetString(
        message="Export",
        strings=[
            "Pattern",
            "FormDiagram",
            "ForceDiagram",
            "ThrustDiagram",
        ],
    )

    if option == "Pattern":
        pattern = session.find_pattern()
        if not pattern:
            return

        mesh: Mesh = pattern.mesh.copy()
        for face in list(mesh.faces_where(_is_loaded=False)):
            mesh.delete_face(face)

        basedir = session.basedir or pathlib.Path().home()
        basename = "Pattern.json"
        filepath = FileForm.save(str(basedir), basename)
        if not filepath:
            return

        compas.json_dump(mesh, filepath)

    elif option == "FormDiagram":
        form = session.find_formdiagram()
        if not form:
            return

        mesh: Mesh = form.diagram.copy()
        for face in list(mesh.faces_where(_is_loaded=False)):
            mesh.delete_face(face)

        basedir = session.basedir or pathlib.Path().home()
        basename = "FormDiagram.json"
        filepath = FileForm.save(str(basedir), basename)
        if not filepath:
            return

        compas.json_dump(mesh, filepath)

    elif option == "ForceDiagram":
        force = session.find_forcediagram()
        if not force:
            return

        mesh: Mesh = force.diagram.copy()
        basedir = session.basedir or pathlib.Path().home()
        basename = "ForceDiagram.json"
        filepath = FileForm.save(str(basedir), basename)
        if not filepath:
            return

        compas.json_dump(mesh, filepath)

    elif option == "ThrustDiagram":
        thrust = session.find_thrustdiagram()
        if not thrust:
            return

        mesh: Mesh = thrust.diagram.copy()
        for face in list(mesh.faces_where(_is_loaded=False)):
            mesh.delete_face(face)

        basedir = session.basedir or pathlib.Path().home()
        basename = "ThrustDiagram.json"
        filepath = FileForm.save(str(basedir), basename)
        if not filepath:
            return

        compas.json_dump(mesh, filepath)

    else:
        raise NotImplementedError


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
