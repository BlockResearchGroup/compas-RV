import math

from compas.geometry import distance_point_point_xy
from compas.geometry import mirror_points_line
from compas.geometry import rotate_points_xy
from compas_rv.datastructures import Pattern


def mirror_4x(line, line_hor, line_ver, lines):
    """Helper to mirror an object 4 times."""
    lines.append(line)
    a_mirror, b_mirror = mirror_points_line(line, line_hor)
    lines.append([a_mirror, b_mirror])
    a_mirror, b_mirror = mirror_points_line([a_mirror, b_mirror], line_ver)
    lines.append([a_mirror, b_mirror])
    a_mirror, b_mirror = mirror_points_line(line, line_ver)
    lines.append([a_mirror, b_mirror])
    return lines


def mirror_8x(line, origin, line_hor, line_ver, lines):
    """Helper to mirror an object 8 times."""
    lines = mirror_4x(line, line_hor, line_ver, lines)
    rot = rotate_points_xy(line, math.pi / 2, origin=origin)
    lines = mirror_4x(rot, line_hor, line_ver, lines)
    return lines


def append_mirrored_lines(line, list_, line_hor, line_ver):
    """Helper to mirror an object 8 times and add to the list"""
    mirror_a = mirror_points_line(line, line_hor)
    mirror_b = mirror_points_line(mirror_a, line_ver)
    mirror_c = mirror_points_line(line, line_ver)
    list_.append(mirror_a)
    list_.append(mirror_b)
    list_.append(mirror_c)


def create_cross_pattern(
    xy_span=[[0.0, 10.0], [0.0, 10.0]],
    discretisation=10,
) -> Pattern:
    """Construct a FormDiagram based on cross discretiastion with orthogonal arrangement and diagonal.

    Parameters
    ----------
    xy_span : list, optional
        List with initial- and end-points of the vault, by default [[0.0, 10.0], [0.0, 10.0]]
    discretisation : int, optional
        Set the density of the grid in x and y directions, by default 10
    fix : str, optional
        Option to select the constrained nodes: 'corners', 'all' are accepted., by default 'corners'

    Returns
    -------
    :class:`~compas_tno.diagrams.FormDiagram`
        The FormDiagram created.

    Notes
    ----------------------
    Position of the quadrants is as in the schema below:

        Q3
    Q2      Q1
        Q4
    """
    if isinstance(discretisation, list):
        discretisation = discretisation[0]

    y1 = float(xy_span[1][1])
    y0 = float(xy_span[1][0])
    x1 = float(xy_span[0][1])
    x0 = float(xy_span[0][0])
    x_span = x1 - x0
    y_span = y1 - y0
    dx = x_span / discretisation
    dy = y_span / discretisation

    lines = []

    for i in range(discretisation + 1):
        for j in range(discretisation + 1):
            if i < discretisation and j < discretisation:
                # Vertical Members:
                xa = x0 + dx * i
                ya = y0 + dy * j
                xb = x0 + dx * (i + 1)
                yb = y0 + dy * j
                # Horizontal Members:
                xc = x0 + dx * i
                yc = y0 + dy * j
                xd = x0 + dx * i
                yd = y0 + dy * (j + 1)
                lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])
                lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
                if i == j:
                    # Diagonal Members in + Direction:
                    xc = x0 + dx * i
                    yc = y0 + dy * j
                    xd = x0 + dx * (i + 1)
                    yd = y0 + dy * (j + 1)
                    lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
                if i + j == discretisation:
                    # Diagonal Members in - Direction:
                    xc = x0 + dx * i
                    yc = y0 + dy * j
                    xd = x0 + dx * (i - 1)
                    yd = y0 + dy * (j + 1)
                    lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
                    if i == (discretisation - 1):
                        xc = x0 + dx * i
                        yc = y0 + dy * j
                        xd = x0 + dx * (i + 1)
                        yd = y0 + dy * (j - 1)
                        lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
            else:
                if i == discretisation and j < discretisation:
                    # Vertical Members on last column:
                    xa = x0 + dx * j
                    ya = y0 + dy * i
                    xb = x0 + dx * (j + 1)
                    yb = y0 + dy * i
                    # Horizontal Members:
                    xc = x0 + dx * i
                    yc = y0 + dy * j
                    xd = x0 + dx * i
                    yd = y0 + dy * (j + 1)
                    lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])
                    lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])

    pattern: Pattern = Pattern.from_lines(lines, delete_boundary_face=True)  # type: ignore
    return pattern


