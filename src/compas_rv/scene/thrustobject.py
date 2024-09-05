from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import ThrustDiagram


class RhinoThrustObject(RUIMeshObject):
    mesh: ThrustDiagram

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
        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_anchor"):
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
            vertices += list(self.mesh.vertices_where(is_anchor=False, is_fixed=False))
        if self.show_fixed:
            vertices += list(self.mesh.vertices_where(is_fixed=True))
        if self.show_anchors:
            vertices += list(self.mesh.vertices_where(is_anchor=True))

        if vertices:
            self.show_vertices = vertices

        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_anchor"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.mesh.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        return super().draw_vertices()
