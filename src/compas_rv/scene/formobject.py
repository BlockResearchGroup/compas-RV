from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import FormDiagram


class RhinoFormObject(RUIMeshObject):
    mesh: FormDiagram

    vertexcolor = ColorDictAttribute(default=Color.green())
    edgecolor = ColorDictAttribute(default=Color.green().darkened(50))
    facecolor = ColorDictAttribute(default=Color.green().lightened(25))

    freecolor = ColorAttribute(default=Color.green())
    anchorcolor = ColorAttribute(default=Color.red())
    fixedcolor = ColorAttribute(default=Color.cyan())

    def __init__(
        self,
        show_supports=True,
        show_fixed=True,
        show_free=False,
        show_angles=False,
        disjoint=True,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

        self.show_faces = False
        self.show_edges = True
        self.show_vertices = True
        self.show_supports = show_supports
        self.show_fixed = show_fixed
        self.show_free = show_free
        self.show_angles = show_angles

    @property
    def settings(self):
        settings = super().settings

        settings["show_supports"] = self.show_supports
        settings["show_fixed"] = self.show_fixed
        settings["show_free"] = self.show_free
        settings["show_angles"] = self.show_angles

        return settings

    def draw(self):
        return super().draw()

    def draw_vertices(self):
        vertices = []

        if self.show_vertices is True:
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
        if self.show_edges is True:
            edges += list(self.mesh.edges_where(_is_edge=True))
            if edges:
                self.show_edges = edges

        for edge in self.mesh.edges_where(_is_edge=True):
            pass

        return super().draw_edges()

    def draw_faces(self):
        faces = []
        if self.show_faces is True:
            faces += list(self.mesh.faces_where(_is_loaded=True))
            if faces:
                self.show_faces = faces

        for face in self.mesh.faces_where(_is_loaded=True):
            pass

        return super().draw_faces()
