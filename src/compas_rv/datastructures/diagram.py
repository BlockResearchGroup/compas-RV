from compas.datastructures import Mesh
from compas.geometry import angle_vectors


class Diagram(Mesh):
    """
    Base data structure for form, force and thrust diagrams.
    """

    def edge_loop(self, uv):
        """
        Identify all edges on the same loop as a given edge.
        This implementation is different than the base implmentation in the mesh data structure,
        because of the "unloaded" faces in form, force, and thrust diagrams.

        Parameters
        ----------
        uv : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        list[tuple[int, int]]
            A list of edge identifiers.

        """
        u, v = uv
        f1, f2 = self.edge_faces(uv)

        if f1 is not None and not self.face_attribute(f1, "_is_loaded"):
            loop = []
            for edge in self.face_halfedges(f1):
                if self.edge_attribute(edge, "_is_edge"):
                    loop.append(edge)

        elif f2 is not None and not self.face_attribute(f2, "_is_loaded"):
            loop = []
            for edge in self.face_halfedges(f2):
                if self.edge_attribute(edge, "_is_edge"):
                    loop.append(edge)

        else:
            forward = super(Diagram, self).halfedge_loop((u, v))
            backward = super(Diagram, self).halfedge_loop((v, u))
            loop = []
            for u, v in forward:
                loop.append((u, v))
                if self.vertex_attribute(v, "is_fixed"):
                    break
            if not self.vertex_attribute(backward[0][0], "is_fixed"):
                for u, v in backward:
                    loop.insert(0, (v, u))
                    if self.vertex_attribute(v, "is_fixed"):
                        break
        return loop

    def collapse_small_edges(self, tol=1e-2):
        """
        Collapse the edges that are shorter than a given length.

        Parameters
        ----------
        tol : float, optional
            The threshold length.
            Edges with a length shorter than this value
            will be collapsed.

        Returns
        -------
        None

        """
        for edge in list(self.edges()):
            if self.has_edge(edge):
                if self.edge_length(edge) < tol:
                    self.collapse_edge(edge, t=0.5, allow_boundary=True)

    def smooth(self, fixed, kmax=10):
        """
        Apply area smoothing to the mesh geometry.

        Parameters
        ----------
        fixed : list[int]
            The vertices to keep fixed.
        kmax : int, optional
            The number of smoothing iterations.

        Returns
        -------
        None

        """
        self.smooth_area(self, fixed=fixed, kmax=kmax)

    def corner_vertices(self, tol=160):
        """
        Identify the corner vertices.

        Parameters
        ----------
        tol : float, optional
            The threshold value for the angle formed between two edges at a vertex
            for it to be considered a corner.
            Vertices with smaller angles are considered a corner.

        Returns
        -------
        list[int]

        """
        vkeys = []
        for key in self.vertices_on_boundary():
            if self.vertex_degree(key) == 2:
                vkeys.append(key)
            else:
                nbrs = []
                for nkey in self.vertex_neighbors(key):
                    if self.is_edge_on_boundary(key, nkey):
                        nbrs.append(nkey)
                u = self.edge_vector(key, nbrs[0])
                v = self.edge_vector(key, nbrs[1])
                if angle_vectors(u, v, deg=True) < tol:
                    vkeys.append(key)
        return vkeys

    def edge_loop_vertices(self, uv):
        """
        Identify all vertices on an edge loop.

        Parameters
        ----------
        uv : tuple[int, int]
            The identifier of the base edge of the loop.

        Returns
        -------
        list[int]

        """
        edges = self.edge_loop(uv)
        if len(edges) == 1:
            return edges[0]
        vertices = [edge[0] for edge in edges]
        if edges[-1][1] != edges[0][0]:
            vertices.append(edges[-1][1])
        return vertices
