from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import Pattern


class RhinoPatternObject(RUIMeshObject):
    mesh: Pattern

    freecolor = ColorAttribute(default=Color.white())
    anchorcolor = ColorAttribute(default=Color.red())
    fixedcolor = ColorAttribute(default=Color.blue())

    def __init__(
        self,
        show_supports=True,
        show_fixed=True,
        show_free=False,
        disjoint=True,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

        self.show_supports = show_supports
        self.show_fixed = show_fixed
        self.show_free = show_free

    @property
    def settings(self):
        settings = super().settings

        settings["show_supports"] = self.show_supports
        settings["show_fixed"] = self.show_fixed
        settings["show_free"] = self.show_free

        return settings

    def draw(self):
        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_support"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.mesh.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        super().draw()
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