def create_cross_diagonal_pattern(
    xy_span=[[0.0, 10.0], [0.0, 10.0]],
    partial_bracing_modules=None,
    discretisation=10,
) -> Pattern:
    """Construct a FormDiagram based on a mixture of cross and fan discretiastion

    Parameters
    ----------
    xy_span : list, optional
        List with initial- and end-points of the vault, by default [[0.0, 10.0], [0.0, 10.0]]
    discretisation : int, optional
        Set the density of the grid in x and y directions, by default 10
    partial_bracing_modules : str, optional
        If partial bracing modules are included, by default None
    fix : str, optional
        Option to select the constrained nodes: 'corners', 'all' are accepted, by default 'corners'

    Returns
    -------
    :class:`~compas_tno.diagrams.FormDiagram`
        The FormDiagram created.

    """
    if isinstance(discretisation, list):
        discretisation = discretisation[0]

    y1 = float(xy_span[1][1])
    y0 = float(xy_span[1][0])
    x1 = float(xy_span[0][1])
    x0 = float(xy_span[0][0])
    x_span = x1 - x0
    y_span = y1 - y0
    dx = x_span / discretisation
    dy = y_span / discretisation

    xc0 = x0 + x_span / 2
    yc0 = y0 + y_span / 2

    nx = ny = int(discretisation / 2)
    if partial_bracing_modules is None:
        nstop = 0
    else:
        nstop = nx - partial_bracing_modules  # Test to stop

    line_hor = [[x0, yc0, 0.0], [xc0, yc0, 0.0]]
    line_ver = [[xc0, y0, 0.0], [xc0, yc0, 0.0]]
    origin = [xc0, yc0, 0.0]

    lines = []

    for i in range(nx):
        for j in range(ny + 1):
            if j <= i:
                if i >= nstop and j >= nstop:
                    # Diagonal Members:
                    xa = x0 + dx * i
                    ya = y0 + dy * 1 * (i - j) / (nx - j) + dy * j
                    xb = x0 + dx * (i + 1)
                    yb = y0 + dy * 1 * (i - j + 1) / (nx - j) + dy * j
                    lin = [[xa, ya, 0.0], [xb, yb, 0.0]]
                    lines = mirror_8x(lin, origin, line_hor, line_ver, lines)

                if i == j and i < nx - 1:
                    # Main diagonal:
                    xa = x0 + dx * i
                    ya = y0 + dy * j
                    xb = x0 + dx * (i + 1)
                    yb = y0 + dy * (j + 1)
                    lin = [[xa, ya, 0.0], [xb, yb, 0.0]]
                    lines = mirror_4x(lin, line_hor, line_ver, lines)

                # Horizontal Members:
                xa = x0 + dx * i
                ya = y0 + dy * j
                xb = x0 + dx * (i + 1)
                yb = y0 + dy * j
                lin = [[xa, ya, 0.0], [xb, yb, 0.0]]
                lines = mirror_8x(lin, origin, line_hor, line_ver, lines)

                i += 1
                # Vertical Members:
                xa = x0 + dx * i
                ya = y0 + dy * j
                xb = x0 + dx * i
                yb = y0 + dy * (j + 1)

                if i >= nstop and j >= nstop:
                    x_ = xa
                    y_ = y0 + dy * 1 * (i - j) / (nx - j) + dy * j
                    lin = [[xa, ya, 0.0], [x_, y_, 0.0]]
                    lines = mirror_8x(lin, origin, line_hor, line_ver, lines)
                    lin = [[x_, y_, 0.0], [xb, yb, 0.0]]
                    lines = mirror_8x(lin, origin, line_hor, line_ver, lines)
                else:
                    lin = [[xa, ya, 0.0], [xb, yb, 0.0]]
                    lines = mirror_8x(lin, origin, line_hor, line_ver, lines)

                i -= 1

    pattern: Pattern = Pattern.from_lines(lines, delete_boundary_face=True)  # type: ignore
    return pattern


