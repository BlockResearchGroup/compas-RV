#! python3
# venv: rhinovault
# r: compas_session==0.4.5, compas_tna==0.5.2

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas_rv.datastructures import Pattern
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

    option = rs.GetString(message="Pattern From", strings=["RhinoLines", "RhinoMesh", "RhinoSurface", "MeshGrid", "Triangulation"])

    if option == "RhinoLines":
        guids = compas_rhino.objects.select_lines("Select lines")
        if not guids:
            return

        lines = compas_rhino.objects.get_line_coordinates(guids)
        if not lines:
            return

        pattern = Pattern.from_lines(lines, delete_boundary_face=True)

        rs.HideObjects(guids)

    elif option == "RhinoMesh":
        guid = compas_rhino.objects.select_mesh("Select a mesh")
        if not guid:
            return

        obj = compas_rhino.objects.find_object(guid)
        pattern = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=Pattern)

        rs.HideObject(guid)

    elif option == "RhinoSurface":
        guid = compas_rhino.objects.select_surface("Select a surface")
        if not guid:
            return

        U = rs.GetInteger(message="U faces", number=16, minimum=2, maximum=64)
        if not U:
            return

        V = rs.GetInteger(message="V faces", number=4, minimum=2, maximum=64)
        if not V:
            return

        # ------------------------------------------------

        obj = compas_rhino.objects.find_object(guid)
        brep = obj.Geometry
        surface = brep.Surfaces[0]

        # ------------------------------------------------

        pattern = compas_rhino.conversions.surface_to_compas_mesh(surface, nu=U, nv=V, weld=True, cls=Pattern)

        rs.HideObject(guid)

    elif option == "MeshGrid":
        DX = rs.GetInteger(message="X Size", number=10)
        if not DX:
            return

        DY = rs.GetInteger(message="Y Size", number=DX)
        if not DY:
            return

        NX = rs.GetInteger(message="Number of faces in X", number=10)
        if not NX:
            return

        NY = rs.GetInteger(message="Number of faces in Y", number=NX)
        if not NY:
            return

        pattern = Pattern.from_meshgrid(dx=DX, nx=NX, dy=DY, ny=NY)

    elif option == "Triangulation":
        raise NotImplementedError

    else:
        return

    # =============================================================================
    # Update scene
    # =============================================================================

    session.scene.add(pattern, name=pattern.name)
    session.scene.draw()

    print("Pattern successfully created.")

    if session.settings.autosave:
        session.record(name="Make Pattern")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
