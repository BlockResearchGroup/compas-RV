from compas.geometry import angle_vectors_xy
from compas.geometry import cross_vectors
from compas_tna.diagrams import ForceDiagram

from .diagram import Diagram
from .formdiagram import FormDiagram  # noqa: F401


class ForceDiagram(Diagram, ForceDiagram):
    """
    Data structure for force diagrams.
    """

    def primal_edge(self, edge):
        """
        Get the corresponding edge in the FormDiagram.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge in this diagram.

        Returns
        -------
        tuple[int, int]
            The identifier of the edge in the other/primal diagram.

        Raises
        ------
        KeyError
            If the dual edge does not exist.

        """
        primal = self.primal  # type: FormDiagram

        f1, f2 = edge
        for u, v in primal.face_halfedges(f1):
            if primal.halfedge[v][u] == f2:
                return u, v
        raise KeyError(edge)

    def update_angle_deviations(self):
        """
        Compute the angle deviation with the corresponding edge in the FormDiagram.

        Returns
        -------
        None

        """
        primal = self.primal  # type: FormDiagram

        for edge in self.edges():
            edge_ = self.primal_edge(edge)
            uv = self.edge_vector(edge)
            uv_ = primal.edge_vector(edge_)
            a = angle_vectors_xy(uv, cross_vectors(uv_, (0, 0, 1)), deg=True)
            if primal.edge_attribute(edge_, "_is_tension"):
                a = 180 - a
            self.edge_attribute(edge, "_a", a)
            primal.edge_attribute(edge_, "_a", a)