def create_cross_with_diagonal_pattern(
    xy_span=[[0.0, 10.0], [0.0, 10.0]],
    discretisation=10,
) -> Pattern:
    """Construct a FormDiagram based on cross discretiastion with diagonals.

    Parameters
    ----------
    xy_span : list, optional
        List with initial- and end-points of the vault, by default [[0.0, 10.0], [0.0, 10.0]]
    discretisation : int, optional
        Set the density of the grid in x and y directions, by default 10
    fix : str, optional
        Option to select the constrained nodes: 'corners', 'all' are accepted, by default 'corners'

    Returns
    -------
    :class:`~compas_tno.diagrams.FormDiagram`
        The FormDiagram created.
    """

    if isinstance(discretisation, list):
        discretisation = discretisation[0]

    y1 = float(xy_span[1][1])
    y0 = float(xy_span[1][0])
    x1 = float(xy_span[0][1])
    x0 = float(xy_span[0][0])
    x_span = x1 - x0
    y_span = y1 - y0
    dx = x_span / discretisation
    dy = y_span / discretisation

    lines = []

    for i in range(discretisation + 1):
        for j in range(discretisation + 1):
            if i < discretisation and j < discretisation:
                # Hor Members:
                xa = x0 + dx * i
                ya = y0 + dy * j
                xb = x0 + dx * (i + 1)
                yb = y0 + dy * j
                # Ver Members:
                xc = x0 + dx * i
                yc = y0 + dy * j
                xd = x0 + dx * i
                yd = y0 + dy * (j + 1)
                lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])
                lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
                # lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
                if (i < discretisation / 2 and j < discretisation / 2) or (i >= discretisation / 2 and j >= discretisation / 2):
                    # Diagonal Members in + Direction:
                    xc = x0 + dx * i
                    yc = y0 + dy * j
                    xd = x0 + dx * (i + 1)
                    yd = y0 + dy * (j + 1)
                    lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
                else:
                    # Diagonal Members in - Direction:
                    xc = x0 + dx * i
                    yc = y0 + dy * (j + 1)
                    xd = x0 + dx * (i + 1)
                    yd = y0 + dy * j
                    lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
                    # if i == (discretisation - 1):
                    #     xc = x0 + dx*i
                    #     yc = y0 + dy*j
                    #     xd = x0 + dx*(i + 1)
                    #     yd = y0 + dy*(j - 1)
                    #     lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])
            else:
                if i == discretisation and j < discretisation:
                    # Vertical Members on last column:
                    xa = x0 + dx * j
                    ya = y0 + dy * i
                    xb = x0 + dx * (j + 1)
                    yb = y0 + dy * i
                    # Horizontal Members:
                    xc = x0 + dx * i
                    yc = y0 + dy * j
                    xd = x0 + dx * i
                    yd = y0 + dy * (j + 1)
                    lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])
                    lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])

    pattern: Pattern = Pattern.from_lines(lines, delete_boundary_face=True)  # type: ignore
    return pattern


