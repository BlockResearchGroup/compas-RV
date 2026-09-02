import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Line
from compas.geometry import Sphere
from compas.scene.descriptors.color import ColorAttribute
from compas_rhino.scene import RhinoSceneObject
from compas_rv.session import RVSession
from compas_tna.envelope import Envelope


class RhinoEnvelopeObject(RhinoSceneObject):
    """Scene object for drawing a TNA envelope in Rhino."""

    session = RVSession()
    envelope: Envelope  # type: ignore

    boundscolor = ColorAttribute(default=Color.magenta())
    extradoscrackcolor = ColorAttribute(default=Color.green())
    intradoscrackcolor = ColorAttribute(default=Color.blue())

    def __init__(
        self,
        layer="RhinoVAULT::Envelope",
        group=None,
        boundsgroup="RhinoVAULT::Envelope::Bounds",
        crackgroup="RhinoVAULT::Envelope::Cracks",
        disjoint=True,
        boundscolor=None,
        extradoscrackcolor=None,
        intradoscrackcolor=None,
        **kwargs,
    ):
        super().__init__(layer=layer, group=group, **kwargs)

        self.boundsgroup = boundsgroup
        self.crackgroup = crackgroup
        self.disjoint = disjoint

        self.boundscolor = boundscolor or self.boundscolor
        self.extradoscrackcolor = extradoscrackcolor or self.extradoscrackcolor
        self.intradoscrackcolor = intradoscrackcolor or self.intradoscrackcolor

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def settings(self):
        settings = super().settings
        settings["layer"] = self.layer
        settings["group"] = self.group
        settings["boundsgroup"] = self.boundsgroup
        settings["crackgroup"] = self.crackgroup
        settings["disjoint"] = self.disjoint
        settings["boundscolor"] = self.boundscolor
        settings["extradoscrackcolor"] = self.extradoscrackcolor
        settings["intradoscrackcolor"] = self.intradoscrackcolor
        return settings

    @property
    def envelope(self):
        return self.item

    @envelope.setter
    def envelope(self, envelope):
        self._item = envelope
        self._transformation = None

    # =============================================================================
    # Clear
    # =============================================================================

    def clear(self):
        """Delete all Rhino geometry drawn by this scene object."""
        compas_rhino.objects.delete_objects(self.guids, purge=True)
        self._guids = []

    # =============================================================================
    # Draw
    # =============================================================================

    def draw_mesh(self, mesh, name):
        """Draw one of the envelope meshes."""
        if not mesh:
            return

        vertices, faces = mesh.to_vertices_and_faces()
        geometry = compas_rhino.conversions.vertices_and_faces_to_rhino(vertices, faces, color=self.color, disjoint=self.disjoint)
        geometry.Transform(compas_rhino.conversions.transformation_to_rhino(self.worldtransformation))

        attr = self.compile_attributes(name=name)
        guid = sc.doc.Objects.AddMesh(geometry, attr)

        if self.group:
            self.add_to_group(self.group, [guid])

        self._guids.append(guid)
        return guid

    def vertex_bound(self, formdiagram, vertex):
        ub = formdiagram.vertex_attribute(vertex, "ub")
        lb = formdiagram.vertex_attribute(vertex, "lb")
        if ub is None or lb is None:
            return

        point = formdiagram.vertex_point(vertex)
        upper = point.copy()
        upper.z = ub
        lower = point.copy()
        lower.z = lb
        return Line(upper, lower)

    def vertex_is_on_upper_bound(self, formdiagram, vertex, tol=1e-6):
        ub = formdiagram.vertex_attribute(vertex, "ub")
        if ub is None:
            return False
        return abs(formdiagram.vertex_attribute(vertex, "z") - ub) < tol

    def vertex_is_on_lower_bound(self, formdiagram, vertex, tol=1e-6):
        lb = formdiagram.vertex_attribute(vertex, "lb")
        if lb is None:
            return False
        return abs(formdiagram.vertex_attribute(vertex, "z") - lb) < tol

    def draw_bounds(self, formdiagram):
        """Draw the lower and upper vertex bounds of a form diagram."""
        guids = []

        for vertex in formdiagram.vertices():
            bound = self.vertex_bound(formdiagram, vertex)
            if not bound:
                continue

            name = "{}.vertex.{}.bound".format(formdiagram.name, vertex)
            attr = self.compile_attributes(name=name, color=self.boundscolor)
            guids.append(sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(bound), attr))
            guids.append(sc.doc.Objects.AddPoint(compas_rhino.conversions.point_to_rhino(bound.start), attr))
            guids.append(sc.doc.Objects.AddPoint(compas_rhino.conversions.point_to_rhino(bound.end), attr))

        if guids:
            if self.boundsgroup:
                self.add_to_group(self.boundsgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_cracks(self, formdiagram):
        """Draw points where the thrust network touches either envelope bound."""
        guids = []

        for vertex in formdiagram.vertices():
            if self.vertex_is_on_lower_bound(formdiagram, vertex):
                color = self.intradoscrackcolor
            elif self.vertex_is_on_upper_bound(formdiagram, vertex):
                color = self.extradoscrackcolor
            else:
                continue

            name = "{}.vertex.{}.crack".format(formdiagram.name, vertex)
            attr = self.compile_attributes(name=name, color=color)
            sphere = Sphere(self.session.settings.envelope.crack_radius, point=formdiagram.vertex_point(vertex))
            guids.append(sc.doc.Objects.AddSphere(compas_rhino.conversions.sphere_to_rhino(sphere), attr))

        if guids:
            if self.crackgroup:
                self.add_to_group(self.crackgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw(self):
        """Draw the visible envelope meshes, bounds, and cracks."""
        self._guids = []
        settings = self.session.settings.envelope

        if settings.show_intrados:
            self.draw_mesh(self.envelope.intrados, "Intrados")
        if settings.show_middle:
            self.draw_mesh(self.envelope.middle, "Middle")
        if settings.show_extrados:
            self.draw_mesh(self.envelope.extrados, "Extrados")
        if settings.show_fill:
            self.draw_mesh(self.envelope.fill, "Fill")

        if settings.show_bounds or settings.show_cracks:
            formobject = self.session.find_formdiagram(warn=False)
            if formobject:
                if settings.show_bounds:
                    self.draw_bounds(formobject.diagram)
                if settings.show_cracks:
                    self.draw_cracks(formobject.diagram)

        return self.guids

    # =============================================================================
    # Redraw
    # =============================================================================

    def redraw(self):
        """Clear and redraw the envelope object."""
        rs.EnableRedraw(False)
        self.clear()
        self.draw()
        rs.EnableRedraw(True)
        rs.Redraw()
