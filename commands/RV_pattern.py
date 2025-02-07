#! python3
# venv: brg-csd
# r: compas_rv>=0.7.0

import rhinoscriptsyntax as rs  # type: ignore
from compas_skeleton.datastructures import Skeleton
from compas_triangle.delaunay import conforming_delaunay_triangulation
from compas_triangle.rhino import discretise_boundary
from compas_triangle.rhino import discretise_constraints

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.geometry import NurbsCurve
from compas.geometry import Point
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

    option = rs.GetString(
        message="Pattern From",
        strings=[
            "RhinoLines",
            "RhinoMesh",
            "RhinoSurface",
            "MeshGrid",
            "Triangulation",
            "Skeleton",
        ],
    )

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
        boundary_guids = compas_rhino.objects.select_curves("Select outer boundary.")
        if not boundary_guids:
            return

        rs.UnselectAllObjects()
        hole_guids = compas_rhino.objects.select_curves("Select inner boundaries.")

        rs.UnselectAllObjects()
        segments_guids = compas_rhino.objects.select_curves("Select constraint curves.")

        rs.UnselectAllObjects()

        target_length = rs.GetReal("Specifiy target edge length.", 1.0)
        if not target_length:
            return

        boundary = discretise_boundary(boundary_guids, target_length)
        holes = None
        segments = None
        curves = None

        if hole_guids:
            holes = discretise_constraints(hole_guids, target_length)

        if segments_guids:
            segments = discretise_constraints(segments_guids, target_length)
            curves: list[NurbsCurve] = [NurbsCurve.from_interpolation(segment) for segment in segments]

        points, triangles = conforming_delaunay_triangulation(
            boundary,
            polylines=segments,
            polygons=holes,
            area=target_length**2 / 2,
        )
        pattern = Pattern.from_vertices_and_faces(points, triangles)

        fixed = [vertex for boundary in pattern.vertices_on_boundaries() for vertex in boundary]
        if curves:
            for index, point in enumerate(points):
                for curve in curves:
                    closest: Point = curve.closest_point(point)
                    if closest.distance_to_point(point) < 0.1 * target_length:
                        fixed.append(index)

        pattern.smooth_area(fixed=fixed)

    elif option == "Skeleton":
        guids = compas_rhino.objects.select_lines("Select skeleton lines.")
        if not guids:
            return

        rs.UnselectAllObjects()

        width = rs.GetReal("Specifiy skeleton width.", 1.0)
        if not width:
            return

        angle = rs.GetReal("Specifiy skeleton leaf angle (degrees).", 30)
        if not angle:
            return

        density = rs.GetInteger("Specifiy skeleton density.", 2)
        if not density:
            return

        objects = [compas_rhino.objects.find_object(guid) for guid in guids]
        curves = [obj.Geometry for obj in objects]
        lines = [compas_rhino.conversions.curve_to_compas_line(curve) for curve in curves]

        skeleton = Skeleton(lines)
        skeleton.node_width = width
        skeleton.leaf_angle = angle
        skeleton.density = density
        pattern = skeleton.pattern.copy(cls=Pattern)

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
