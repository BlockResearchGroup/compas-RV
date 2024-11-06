import rhinoscriptsyntax as rs  # type: ignore

from compas.colors import Color
from compas.scene.descriptors.color import ColorAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import Pattern
from compas_rv.session import RVSession


class RhinoPatternObject(RUIMeshObject):
    session = RVSession()
    mesh: Pattern

    freecolor = ColorAttribute(default=Color.white())
    anchorcolor = ColorAttribute(default=Color.red())
    fixedcolor = ColorAttribute(default=Color.blue())

    def __init__(
        self,
        disjoint=True,
        **kwargs,
    ):
        super().__init__(disjoint=disjoint, **kwargs)

    def draw_vertices(self):
        for vertex in self.mesh.vertices():
            if self.mesh.vertex_attribute(vertex, "is_support"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.mesh.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        return super().draw_vertices()

    def redraw_vertices(self):
        self.clear_vertices()
        self.draw_vertices()
        rs.Redraw()

    def redraw_edges(self):
        self.clear_edges()
        self.draw_edges()
        rs.Redraw()

    def redraw_faces(self):
        self.clear_faces()
        self.draw_faces()
        rs.Redraw()

    def redraw(self):
        self.clear()
        self.draw()
        rs.Redraw()
