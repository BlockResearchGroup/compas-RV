from typing import Optional

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


def make_pattern_from_rhinolines() -> Optional[Pattern]:
    guids = compas_rhino.objects.select_lines("Select lines")
    if not guids:
        return

    lines = compas_rhino.objects.get_line_coordinates(guids)
    if not lines:
        return

    pattern: Pattern = Pattern.from_lines(lines, delete_boundary_face=True)  # type: ignore

    rs.HideObjects(guids)

    return pattern


def make_pattern_from_rhinomesh() -> Optional[Pattern]:
    guid = compas_rhino.objects.select_mesh("Select a mesh")
    if not guid:
        return

    obj = compas_rhino.objects.find_object(guid)
    pattern: Pattern = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=Pattern)  # type: ignore

    rs.HideObject(guid)

    return pattern


def make_pattern_from_rhinosurface() -> Optional[Pattern]:
    guid = compas_rhino.objects.select_surface("Select a surface")
    if not guid:
        return

    U = rs.GetInteger(message="U faces", number=16, minimum=2, maximum=64)
    if not U:
        return

    V = rs.GetInteger(message="V faces", number=4, minimum=2, maximum=64)
    if not V:
        return

    obj = compas_rhino.objects.find_object(guid)
    brep = obj.Geometry
    surface = brep.Surfaces[0]
    pattern: Pattern = compas_rhino.conversions.surface_to_compas_mesh(surface, nu=U, nv=V, weld=True, cls=Pattern)  # type: ignore

    rs.HideObject(guid)

    return pattern


def make_pattern_from_meshgrid() -> Optional[Pattern]:
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

    pattern: Pattern = Pattern.from_meshgrid(dx=DX, nx=NX, dy=DY, ny=NY)  # type: ignore
    return pattern


def make_pattern_from_triangulation() -> Optional[Pattern]:
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
    curves = None  # type: ignore

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


def make_pattern_from_skeleton() -> Optional[Pattern]:
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

    return pattern
