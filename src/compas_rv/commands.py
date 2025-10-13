from typing import Optional

import rhinoscriptsyntax as rs  # type: ignore
from compas_skeleton.datastructures import Skeleton
from compas_triangle.delaunay import conforming_delaunay_triangulation
from compas_triangle.rhino import discretise_boundary
from compas_triangle.rhino import discretise_constraints

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.datastructures import Mesh
from compas.geometry import NurbsCurve
from compas.geometry import Point
from compas_rv.datastructures import Pattern
from compas_tna.diagrams.diagram_circular import create_circular_radial_mesh
from compas_tna.diagrams.diagram_circular import create_circular_radial_spaced_mesh
from compas_tna.diagrams.diagram_circular import create_circular_spiral_mesh
from compas_tna.diagrams.diagram_rectangular import create_cross_mesh
from compas_tna.diagrams.diagram_rectangular import create_fan_mesh
from compas_tna.diagrams.diagram_rectangular import create_ortho_mesh
from compas_tna.diagrams.diagram_rectangular import create_parametric_fan_mesh


def get_location():
    option = rs.GetString("Pattern Location", strings=["Origin", "Coordinates", "Point"])
    if not option:
        return

    if option == "Origin":
        point = (0, 0)

    elif option == "Coordinates":
        x = rs.GetReal("X", 0.0, -1000.0, 1000.0)
        if x is None:
            return

        y = rs.GetReal("Y", 0.0, -1000.0, 1000.0)
        if y is None:
            return

        point = (x, y)

    elif option == "Point":
        point = rs.GetPoint("Point")
        if not point:
            return

    else:
        raise NotImplementedError

    return point[0], point[1]


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


def make_pattern_from_template() -> Optional[Pattern]:
    option = rs.GetString(
        message="Template Name",
        strings=[
            "Radial",
            "RadialSpaced",
            "Spiral",
            "Cross",
            "Fan",
            "Ortho",
            "Parametric",
        ],
    )
    if not option:
        return

    if option == "Radial":
        pattern = make_pattern_radial()
    elif option == "RadialSpaced":
        pattern = make_pattern_radial_spaced()
    elif option == "Spiral":
        pattern = make_pattern_spiral()
    elif option == "Cross":
        pattern = make_pattern_cross()
    elif option == "Fan":
        pattern = make_pattern_fan()
    elif option == "Ortho":
        pattern = make_pattern_ortho()
    elif option == "Parametric":
        pattern = make_pattern_parametric()
    else:
        NotImplementedError

    return pattern


def make_pattern_radial() -> Optional[Pattern]:
    center = get_location()
    if not center:
        return

    radius = rs.GetReal("Radius", number=1.0, minimum=0.0)
    if not radius:
        return

    rings = rs.GetInteger("Rings", 8, 4, 32)
    if not rings:
        return

    radials = rs.GetInteger("Radials", 24, 12, 64)
    if not radials:
        return

    oculus = rs.GetReal("Oculus", number=0.3, minimum=0.0)
    if not oculus:
        return

    pattern = create_circular_radial_mesh(
        center=center,
        radius=radius,
        n_hoops=rings,
        n_parallels=radials,
        r_oculus=oculus,
    ).copy(cls=Pattern)  # type: ignore

    return pattern


def make_pattern_radial_spaced() -> Optional[Pattern]:
    center = get_location()
    if not center:
        return

    radius = rs.GetReal("Radius", number=1.0, minimum=0.0)
    if not radius:
        return

    rings = rs.GetInteger("Rings", 8, 4, 32)
    if not rings:
        return

    radials = rs.GetInteger("Radials", 24, 12, 64)
    if not radials:
        return

    oculus = rs.GetReal("Oculus", number=0.3, minimum=0.0)
    if not oculus:
        return

    pattern = create_circular_radial_spaced_mesh(
        center=center,
        radius=radius,
        n_hoops=rings,
        n_parallels=radials,
        r_oculus=oculus,
    ).copy(cls=Pattern)  # type: ignore

    return pattern


