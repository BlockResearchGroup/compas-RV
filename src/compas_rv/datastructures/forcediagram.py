from compas.geometry import Box
from compas.geometry import angle_vectors_xy
from compas.geometry import bounding_box
from compas.geometry import cross_vectors
from compas_fd.solvers import fd_numpy
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
        primal: FormDiagram = self.primal

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
        primal: FormDiagram = self.primal

        for edge in self.edges():
            edge_ = self.primal_edge(edge)
            uv = self.edge_vector(edge)
            uv_ = primal.edge_vector(edge_)
            a = angle_vectors_xy(uv, cross_vectors(uv_, (0, 0, 1)), deg=True)
            if primal.edge_attribute(edge_, "_is_tension"):
                a = 180 - a
            self.edge_attribute(edge, "_a", a)
            primal.edge_attribute(edge_, "_a", a)

    def update_position(self, margin: float = 1.3) -> None:
        """Update the position of the diagram based on the size and position of the form diagram.

        Parameters
        ----------
        margin : float, optional
            Multiplication factor for the size of the bounding box of the form diagram in the X direction.

        Returns
        -------
        None

        """
        primal: FormDiagram = self.primal

        bbox_form = Box.from_bounding_box(bounding_box(primal.vertices_attributes("xyz")))
        bbox_force = Box.from_bounding_box(bounding_box(self.vertices_attributes("xyz")))

        y_form = bbox_form.ymin + 0.5 * (bbox_form.ymax - bbox_form.ymin)
        y_force = bbox_force.ymin + 0.5 * (bbox_force.ymax - bbox_force.ymin)
        dx = margin * (bbox_form.xmax - bbox_form.xmin) + (bbox_form.xmin - bbox_force.xmin)
        dy = y_form - y_force

        self.translate([dx, dy, 0])

    def solve_fd(self) -> None:
        """Relax the mesh using the force density method with the curent edge force densities of te corresponding form diagram.

        Returns
        -------
        None

        """
        vertex_index = self.vertex_index()

        xyz = self.vertices_attributes("xyz")
        loads = [[0.0, 0.0, 0.0] for _ in xyz]

        fixed = list(self.vertices_where(is_support=True))
        fixed += list(self.vertices_where(is_fixed=True))
        if len(fixed) < 4:
            fixed += self.vertices_on_boundary()
        fixed = list(set([vertex_index[vertex] for vertex in fixed]))

        edges = list(self.edges())
        qinv = [self.form_edge_attribute(self.primal, edge, name="q") for edge in edges]
        q = [1 / value for value in qinv]

        edges = [(vertex_index[u], vertex_index[v]) for u, v in edges]

        result = fd_numpy(
            vertices=xyz,
            fixed=fixed,
            edges=edges,
            forcedensities=q,
            loads=loads,
        )

        for key in self.vertices():
            index = vertex_index[key]
            self.vertex_attributes(key, "xyz", result.vertices[index])
