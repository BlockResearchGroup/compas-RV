from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import ForceDiagram


class RhinoForceObject(RUIMeshObject):
    mesh: ForceDiagram

    vertexcolor = ColorDictAttribute(default=Color.blue())
    edgecolor = ColorDictAttribute(default=Color.blue().darkened(50))
    facecolor = ColorDictAttribute(default=Color.blue().lightened(25))

    freecolor = ColorAttribute(default=Color.white())
    anchorcolor = ColorAttribute(default=Color.red())
    fixedcolor = ColorAttribute(default=Color.blue())

    def __init__(
        self,
        disjoint=True,
        show_supports=True,
        show_fixed=True,
        show_free=False,
        show_angles=False,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

        self.show_edges = True
        self.show_faces = False

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

    def draw_angles(self):
        pass
