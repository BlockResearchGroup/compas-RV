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


class RhinoThrustObject(RUIMeshObject):
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
        show_reactions=True,
        show_residuals=False,
        show_loads=False,
        show_selfweight=False,
        show_forces=False,
        loadgroup=None,
        selfweightgroup=None,
        forcegroup=None,
        reactiongroup=None,
        residualgroup=None,
        scale_loads=1,
        scale_forces=1e-2,
        scale_residuals=0.1,
        scale_selfweight=1,
        tol_vectors=1e-3,
        tol_pipes=1e-3,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

        self.show_faces = True
        self.show_edges = False

        self.show_supports = show_supports
        self.show_fixed = show_fixed
        self.show_free = show_free

        self.show_reactions = show_reactions
        self.show_residuals = show_residuals
        self.show_loads = show_loads
        self.show_selfweight = show_selfweight
        self.show_forces = show_forces

        self.loadgroup = loadgroup
        self.selfweightgroup = selfweightgroup
        self.forcegroup = forcegroup
        self.reactiongroup = reactiongroup
        self.residualgroup = residualgroup

        self.scale_loads = scale_loads
        self.scale_forces = scale_forces
        self.scale_residuals = scale_residuals
        self.scale_selfweight = scale_selfweight

        self.tol_vectors = tol_vectors
        self.tol_pipes = tol_pipes

    @property
    def settings(self):
        settings = super().settings

        settings["show_supports"] = self.show_supports
        settings["show_free"] = self.show_free
        settings["show_forces"] = self.show_forces
        settings["show_residuals"] = self.show_residuals
        settings["show_reactions"] = self.show_reactions
        settings["show_loads"] = self.show_loads
        settings["show_selfweight"] = self.show_selfweight

        settings["scale_loads"] = self.scale_loads
        settings["scale_forces"] = self.scale_forces
        settings["scale_residuals"] = self.scale_residuals
        settings["scale_selfweight"] = self.scale_selfweight

        settings["tol_vectors"] = self.tol_vectors
        settings["tol_pipes"] = self.tol_pipes

        settings["freecolor"] = self.freecolor
        settings["anchorcolor"] = self.anchorcolor
        settings["residualcolor"] = self.residualcolor
        settings["reactioncolor"] = self.reactioncolor
        settings["loadcolor"] = self.loadcolor
        settings["selfweightcolor"] = self.selfweightcolor
        settings["compressioncolor"] = self.compressioncolor
        settings["tensioncolor"] = self.tensioncolor

        return settings

    def draw(self):
        faces = []
        if self.show_faces:
            faces += list(self.mesh.faces_where(_is_loaded=True))
        if faces:
            self.show_faces = faces

        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_support"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.mesh.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        super().draw()

        if self.show_reactions:
            self.draw_reactions()
        if self.show_residuals:
            self.draw_residuals()
        if self.show_loads:
            self.draw_loads()
        if self.show_selfweight:
            self.draw_selfweight()
        if self.show_forces:
            self.draw_forces()

        return self.guids

    def draw_vertices(self):
        vertices = []
        if self.show_free:
            vertices += list(self.mesh.vertices_where(is_support=False, is_fixed=False))
        if self.show_fixed:
            vertices += list(self.mesh.vertices_where(is_fixed=True))
        if self.show_supports:
            vertices += list(self.mesh.vertices_where(is_support=True))
        if vertices:
            self.show_vertices = vertices

        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_support"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.mesh.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        return super().draw_vertices()

    def draw_edges(self):
        edges = []
        if self.show_edges:
            edges += list(self.mesh.edges_where(_is_edge=True))
        if edges:
            self.show_edges = edges

        for edge in self.mesh.edges_where(_is_edge=True):
            pass

        return super().draw_edges()

    def draw_faces(self):
        faces = []
        if self.show_faces:
            faces += list(self.mesh.faces_where(_is_loaded=True))
        if faces:
            self.show_faces = faces

        for face in self.mesh.faces_where(_is_loaded=True):
            pass

        return super().draw_faces()

    def draw_loads(self):
        guids = []

        for vertex in self.mesh.vertices_where(is_support=False):
            load = self.mesh.vertex_attributes(vertex, ["px", "py", "pz"])

            if load is not None:
                vector = Vector(*load) * self.scale_loads
                if vector.length > self.tol_vectors:
                    name = "{}.vertex.{}.load".format(self.mesh.name, vertex)
                    attr = self.compile_attributes(name=name, color=self.loadcolor, arrow="end")
                    point = self.mesh.vertex_point(vertex)
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

        for vertex in self.mesh.vertices_where(is_support=False):
            thickness = self.mesh.vertex_attribute(vertex, "t")

            if thickness:
                area = self.mesh.vertex_area(vertex)
                weight = area * thickness
                point = self.mesh.vertex_point(vertex)
                vector = Vector(0, 0, -weight * self.scale_selfweight)
                if vector.length > self.tol_vectors:
                    line = Line.from_point_and_vector(point, vector)
                    name = "{}.vertex.{}.selfweight".format(self.mesh.name, vertex)
                    attr = self.compile_attributes(name=name, color=self.selfweightcolor, arrow="end")
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.selfweightgroup:
                self.add_to_group(self.selfweightgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_forces(self):
        guids = []

        for edge in self.mesh.edges():
            force = self.mesh.edge_attribute(edge, "_f")

            if force != 0:
                line = self.mesh.edge_line(edge)
                radius = abs(force) * self.scale_forces
                color = self.compressioncolor
                if radius > self.tol_pipes:
                    pipe = Cylinder.from_line_and_radius(line, radius)
                    name = "{}.edge.{}.force".format(self.mesh.name, edge)
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

        for vertex in self.mesh.vertices_where(is_support=True):
            residual = Vector(*self.mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"]))

            vector = residual * self.scale_residuals
            if vector.length > self.tol_vectors:
                name = "{}.vertex.{}.reaction".format(self.mesh.name, vertex)
                attr = self.compile_attributes(name=name, color=self.reactioncolor, arrow="end")
                point = self.mesh.vertex_point(vertex)
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

        for vertex in self.mesh.vertices_where(is_support=False):
            residual = Vector(*self.mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"]))

            vector = residual * -self.scale_residuals
            if vector.length > self.tol_vectors:
                name = "{}.vertex.{}.residual".format(self.mesh.name, vertex)
                attr = self.compile_attributes(name=name, color=self.residualcolor, arrow="end")
                point = self.mesh.vertex_point(vertex)
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