def create_fan_pattern(
    xy_span=[[0.0, 10.0], [0.0, 10.0]],
    discretisation=[10, 10],
) -> Pattern:
    """Helper to construct a FormDiagram based on fan discretiastion with straight lines to the corners.

    Parameters
    ----------
    xy_span : list, optional
        List with initial- and end-points of the vault, by default [[0.0, 10.0], [0.0, 10.0]]
    discretisation : int, optional
        Set the density of the grid in x and y directions, by default 10
    fix : str, optional
        Option to select the constrained nodes: 'corners', 'all' are accepted, by default 'corners'

    Returns
    -------
    :class:`~compas_tno.diagrams.FormDiagram`
        The FormDiagram created.
    """

    if isinstance(discretisation, int):
        discretisation = [discretisation, discretisation]
    if discretisation[0] % 2 != 0 or discretisation[1] % 2 != 0:
        msg = "Warning!: discretisation of this form diagram has to be even."
        raise ValueError(msg)

    y1 = float(xy_span[1][1])
    y0 = float(xy_span[1][0])
    x1 = float(xy_span[0][1])
    x0 = float(xy_span[0][0])

    x_span = x1 - x0
    y_span = y1 - y0
    xc0 = x0 + x_span / 2
    yc0 = y0 + y_span / 2
    division_x = discretisation[0]
    division_y = discretisation[1]
    dx = float(x_span / division_x)
    dy = float(y_span / division_y)
    nx = int(division_x / 2)
    ny = int(division_y / 2)
    line_hor = [[x0, yc0, 0.0], [xc0, yc0, 0.0]]
    line_ver = [[xc0, y0, 0.0], [xc0, yc0, 0.0]]

    lines = []

    for i in range(nx):
        for j in range(ny + 1):
            # Diagonal Members:
            xa = x0 + dx * i
            ya = y0 + dy * j * i / nx
            xb = x0 + dx * (i + 1)
            yb = y0 + dy * j * (i + 1) / nx
            lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])

            a_mirror, b_mirror = mirror_points_line([[xa, ya, 0.0], [xb, yb, 0.0]], line_hor)
            lines.append([a_mirror, b_mirror])
            a_mirror, b_mirror = mirror_points_line([a_mirror, b_mirror], line_ver)
            lines.append([a_mirror, b_mirror])
            a_mirror, b_mirror = mirror_points_line([[xa, ya, 0.0], [xb, yb, 0.0]], line_ver)
            lines.append([a_mirror, b_mirror])

            xa_ = x0 + dx * j * i / nx
            ya_ = y0 + dy * i
            xb_ = x0 + dx * j * (i + 1) / nx
            yb_ = y0 + dy * (i + 1)
            lines.append([[xa_, ya_, 0.0], [xb_, yb_, 0.0]])

            a_mirror, b_mirror = mirror_points_line([[xa_, ya_, 0.0], [xb_, yb_, 0.0]], line_hor)
            lines.append([a_mirror, b_mirror])
            a_mirror, b_mirror = mirror_points_line([a_mirror, b_mirror], line_ver)
            lines.append([a_mirror, b_mirror])
            a_mirror, b_mirror = mirror_points_line([[xa_, ya_, 0.0], [xb_, yb_, 0.0]], line_ver)
            lines.append([a_mirror, b_mirror])

            if j < ny:
                # Vertical or Horizontal Members:
                xc = x0 + dx * (i + 1)
                yc = y0 + dy * j * (i + 1) / nx
                xd = x0 + dx * (i + 1)
                yd = y0 + dy * (j + 1) * (i + 1) / nx
                lines.append([[xc, yc, 0.0], [xd, yd, 0.0]])

                c_mirror, d_mirror = mirror_points_line([[xc, yc, 0.0], [xd, yd, 0.0]], line_hor)
                lines.append([c_mirror, d_mirror])
                c_mirror, d_mirror = mirror_points_line([c_mirror, d_mirror], line_ver)
                lines.append([c_mirror, d_mirror])
                c_mirror, d_mirror = mirror_points_line([[xc, yc, 0.0], [xd, yd, 0.0]], line_ver)
                lines.append([c_mirror, d_mirror])

                xc_ = x0 + dx * j * (i + 1) / nx
                yc_ = y0 + dy * (i + 1)
                xd_ = x0 + dx * (j + 1) * (i + 1) / nx
                yd_ = y0 + dy * (i + 1)
                lines.append([[xc_, yc_, 0.0], [xd_, yd_, 0.0]])

                c_mirror, d_mirror = mirror_points_line([[xc_, yc_, 0.0], [xd_, yd_, 0.0]], line_hor)
                lines.append([c_mirror, d_mirror])
                c_mirror, d_mirror = mirror_points_line([c_mirror, d_mirror], line_ver)
                lines.append([c_mirror, d_mirror])
                c_mirror, d_mirror = mirror_points_line([[xc_, yc_, 0.0], [xd_, yd_, 0.0]], line_ver)
                lines.append([c_mirror, d_mirror])

    pattern: Pattern = Pattern.from_lines(lines, delete_boundary_face=True)  # type: ignore
    return pattern


def create_ortho_pattern(
    xy_span=[[0.0, 10.0], [0.0, 10.0]],
    discretisation=[10, 10],
) -> Pattern:
    """Helper to construct a FormDiagram based on a simple orthogonal discretisation.

    Parameters
    ----------
    xy_span : list, optional
        List with initial- and end-points of the vault, by default [[0.0, 10.0], [0.0, 10.0]]
    discretisation : int, optional
        Set the density of the grid in x and y directions, by default 10
    fix : str, optional
        Option to select the constrained nodes: 'corners', 'all' are accepted, by default 'corners'

    Returns
    -------
    :class:`~compas_tno.diagrams.FormDiagram`
        The FormDiagram created.
    """

    if isinstance(discretisation, int):
        discretisation = [discretisation, discretisation]
    # if discretisation[0] % 2 != 0 or discretisation[1] % 2 != 0:
    #     msg = "Warning!: discretisation of this form diagram has to be even."
    #     raise ValueError(msg)

    y1 = float(xy_span[1][1])
    y0 = float(xy_span[1][0])
    x1 = float(xy_span[0][1])
    x0 = float(xy_span[0][0])
    x_span = x1 - x0
    y_span = y1 - y0
    division_x = discretisation[0]
    division_y = discretisation[1]
    dx = float(x_span / division_x)
    dy = float(y_span / division_y)

    vertices = []
    faces = []

    for j in range(division_y + 1):
        for i in range(division_x + 1):
            xi = x0 + dx * i
            yi = y0 + dy * j
            vertices.append([xi, yi, 0.0])
            if i < division_x and j < division_y:
                p1 = j * (division_x + 1) + i
                p2 = j * (division_x + 1) + i + 1
                p3 = (j + 1) * (division_x + 1) + i + 1
                p4 = (j + 1) * (division_x + 1) + i
                face = [p1, p2, p3, p4, p1]
                faces.append(face)
                print(face)

    pattern: Pattern = Pattern.from_vertices_and_faces(vertices, faces)  # type: ignore
    return pattern


