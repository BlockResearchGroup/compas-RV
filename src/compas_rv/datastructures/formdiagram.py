from compas.geometry import scale_vector
from compas.geometry import sum_vectors
from compas_fd.solvers import fd_numpy
from compas_tna.diagrams import FormDiagram

from .diagram import Diagram
from .pattern import Pattern


class FormDiagram(Diagram, FormDiagram):
    """
    Data structure for form diagrams.
    """

    @classmethod
    def from_pattern(cls, pattern: Pattern) -> "FormDiagram":
        """Construct a form diagram from a pattern.

        Parameters
        ----------
        pattern : Pattern
            The pattern from which the diagram should be constructed.
        feet : {1, 2}, optional
            The number of horizontal force directions that should be added to the supports.

        Returns
        -------
        FormDiagram
            The form diagram.
        """
        form: FormDiagram = pattern.copy(cls=cls)
        form.update_boundaries()
        return form

    # not sure if this is a good idea
    # because it might clash with the parent function

    def edges_on_boundaries(self) -> list[list[tuple[int, int]]]:
        """Compute and return the edges on the perceived boundary of the diagram.

        Returns
        -------
        list[list[tuple[int, int]]]

        """
        boundaries = []
        for face in self.faces_where(_is_loaded=False):
            boundary = []
            for edge in self.face_halfedges(face):
                if self.edge_attribute(edge, name="_is_edge"):
                    boundary.append(edge)
            boundaries.append(boundary)
        return boundaries

    def is_vertex_internal(self, vertex: int) -> bool:
        """Indicate that a vertex is on perceived inside of the diagram.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool

        """
        return not any(self.is_face_on_boundary(face) for face in self.vertex_faces(vertex))

    def solve_fd(self) -> None:
        """
        Relax the mesh using the force density method with the curent edge force densities.

        Returns
        -------
        None

        """
        vertex_index = self.vertex_index()
        xyz = self.vertices_attributes("xyz")
        loads = [[0.0, 0.0, 0.0] for _ in xyz]
        fixed = [vertex_index[key] for key in self.vertices_where(is_support=True)]
        fixed += [vertex_index[key] for key in self.vertices_where(is_fixed=True)]
        edges = list(self.edges_where(_is_edge=True))
        q = self.edges_attribute("q", keys=edges)
        edges = [(vertex_index[u], vertex_index[v]) for u, v in edges]
        result = fd_numpy(vertices=xyz, fixed=fixed, edges=edges, forcedensities=q, loads=loads)
        for key in self.vertices():
            index = vertex_index[key]
            self.vertex_attributes(key, "xyz", result.vertices[index])

    def flip_cycles_if_normal_down(self):
        """Flip the cycles of the diagram if the average normal points downward."""
        normals = [self.face_normal(face) for face in self.faces_where(_is_loaded=True)]
        scale = 1 / len(normals)
        normal = scale_vector(sum_vectors(normals), scale)
        if normal[2] < 0:
            self.flip_cycles()
