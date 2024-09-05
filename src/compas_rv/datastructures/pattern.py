from compas.datastructures import Mesh
from compas.geometry import angle_vectors


class Pattern(Mesh):
    """
    Data structure for force layout patterns that are the basis for form diagrams.
    """

    def __init__(self, *args, **kwargs):
        super(Pattern, self).__init__(*args, **kwargs)
        self.attributes.update({"openings": {}})
        self.default_vertex_attributes.update(
            {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "constraints": None,
                "is_fixed": False,
            }
        )
        self.default_edge_attributes.update(
            {
                "q": 1.0,
                "lmin": 1e-6,
                "lmax": 1e6,
            }
        )

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
        for key in list(self.edges()):
            if self.has_edge(key):
                u, v = key
                if self.edge_length(u, v) < tol:
                    self.collapse_edge(u, v, t=0.5, allow_boundary=True)

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

    def relax(self):
        """
        Relax the mesh using the force density method with the curent edge force densities.

        Returns
        -------
        None

        """
        from compas_fd.solvers import fd_numpy

        vertex_index = self.vertex_index()
        xyz = self.vertices_attributes("xyz")
        loads = [[0.0, 0.0, 0.0] for _ in xyz]
        fixed = [vertex_index[key] for key in self.vertices_where(is_fixed=True)]
        edges = [(vertex_index[u], vertex_index[v]) for u, v in self.edges()]
        q = self.edges_attribute("q")
        result = fd_numpy(vertices=xyz, fixed=fixed, edges=edges, forcedensities=q, loads=loads)
        for key in self.vertices():
            index = vertex_index[key]
            self.vertex_attributes(key, "xyz", result.vertices[index])

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