def create_parametric_pattern(
    xy_span=[[0.0, 10.0], [0.0, 10.0]],
    discretisation=10,
    lambd=0.5,
) -> Pattern:
    """Create a parametric form diagram based on the inclination lambda of the arches

    Parameters
    ----------
    xy_span : [[float, float], [float, float]], optional
        List with initial- and end-points of the vault, by default, by default [[0.0, 10.0], [0.0, 10.0]]
    discretisation : int, optional
        Set the density of the grid in x and y directions, by default 10
    lambd : float, optional
        Inclination of the arches in the diagram (0.0 will result in cross and 1.0 in fan diagrams), by default 0.5
    fix : str, optional
        Option to select the constrained nodes: 'corners', 'all' are accepted, by default 'corners'

    Returns
    -------
    :class:`~compas_tno.diagrams.FormDiagram`
        The FormDiagram created.

    Notes
    ---------
        Diagram implemented after `N. A. Nodargi et al., 2022 <https://doi.org/10.1016/j.engstruct.2022.114878>`_.
    """
    if 0.0 > lambd or lambd > 1.0:
        raise ValueError("Lambda should be between 0.0 and 1.0")

    x_span = xy_span[0][1] - xy_span[0][0]
    y_span = xy_span[1][1] - xy_span[1][0]

    if abs(x_span - y_span) > 1e-6:
        y_span = x_span = 10.0
        x0, x1 = y0, y1 = 0.0, 10.0
    else:
        x0, x1 = xy_span[0][0], xy_span[0][1]
        y0, y1 = xy_span[1][0], xy_span[1][1]

    xc = (x1 + x0) / 2
    yc = (y1 + y0) / 2

    xc0 = x0 + x_span / 2
    yc0 = y0 + y_span / 2
    division_x = discretisation
    division_y = discretisation
    dx = float(x_span / division_x)
    dy = float(y_span / division_y)
    nx = int(division_x / 2)
    line_hor = [[x0, yc0, 0.0], [xc0, yc0, 0.0]]
    line_ver = [[xc0, y0, 0.0], [xc0, yc0, 0.0]]

    lines = []

    for i in range(nx + 1):
        j = i

        xa = xc
        ya = xc - dy * j
        xb = (ya - y0) * (1 - lambd)
        yb = (ya - y0) * (1 - lambd)

        if distance_point_point_xy([xa, ya], [xb, yb]):
            lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])

            append_mirrored_lines([[xa, ya, 0.0], [xb, yb, 0.0]], lines, line_hor, line_ver)

        if i == 0:
            xa = x0
            ya = y0

            if distance_point_point_xy([xa, ya], [xb, yb]):
                lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])

                append_mirrored_lines([[xa, ya, 0.0], [xb, yb, 0.0]], lines, line_hor, line_ver)

        xa = xc - dx * j
        xb = xc - dx * j
        ya = yc - dy * j
        yb = y0

        if distance_point_point_xy([xa, ya], [xb, yb]):
            lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])

            append_mirrored_lines([[xa, ya, 0.0], [xb, yb, 0.0]], lines, line_hor, line_ver)

        xa = yc - dy * j
        ya = yc
        xb = (xa - x0) * (1 - lambd)
        yb = xb * (y1 - y0) / (x1 - x0) + y0

        if distance_point_point_xy([xa, ya], [xb, yb]):
            lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])

            append_mirrored_lines([[xa, ya, 0.0], [xb, yb, 0.0]], lines, line_hor, line_ver)

        xa = xc - dx * j
        xb = x0
        ya = yc - dy * j
        yb = yc - dy * j

        if distance_point_point_xy([xa, ya], [xb, yb]):
            lines.append([[xa, ya, 0.0], [xb, yb, 0.0]])

            append_mirrored_lines([[xa, ya, 0.0], [xb, yb, 0.0]], lines, line_hor, line_ver)

    # clean_lines = split_intersection_lines(lines)
