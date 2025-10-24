from compas.geometry import Box
from compas.geometry import bounding_box
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import sum_vectors
from compas_fd.solvers import fd_numpy
from compas_tna.diagrams import FormDiagram as BaseFormDiagram

from .diagram import Diagram
from .pattern import Pattern


class FormDiagram(Diagram, BaseFormDiagram):
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
        xyz: list[list[float]] = self.vertices_attributes("xyz")  # type: ignore
        loads = [[0.0, 0.0, 0.0] for _ in xyz]
        fixed = [vertex_index[key] for key in self.vertices_where(is_support=True)]
        fixed += [vertex_index[key] for key in self.vertices_where(is_fixed=True)]
        edges = list(self.edges_where(_is_edge=True))
        q: list[float] = self.edges_attribute("q", keys=edges)  # type: ignore
        edges = [(vertex_index[u], vertex_index[v]) for u, v in edges]
        result = fd_numpy(vertices=xyz, fixed=fixed, edges=edges, forcedensities=q, loads=loads)
        for vertex in self.vertices():
            index = vertex_index[vertex]
            self.vertex_attributes(vertex, "xyz", result.vertices[index])
            self.vertex_attributes(vertex, ["_rx", "_ry", "_rz"], result.residuals[index])

    def flip_cycles_if_normal_down(self):
        """Flip the cycles of the diagram if the average normal points downward."""
        normals = [self.face_normal(face) for face in self.faces_where(_is_loaded=True)]
        scale = 1 / len(normals)
        normal = scale_vector(sum_vectors(normals), scale)
        if normal[2] < 0:
            self.flip_cycles()

    def vertex_tributary_area(self, vertex: int) -> float:
        """
        Compute the tributary area of a vertex taking into account only the loaded faces.

        Parameters
        ----------
        vertex : int
            The vertex identifier.

        Returns
        -------
        float

        """
        area = 0
        p0 = self.vertex_coordinates(vertex)
        for nbr in self.halfedge[vertex]:
            p1 = self.vertex_coordinates(nbr)
            v1 = subtract_vectors(p1, p0)
            fkey = self.halfedge[vertex][nbr]
            if fkey is not None:
                if self.face_attribute(fkey, "_is_loaded"):
                    p2 = self.face_centroid(fkey)
                    v2 = subtract_vectors(p2, p0)
                    area += length_vector(cross_vectors(v1, v2))
            fkey = self.halfedge[nbr][vertex]
            if fkey is not None:
                if self.face_attribute(fkey, "_is_loaded"):
                    p3 = self.face_centroid(fkey)
                    v3 = subtract_vectors(p3, p0)
                    area += length_vector(cross_vectors(v1, v3))
        return 0.25 * area

    def vertex_lumped_stress(self, vertex: int) -> float:
        """
        Compute an approximation of the compressive stress at a vertex.

        Parameters
        ----------
        vertex : int
            The vertex identifier.

        Returns
        -------
        float

        """
        stress = 0
        neighbors = self.vertex_neighbors(vertex)
        count = 0
        for nbr in neighbors:
            edge_area = 0
            edge_thickness = sum(self.vertices_attribute("t", keys=[vertex, nbr])) / 2
            edge_force = self.edge_attribute((vertex, nbr), "_f")

            if abs(edge_force) <= 0:
                continue

            mp = self.edge_midpoint((vertex, nbr))

            f0 = self.halfedge_face((vertex, nbr))
            if f0 is not None:
                if self.face_attribute(f0, "_is_loaded"):
                    f0_c = self.face_center(f0)
                    area = length_vector(subtract_vectors(f0_c, mp)) * edge_thickness
                    if area > 0:
                        edge_area += area
            f1 = self.halfedge_face((nbr, vertex))
            if f1 is not None:
                if self.face_attribute(f1, "_is_loaded"):
                    f1_c = self.face_center(f1)
                    area = length_vector(subtract_vectors(f1_c, mp)) * edge_thickness
                    if area > 0:
                        edge_area += area

            if edge_area > 0:
                stress += edge_force / edge_area
                count += 1

        return stress / count

    def compute_zmax(self) -> float:
        """Compute a suitable value for zmax based on the length of the diagonal of the bounding box of the projection of the diagram in XY.

        Returns
        -------
        float
            Maximum Z coordinate.

        """
        bbox = Box.from_bounding_box(bounding_box(self.vertices_attributes("xyz")))
        diagonal = bbox.points[2] - bbox.points[0]
        return 0.25 * diagonal.length
