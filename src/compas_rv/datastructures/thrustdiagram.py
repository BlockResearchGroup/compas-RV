from compas.geometry import Box
from compas.geometry import bounding_box
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import subtract_vectors

from .formdiagram import FormDiagram


class ThrustDiagram(FormDiagram):
    """Data structure for thrust diagrams."""

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
