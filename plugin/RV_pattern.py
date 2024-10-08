#! python3
# venv: rhinovault
# r: compas>=2.4, compas_rui, compas_session, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
import compas_rv.settings
from compas_rv.datastructures import Pattern
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")

    scene = session.scene()

    patternobj = scene.find_by_itemtype(itemtype=Pattern)

    if patternobj:
        result = rs.MessageBox(
            "This will remove all current RhinoVAULT data and objects. Do you wish to proceed?",
            buttons=4 | 32 | 256 | 0,
            title="RhinoVAULT",
        )
        if result == 6:
            scene.clear()
        else:
            return

    else:
        scene.clear()

    # =============================================================================
    # Make a Force "Pattern"
    # =============================================================================

    option = rs.GetString(message="CableMesh From", strings=["RhinoLines", "RhinoMesh", "RhinoSurface", "MeshGrid", "Triangulation"])

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

    scene.add(pattern, name=pattern.name)
    scene.draw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(name="Make Pattern")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