def make_pattern_spiral() -> Optional[Pattern]:
    center = get_location()
    if not center:
        return

    radius = rs.GetReal("Radius", number=1.0, minimum=0.0)
    if not radius:
        return

    rings = rs.GetInteger("Rings", 8, 4, 32)
    if not rings:
        return

    radials = rs.GetInteger("Radials", 24, 12, 64)
    if not radials:
        return

    oculus = rs.GetReal("Oculus", number=0.3, minimum=0.0)
    if not oculus:
        return

    pattern = create_circular_spiral_mesh(
        center=center,
        radius=radius,
        n_hoops=rings,
        n_parallels=radials,
        r_oculus=oculus,
    ).copy(cls=Pattern)  # type: ignore

    return pattern


def make_pattern_cross() -> Optional[Pattern]:
    point = get_location()
    if not point:
        return

    x_size = rs.GetReal("X Size", 10, 0.0, 1000)
    if not x_size:
        return

    y_size = rs.GetReal("Y Size", 10, 0.0, 1000)
    if not y_size:
        return

    n = rs.GetInteger("Resolution", 10, 0)
    if not n:
        return

    x_span = (point[0], point[0] + x_size)
    y_span = (point[1], point[1] + y_size)

    pattern = create_cross_mesh(
        x_span=x_span,
        y_span=y_span,
        n=n,
    ).copy(cls=Pattern)  # type: ignore

    return pattern


def make_pattern_fan() -> Optional[Pattern]:
    point = get_location()
    if not point:
        return

    x_size = rs.GetReal("X Size", 10, 0.0, 1000)
    if not x_size:
        return

    y_size = rs.GetReal("Y Size", 10, 0.0, 1000)
    if not y_size:
        return

    n_fans = rs.GetInteger("Number of Fans", 10, 2)
    if not n_fans:
        return

    n_hoops = rs.GetInteger("Number of Hoops", n_fans, 2)
    if not n_hoops:
        return

    x_span = (point[0], point[0] + x_size)
    y_span = (point[1], point[1] + y_size)

    pattern = create_fan_mesh(
        x_span=x_span,
        y_span=y_span,
        n_fans=n_fans,
        n_hoops=n_hoops,
    ).copy(cls=Pattern)  # type: ignore

    return pattern


def make_pattern_ortho() -> Optional[Pattern]:
    point = get_location()
    if not point:
        return

    x_size = rs.GetReal("X Size", 10, 0.0, 1000)
    if not x_size:
        return

    y_size = rs.GetReal("Y Size", 10, 0.0, 1000)
    if not y_size:
        return

    nx = rs.GetInteger("Number of X Faces", 10, 2)
    if not nx:
        return

    ny = rs.GetInteger("Number of Y Faces", nx, 2)
    if not ny:
        return

    x_span = (point[0], point[0] + x_size)
    y_span = (point[1], point[1] + y_size)

    pattern = create_ortho_mesh(
        x_span=x_span,
        y_span=y_span,
        nx=nx,
        ny=ny,
    ).copy(cls=Pattern)  # type: ignore

    return pattern


def make_pattern_parametric() -> Optional[Pattern]:
    point = get_location()
    if not point:
        return

    x_size = rs.GetReal("X Size", 10, 0.0, 1000)
    if not x_size:
        return

    y_size = rs.GetReal("Y Size", 10, 0.0, 1000)
    if not y_size:
        return

    n = rs.GetInteger("Resolution", 10, 2)
    if not n:
        return

    lambd = rs.GetReal("Lambda Inclination [0-1]", number=0.5, minimum=0.0, maximum=1.0)
    if lambd is None:
        return

    x_span = (point[0], point[0] + x_size)
    y_span = (point[1], point[1] + y_size)

    pattern = create_parametric_fan_mesh(
        x_span=x_span,
        y_span=y_span,
        n=n,
        lambd=lambd,
    ).copy(cls=Pattern)  # type: ignore

    return pattern
