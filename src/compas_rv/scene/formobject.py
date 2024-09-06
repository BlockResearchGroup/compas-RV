from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import FormDiagram


class RhinoFormObject(RUIMeshObject):
    mesh: FormDiagram

    freecolor = ColorAttribute(default=Color.white())
    anchorcolor = ColorAttribute(default=Color.red())
    fixedcolor = ColorAttribute(default=Color.blue())

    def __init__(
        self,
        show_anchors=True,
        show_fixed=True,
        show_free=False,
        disjoint=True,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

        self.show_faces = False
        self.show_edges = True

        self.show_anchors = show_anchors
        self.show_fixed = show_fixed
        self.show_free = show_free

    @property
    def settings(self):
        settings = super().settings

        settings["show_anchors"] = self.show_anchors
        settings["show_fixed"] = self.show_fixed
        settings["show_free"] = self.show_free

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

        return super().draw()

    def draw_vertices(self):
        vertices = []
        if self.show_free:
            vertices += list(self.mesh.vertices_where(is_support=False, is_fixed=False))
        if self.show_fixed:
            vertices += list(self.mesh.vertices_where(is_fixed=True))
        if self.show_anchors:
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

        return super().draw_edges()

    def draw_faces(self):
        faces = []
        if self.show_faces:
            faces += list(self.mesh.faces_where(_is_loaded=True))
        if faces:
            self.show_faces = faces

        return super().draw_faces()

    def draw_angles(self):
        pass
