#! python3
# venv: brg-csd
# r: compas_rv>=0.10.0

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.commands import make_pattern_from_meshgrid
from compas_rv.commands import make_pattern_from_rhinolines
from compas_rv.commands import make_pattern_from_rhinomesh
from compas_rv.commands import make_pattern_from_rhinosurface
from compas_rv.commands import make_pattern_from_skeleton
from compas_rv.commands import make_pattern_from_triangulation
from compas_rv.datastructures import Pattern
from compas_rv.session import RVSession
from compas_tna.diagrams.diagram_circular import create_circular_radial_mesh
from compas_tna.diagrams.diagram_circular import create_circular_radial_spaced_mesh
from compas_tna.diagrams.diagram_circular import create_circular_spiral_mesh
from compas_tna.diagrams.diagram_rectangular import create_cross_mesh
from compas_tna.diagrams.diagram_rectangular import create_fan_mesh
from compas_tna.diagrams.diagram_rectangular import create_ortho_mesh
from compas_tna.diagrams.diagram_rectangular import create_parametric_fan_mesh


def get_location():
    option = rs.GetString("Pattern location", "Origin", ["Origin", "Coordinates", "Point"])
    if not option:
        return
    if option == "Origin":
        return 0.0, 0.0
    if option == "Coordinates":
        x = rs.GetReal("X", 0.0)
        if x is None:
            return
        y = rs.GetReal("Y", 0.0)
        if y is None:
            return
        return x, y
    point = rs.GetPoint("Point")
    if not point:
        return
    return point[0], point[1]


def get_size():
    x_size = rs.GetReal("X size", 10.0, minimum=0.0)
    if x_size is None:
        return
    y_size = rs.GetReal("Y size", 10.0, minimum=0.0)
    if y_size is None:
        return
    return x_size, y_size


def get_circular_pattern(factory):
    center = get_location()
    if center is None:
        return
    radius = rs.GetReal("Radius", 5.0, minimum=0.0)
    if radius is None:
        return
    n_hoops = rs.GetInteger("Hoops", 12, minimum=4)
    if n_hoops is None:
        return
    n_parallels = rs.GetInteger("Radials", 24, minimum=12)
    if n_parallels is None:
        return
    r_oculus = rs.GetReal("Oculus radius", 0.0, minimum=0.0)
    if r_oculus is None:
        return
    if r_oculus >= radius:
        rs.MessageBox("The oculus radius should be smaller than the pattern radius.", title="Warning")
        return
    return factory(center=center, radius=radius, n_hoops=n_hoops, n_parallels=n_parallels, r_oculus=r_oculus).copy(cls=Pattern)


def get_cross_pattern():
    point = get_location()
    if point is None:
        return
    size = get_size()
    if size is None:
        return
    resolution = rs.GetInteger("Resolution", 10, minimum=1)
    if resolution is None:
        return
    return create_cross_mesh(
        x_span=(point[0], point[0] + size[0]),
        y_span=(point[1], point[1] + size[1]),
        n=resolution,
    ).copy(cls=Pattern)


def get_fan_pattern():
    point = get_location()
    if point is None:
        return
    size = get_size()
    if size is None:
        return
    n_fans = rs.GetInteger("Fans", 10, minimum=2)
    if n_fans is None:
        return
    n_hoops = rs.GetInteger("Hoops", 10, minimum=2)
    if n_hoops is None:
        return
    if n_fans % 2 or n_hoops % 2:
        rs.MessageBox("The fan and hoop discretisation should be even.", title="Warning")
        return
    return create_fan_mesh(
        x_span=(point[0], point[0] + size[0]),
        y_span=(point[1], point[1] + size[1]),
        n_fans=n_fans,
        n_hoops=n_hoops,
    ).copy(cls=Pattern)


def get_ortho_pattern():
    point = get_location()
    if point is None:
        return
    size = get_size()
    if size is None:
        return
    nx = rs.GetInteger("X faces", 10, minimum=2)
    if nx is None:
        return
    ny = rs.GetInteger("Y faces", nx, minimum=2)
    if ny is None:
        return
    return create_ortho_mesh(
        x_span=(point[0], point[0] + size[0]),
        y_span=(point[1], point[1] + size[1]),
        nx=nx,
        ny=ny,
    ).copy(cls=Pattern)


def get_parametric_pattern():
    point = get_location()
    if point is None:
        return
    size = get_size()
    if size is None:
        return
    resolution = rs.GetInteger("Resolution", 10, minimum=2)
    if resolution is None:
        return
    inclination = rs.GetReal("Lambda inclination", 0.5, minimum=0.0, maximum=1.0)
    if inclination is None:
        return
    return create_parametric_fan_mesh(
        x_span=(point[0], point[0] + size[0]),
        y_span=(point[1], point[1] + size[1]),
        n=resolution,
        lambd=inclination,
    ).copy(cls=Pattern)


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

    session.clear()

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
        option2 = rs.GetString(
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

        if option2 == "Radial":
            pattern = get_circular_pattern(create_circular_radial_mesh)

        elif option2 == "RadialSpaced":
            pattern = get_circular_pattern(create_circular_radial_spaced_mesh)

        elif option2 == "Spiral":
            pattern = get_circular_pattern(create_circular_spiral_mesh)

        elif option2 == "Cross":
            pattern = get_cross_pattern()

        elif option2 == "Fan":
            pattern = get_fan_pattern()

        elif option2 == "Ortho":
            pattern = get_ortho_pattern()

        elif option2 == "Parametric":
            pattern = get_parametric_pattern()

        else:
            return

    else:
        return

    if not pattern:
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
