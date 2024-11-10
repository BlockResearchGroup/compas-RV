from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import angle_vectors
from compas.itertools import pairwise
from compas_fd.solvers import fd_numpy


class Pattern(Mesh):
    """
    Data structure for force layout patterns that are the basis for form diagrams.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes.update({"openings": {}})
        self.default_vertex_attributes.update(
            {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "is_fixed": False,
                "is_support": False,
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
        vertex_index = self.vertex_index()
        xyz = self.vertices_attributes("xyz")
        loads = [[0.0, 0.0, 0.0] for _ in xyz]
        anchors = [vertex_index[key] for key in self.vertices_where(is_support=True)]
        fixed = [vertex_index[key] for key in self.vertices_where(is_fixed=True)]
        supports = list(set(anchors + fixed))
        edges = [(vertex_index[u], vertex_index[v]) for u, v in self.edges()]
        q = self.edges_attribute("q")
        result = fd_numpy(vertices=xyz, fixed=supports, edges=edges, forcedensities=q, loads=loads)
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

    def split_boundary(self):
        """Split the boundary into openings based on the location of the anchors.

        The algorithm assumes that the first boundary of the mesh is the exterior boundary.

        Returns
        -------
        list[list[int]]

        """
        boundaries = self.vertices_on_boundaries()
        exterior = boundaries[0]
        if exterior[-1] == exterior[0]:
            del exterior[-1]
        anchors = list(self.vertices_where(is_support=True))
        anchors = sorted(anchors, key=lambda a: exterior.index(a))
        index = exterior.index(anchors[0])
        exterior = exterior[index:] + exterior[:index]
        exterior.append(exterior[0])
        openings = []
        i = 0
        for anchor in anchors[1:]:
            j = exterior.index(anchor)
            openings.append(exterior[i : j + 1])
            i = j
        openings.append(exterior[j:])
        return [opening for opening in openings if len(opening) > 2]

    def compute_sag(self, opening):
        """Compute the sag of the opening as the ratio of the rise of the opening over its span.

        Parameters
        ----------
        opening : list[int]

        Returns
        -------
        float

        """
        start = self.vertex_point(opening[0])
        end = self.vertex_point(opening[-1])
        span = Line(start, end)
        distances = [self.vertex_point(vertex).distance_to_line(span) for vertex in opening[1:-1]]
        rise = max(distances)
        return rise / span.length

    def init_openings(self, minsag: float = 0.1) -> tuple[list[list[int]], list[float]]:
        """Initialise the boundary openings by imposing a minimal sag.

        Parameters
        ----------
        minsag : float, optional
            Minimal value for boundary sag.

        Returns
        -------
        tuple[list[list[int]], list[float]]

        """
        openings = self.split_boundary()

        targets = []
        for opening in openings:
            sag = self.compute_sag(opening)
            sag = max(sag, minsag)
            targets.append(sag)

        self.relax()
        self.match_opening_sag_targets(openings, targets)

        return openings, targets

    def match_opening_sag_targets(self, openings: list[list[int]], targets: list[float]) -> None:
        """Iteratively update the force densities in the opneing edges to match the target sag values.

        Parameters
        ----------
        openings : list[list[int]]
            The vertices of the openings.
        targets : list[float]
            The target sag values.

        """
        count = 0
        while count < 10:
            count += 1
            current = [self.compute_sag(opening) for opening in openings]

            if all(abs(sag - target) < 0.01 for sag, target in zip(current, targets)):
                break

            for sag, target, opening in zip(current, targets, openings):
                scale = sag / target

                for u, v in pairwise(opening):
                    q = self.edge_attribute((u, v), name="q")
                    self.edge_attribute((u, v), name="q", value=scale * q)

            self.relax()
