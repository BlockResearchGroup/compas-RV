#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino
import compas_rhino.conversions
import compas_rhino.objects
from compas.datastructures import Mesh
from compas_rv.session import RVSession
from compas_tna.envelope import BarrelVaultEnvelope
from compas_tna.envelope import CrossVaultEnvelope
from compas_tna.envelope import DomeEnvelope
from compas_tna.envelope import MeshEnvelope
from compas_tna.envelope import PavillionVaultEnvelope
from compas_tna.envelope import PointedVaultEnvelope


ENVELOPE_LAYER = "RhinoVAULT::Envelope"


def get_location():
    option = rs.GetString("Envelope location", "Origin", ["Origin", "Coordinates", "Point"])
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


def get_size(default_x=10.0, default_y=10.0):
    x_size = rs.GetReal("X size", default_x, minimum=0.0)
    if x_size is None:
        return
    y_size = rs.GetReal("Y size", default_y, minimum=0.0)
    if y_size is None:
        return
    return x_size, y_size


def get_thickness(default=0.5):
    return rs.GetReal("Thickness", default, minimum=0.0)


def get_crossvault():
    point = get_location()
    if point is None:
        return
    size = get_size()
    if size is None:
        return
    thickness = get_thickness()
    if thickness is None:
        return
    return CrossVaultEnvelope(x_span=(point[0], point[0] + size[0]), y_span=(point[1], point[1] + size[1]), thickness=thickness)


def get_barrelvault():
    point = get_location()
    if point is None:
        return
    span = rs.GetReal("Span", 10.0, minimum=0.0)
    if span is None:
        return
    depth = rs.GetReal("Depth", 10.0, minimum=0.0)
    if depth is None:
        return
    rise = rs.GetReal("Rise", 3.0, minimum=0.0)
    if rise is None:
        return
    thickness = get_thickness()
    if thickness is None:
        return
    return BarrelVaultEnvelope(rise=rise, span=span, x0=point[0], y_span=(point[1], point[1] + depth), thickness=thickness)


def get_pointedvault():
    point = get_location()
    if point is None:
        return
    size = get_size()
    if size is None:
        return
    minimum_rise = 0.5 * max(size)
    message = "Rise must be greater than or equal to {0:.3f}".format(minimum_rise)
    rise = rs.GetReal(message, minimum_rise, minimum=minimum_rise)
    if rise is None:
        return
    thickness = get_thickness()
    if thickness is None:
        return
    return PointedVaultEnvelope(x_span=(point[0], point[0] + size[0]), y_span=(point[1], point[1] + size[1]), thickness=thickness, hc=rise)


def get_pavilionvault():
    point = get_location()
    if point is None:
        return
    size = get_size()
    if size is None:
        return
    thickness = get_thickness()
    if thickness is None:
        return
    angle = rs.GetReal("Springing angle", 45.0, minimum=0.0, maximum=90.0)
    if angle is None:
        return
    return PavillionVaultEnvelope(x_span=(point[0], point[0] + size[0]), y_span=(point[1], point[1] + size[1]), thickness=thickness, spr_angle=angle)


def get_dome():
    center = get_location()
    if center is None:
        return
    radius = rs.GetReal("Radius", 5.0, minimum=0.0)
    if radius is None:
        return
    thickness = get_thickness()
    if thickness is None:
        return
    r_oculus = rs.GetReal("Oculus radius", 0.5, minimum=0.0)
    if r_oculus is None or r_oculus >= radius:
        return
    return DomeEnvelope(center=center, radius=radius, thickness=thickness, n_hoops=40, n_parallels=40, r_oculus=r_oculus)


def get_from_middle():
    guid = compas_rhino.objects.select_mesh("Select middle mesh")
    if not guid:
        return
    obj = compas_rhino.objects.find_object(guid)
    mesh = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=Mesh)
    thickness = get_thickness()
    if thickness is None:
        return
    rs.HideObject(guid)
    return MeshEnvelope.from_middle_mesh(mesh, thickness)


def get_from_bounds():
    guids = []

    guid = compas_rhino.objects.select_mesh("Select intrados")
    rs.UnselectAllObjects()
    if not guid:
        return
    guids.append(guid)
    obj = compas_rhino.objects.find_object(guid)
    intrados = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=Mesh)

    guid = compas_rhino.objects.select_mesh("Select extrados")
    rs.UnselectAllObjects()
    if not guid:
        return
    guids.append(guid)
    obj = compas_rhino.objects.find_object(guid)
    extrados = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=Mesh)

    guid = compas_rhino.objects.select_mesh("Select middle (optional)")
    rs.UnselectAllObjects()
    if guid:
        guids.append(guid)
        obj = compas_rhino.objects.find_object(guid)
        middle = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=Mesh)
    else:
        middle = None

    guid = compas_rhino.objects.select_mesh("Select fill mesh (optional)")
    rs.UnselectAllObjects()
    if guid:
        guids.append(guid)
        obj = compas_rhino.objects.find_object(guid)
        fill = compas_rhino.conversions.mesh_to_compas(obj.Geometry, cls=Mesh)
    else:
        fill = None

    rs.HideObjects(guids)

    envelope = MeshEnvelope.from_meshes(intrados, extrados, middle)
    if fill:
        envelope.fill = fill
    return envelope


LIBRARY = {
    "BarrelVault": get_barrelvault,
    "CrossVault": get_crossvault,
    "PointedVault": get_pointedvault,
    "PavilionVault": get_pavilionvault,
    "Dome": get_dome,
}


def RunCommand():
    session = RVSession()

    option = rs.GetString("Envelope from", "FromLibrary", ["FromLibrary", "FromMiddle", "FromBounds"])
    if not option:
        return

    if option == "FromLibrary":
        pattern = rs.GetString("Envelope pattern", "BarrelVault", list(LIBRARY.keys()))
        if not pattern:
            return
        envelope = LIBRARY[pattern]()
    elif option == "FromMiddle":
        envelope = get_from_middle()
    elif option == "FromBounds":
        envelope = get_from_bounds()
    else:
        return

    if not envelope:
        return session.warn("Error creating Envelope. Try again.")

    rho = rs.GetInteger("Density masonry (rho)", int(envelope.rho), minimum=0, maximum=200)
    if rho is None:
        return
    envelope.rho = rho

    if envelope.fill:
        rho_fill = rs.GetInteger("Density masonry fill (rho_fill)", int(envelope.rho_fill), minimum=0, maximum=200)
        if rho_fill is None:
            return
        envelope.rho_fill = rho_fill

    session.clear_envelope(redraw=False)
    session["envelope"] = envelope

    settings = session.settings.envelope
    if envelope.intrados:
        session.scene.add(envelope.intrados, disjoint=True, show=settings.show_intrados, name="Intrados", layer=ENVELOPE_LAYER)
    if envelope.middle:
        session.scene.add(envelope.middle, disjoint=True, show=settings.show_middle, name="Middle", layer=ENVELOPE_LAYER)
    if envelope.extrados:
        session.scene.add(envelope.extrados, disjoint=True, show=settings.show_extrados, name="Extrados", layer=ENVELOPE_LAYER)
    if envelope.fill:
        session.scene.add(envelope.fill, disjoint=True, show=settings.show_fill, name="Fill", layer=ENVELOPE_LAYER)

    session.scene.redraw()
    rs.Redraw()

    print("Envelope successfully created.")

    if session.settings.autosave:
        session.record(name="TNO Envelope")


if __name__ == "__main__":
    RunCommand()
