import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import Diagram
from compas_rv.session import RVSession


class RhinoDiagramObject(RUIMeshObject):
    session = RVSession()

    freecolor = ColorAttribute(default=Color.white())
    anchorcolor = ColorAttribute(default=Color.red())
    fixedcolor = ColorAttribute(default=Color.cyan())

    def __init__(
        self,
        disjoint=True,
        show_supports=True,
        show_fixed=True,
        show_free=False,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

        self.show_vertices = True
        self.show_supports = show_supports
        self.show_fixed = show_fixed
        self.show_free = show_free
        self.show_edges = True
        self.show_faces = False

        self._guids_angles = []

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def settings(self):
        settings = super().settings
        settings["show_supports"] = self.show_supports
        settings["show_fixed"] = self.show_fixed
        settings["show_free"] = self.show_free
        return settings

    @property
    def diagram(self) -> Diagram:
        return self.mesh

    @diagram.setter
    def diagram(self, diagram: Diagram) -> None:
        self.mesh = diagram

    def edges(self, **kwargs):
        return self.diagram.edges(**kwargs)

    def faces(self, **kwargs):
        return self.diagram.faces(**kwargs)

    def forces(self):
        return self.diagram.edges_attribute("_f", keys=self.edges())

    def compute_edge_colors(self, tol=1e-3) -> None:
        forces = self.forces()
        magnitudes = [abs(f) for f in forces]
        fmin = min(magnitudes)
        fmax = max(magnitudes)

        if fmax - fmin < tol:
            # size of the range of forces is already checked here
            # no need to check again in the loop
            return

        colors = []

        for force, magnitude in zip(forces, magnitudes):
            # this will need to be updated once we allow for tension forces
            # or we have to exclude tension forces from the calculation
            # and give tension edges their own style
            colors.append(Color.from_i((magnitude - fmin) / (fmax - fmin)))

        return colors

    # =============================================================================
    # Clear
    # =============================================================================

    def clear_angles(self):
        compas_rhino.objects.delete_objects(self._guids_angles, purge=True)

    def clear(self):
        super().clear()
        self.clear_angles()

    # =============================================================================
    # Draw
    # =============================================================================

    def draw(self):
        faces = []
        if self.show_faces:
            faces += list(self.diagram.faces_where(_is_loaded=True))
        if faces:
            self.show_faces = faces

        for vertex in self.diagram.vertices():
            if self.diagram.vertex_attribute(vertex, "is_support"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.diagram.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        super().draw()

        if self.session.settings.drawing.show_angles:
            self.draw_angles()

        return self.guids

    def draw_vertices(self):
        if self.show_vertices is True:
            vertices = []
            if self.show_free:
                vertices += list(self.diagram.vertices_where(is_support=False, is_fixed=False))
            if self.show_fixed:
                vertices += list(self.diagram.vertices_where(is_fixed=True))
            if self.show_supports:
                vertices += list(self.diagram.vertices_where(is_support=True))
            self.show_vertices = vertices

        for vertex in self.diagram.vertices():
            if self.diagram.vertex_attribute(vertex, "is_support"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.diagram.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        return super().draw_vertices()

    def draw_edges(self):
        if self.show_edges is True:
            edges = list(self.edges())
            if edges:
                self.show_edges = edges

        if self.session.settings.drawing.show_forces:
            edges = list(self.edges())
            colors = self.compute_edge_colors()
            if colors:
                edge_color = dict(zip(edges, colors))
            else:
                edge_color = dict()

        for edge in self.edges():
            if self.session.settings.drawing.show_forces:
                if edge in edge_color:
                    self.edgecolor[edge] = edge_color[edge]
            else:
                self.edgecolor.clear()  # not sure why this is not recognised

        return super().draw_edges()

    def draw_faces(self):
        faces = []
        if self.show_faces is True:
            faces += list(self.faces())
            if faces:
                self.show_faces = faces

        return super().draw_faces()

    def draw_angles(self):
        fontheight = 10
        fontface = "Arial Regular"
        group = None

        # perhaps there should be aseparate setting for this
        tol = self.session.settings.tna.horizontal_max_angle

        edges = list(self.edges())
        angles = self.diagram.edges_attribute(name="_a", keys=edges)
        amin = min(angles)
        amax = max(angles)
        aspan = amax - amin

        if aspan**2 < 0.001**2:
            return

        transformation = compas_rhino.conversions.transformation_to_rhino(self.worldtransformation)

        guids = []

        for edge, angle in zip(edges, angles):
            if angle < tol:
                continue

            name = "{}.angle.{}-{}".format(self.diagram.name, *edge)  # type: ignore
            color = Color.from_i((angle - amin) / aspan)
            attr = self.compile_attributes(name="{}.label".format(name), color=color)
            line = self.diagram.edge_line(edge)
            location = compas_rhino.conversions.point_to_rhino(line.midpoint)
            location.Transform(transformation)

            dot = Rhino.Geometry.TextDot(f"{angle:.1f}", location)  # type: ignore
            dot.FontHeight = fontheight
            dot.FontFace = fontface

            guid = sc.doc.Objects.AddTextDot(dot, attr)
            guids.append(guid)

        if group:
            self.add_to_group(group, guids)

        self._guids_angles = guids
        self._guids += guids
        return guids

    # =============================================================================
    # Redraw
    # =============================================================================

    def redraw(self):
        rs.EnableRedraw(False)
        self.clear()
        self.draw()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_vertices(self):
        rs.EnableRedraw(False)
        self.clear_vertices()
        self.draw_vertices()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_edges(self):
        rs.EnableRedraw(False)
        self.clear_edges()
        self.draw_edges()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_faces(self):
        rs.EnableRedraw(False)
        self.clear_faces()
        self.draw_faces()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_angles(self):
        rs.EnableRedraw(False)
        self.clear_angles()
        self.draw_angles()
        rs.EnableRedraw(True)
        rs.Redraw()
