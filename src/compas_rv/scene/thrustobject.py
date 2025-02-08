import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
from compas.colors import Color
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Vector
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import ThrustDiagram
from compas_rv.session import RVSession


class RhinoThrustObject(RUIMeshObject):
    session = RVSession()
    mesh: ThrustDiagram

    vertexcolor = ColorDictAttribute(default=Color.purple())
    edgecolor = ColorDictAttribute(default=Color.purple().darkened(50))
    facecolor = ColorDictAttribute(default=Color.purple().lightened(25))
    freecolor = ColorAttribute(default=Color.purple())
    anchorcolor = ColorAttribute(default=Color.red())
    fixedcolor = ColorAttribute(default=Color.cyan())
    residualcolor = ColorAttribute(default=Color.cyan())
    reactioncolor = ColorAttribute(default=Color.green())
    loadcolor = ColorAttribute(default=Color.green().darkened(50))
    selfweightcolor = ColorAttribute(default=Color.white())
    compressioncolor = ColorAttribute(default=Color.blue())
    tensioncolor = ColorAttribute(default=Color.red())

    def __init__(
        self,
        disjoint=True,
        show_supports=True,
        show_fixed=True,
        show_free=False,
        vertexgroup="RV::ThrustDiagram::Vertices",
        edgegroup="RV::ThrustDiagram::Edges",
        facegroup="RV::ThrustDiagram::Faces",
        loadgroup="RV::ThrustDiagram::Loads",
        selfweightgroup="RV::ThrustDiagram::Selfweight",
        forcegroup="RV::ThrustDiagram::Forces",
        reactiongroup="RV::ThrustDiagram::Reactions",
        residualgroup="RV::ThrustDiagram::Residuals",
        **kwargs,
    ):
        super().__init__(
            disjoint=disjoint,
            vertexgroup=vertexgroup,
            edgegroup=edgegroup,
            facegroup=facegroup,
            **kwargs,
        )

        self.show_faces = True
        self.show_edges = False
        self.show_supports = show_supports
        self.show_fixed = show_fixed
        self.show_free = show_free
        self.loadgroup = loadgroup
        self.selfweightgroup = selfweightgroup
        self.forcegroup = forcegroup
        self.reactiongroup = reactiongroup
        self.residualgroup = residualgroup

    @property
    def settings(self):
        settings = super().settings
        settings["show_supports"] = self.show_supports
        settings["show_fixed"] = self.show_fixed
        settings["show_free"] = self.show_free
        return settings

    @property
    def diagram(self) -> ThrustDiagram:
        return self.mesh

    @diagram.setter
    def diagram(self, diagram: ThrustDiagram) -> None:
        self.mesh = diagram

    def compute_pipe_colors(self, tol=1e-3) -> None:
        edges = list(self.diagram.edges())
        forces = [self.diagram.edge_attribute(edge, "_f") for edge in edges]
        magnitudes = [abs(f) for f in forces]
        fmin = min(magnitudes)
        fmax = max(magnitudes)

        if fmax - fmin < tol:
            # the size of the range is already checked here
            # no need to do this again in the loop
            return

        colors = []
        for force, magnitude in zip(forces, magnitudes):
            # this will need to be updated when we include tension edges
            colors.append(Color.from_i((magnitude - fmin) / (fmax - fmin)))

        return dict(zip(edges, colors))

    # =============================================================================
    # Clear
    # =============================================================================

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

        if self.session.settings.drawing.show_reactions:
            self.draw_reactions()
        if self.session.settings.drawing.show_loads:
            self.draw_loads()
        if self.session.settings.drawing.show_selfweight:
            self.draw_selfweight()
        if self.session.settings.drawing.show_pipes:
            self.draw_pipes()

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
            edges = list(self.diagram.edges_where(_is_edge=True))
            if edges:
                self.show_edges = edges

        return super().draw_edges()

    def draw_faces(self):
        faces = []
        if self.show_faces:
            faces += list(self.diagram.faces_where(_is_loaded=True))
        if faces:
            self.show_faces = faces

        return super().draw_faces()

    def draw_loads(self):
        guids = []

        scale = self.session.settings.drawing.scale_loads
        color = self.loadcolor
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=False):
            load = self.diagram.vertex_attributes(vertex, ["px", "py", "pz"])

            if load is not None:
                vector = Vector(*load) * scale
                if vector.length > tol:
                    name = "{}.vertex.{}.load".format(self.diagram.name, vertex)
                    attr = self.compile_attributes(name=name, color=color, arrow="start")
                    point = self.diagram.vertex_point(vertex)
                    line = Line.from_point_and_vector(point, vector)
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.loadgroup:
                self.add_to_group(self.loadgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_selfweight(self):
        guids = []

        scale = self.session.settings.drawing.scale_selfweight
        color = self.selfweightcolor
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=False):
            thickness = self.diagram.vertex_attribute(vertex, "t")

            if thickness:
                area = self.diagram.vertex_area(vertex)
                weight = area * thickness
                point = self.diagram.vertex_point(vertex)
                vector = Vector(0, 0, -weight * scale)
                if vector.length > tol:
                    line = Line.from_point_and_vector(point, vector)
                    name = "{}.vertex.{}.selfweight".format(self.diagram.name, vertex)
                    attr = self.compile_attributes(name=name, color=color, arrow="end")
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.selfweightgroup:
                self.add_to_group(self.selfweightgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_pipes(self):
        guids = []

        scale = self.session.settings.drawing.scale_pipes
        tol = self.session.settings.drawing.tol_pipes

        pipe_colors = self.compute_pipe_colors()

        for edge in self.diagram.edges():
            force = self.diagram.edge_attribute(edge, "_f")

            if force != 0:
                line = self.diagram.edge_line(edge)
                radius = abs(force) * scale

                color = self.compressioncolor
                if self.session.settings.drawing.show_forces:
                    color = pipe_colors[edge]

                if radius > tol:
                    pipe = Cylinder.from_line_and_radius(line, radius)
                    name = "{}.edge.{}.force".format(self.diagram.name, edge)
                    attr = self.compile_attributes(name=name, color=color)
                    guid = sc.doc.Objects.AddBrep(compas_rhino.conversions.cylinder_to_rhino_brep(pipe), attr)
                    guids.append(guid)

        if guids:
            if self.forcegroup:
                self.add_to_group(self.forcegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_reactions(self):
        guids = []

        scale = self.session.settings.drawing.scale_reactions
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=True):
            residual = Vector(*self.diagram.vertex_attributes(vertex, ["_rx", "_ry", "_rz"]))
            vector = residual * scale

            if vector.length > tol:
                name = "{}.vertex.{}.reaction".format(self.diagram.name, vertex)
                attr = self.compile_attributes(name=name, color=self.reactioncolor, arrow="start")
                point = self.diagram.vertex_point(vertex)
                line = Line.from_point_and_vector(point, vector)
                guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                guids.append(guid)

        if guids:
            if self.reactiongroup:
                self.add_to_group(self.reactiongroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_residuals(self):
        guids = []

        scale = self.session.settings.drawing.scale_residuals
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=False):
            residual = Vector(*self.diagram.vertex_attributes(vertex, ["_rx", "_ry", "_rz"]))

            vector = residual * scale
            if vector.length > tol:
                name = "{}.vertex.{}.residual".format(self.diagram.name, vertex)
                attr = self.compile_attributes(name=name, color=self.residualcolor, arrow="end")
                point = self.diagram.vertex_point(vertex)
                line = Line.from_point_and_vector(point, vector)
                guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                guids.append(guid)

        if guids:
            if self.residualgroup:
                self.add_to_group(self.residualgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    # =============================================================================
    # Redraw
    # =============================================================================

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

    def redraw(self):
        rs.EnableRedraw(False)
        self.clear()
        self.draw()
        rs.EnableRedraw(True)
        rs.Redraw()
