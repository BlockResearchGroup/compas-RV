from itertools import groupby

from compas.datastructures import Mesh
from compas.datastructures.mesh.subdivision import mesh_fast_copy
from compas.tolerance import TOL


class SubdMesh(Mesh):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_edge_attributes.update(
            {
                "brep_curve": None,
                "brep_curve_pts": [],
                "brep_curve_dir": None,
            }
        )
        self.default_face_attributes.update(
            {
                "is_quad": False,
                "u_edge": None,
                "v_edge": None,
                "nu": 4,
                "nv": 4,
                "n": 2,
                "brep_face": None,
            }
        )
        self._edge_strips = {}

    # @classmethod
    # def from_guid(cls, guid):
    #     """
    #     Construct a subd mesh from a GUID representing a surface or polysurface in Rhino.

    #     Parameters
    #     ----------
    #     guid : System.Guid
    #         The GUID of the input surface.

    #     Returns
    #     -------
    #     :class:`SubdMesh`

    #     """
    #     import compas_rhino.conversions
    #     import compas_rhino.objects
    #     import Rhino  # type: ignore

    #     rhinosurface = compas_rhino.objects.find_object(guid)
    #     subdmesh = compas_rhino.conversions.surface_to_compas_mesh(rhinosurface, cleanup=False)
    #     gkey_vertex = {TOL.geometric_key(subdmesh.vertex_coordinates(vertex)): vertex for vertex in subdmesh.vertices()}

    #     brep = Rhino.Geometry.Brep.TryConvertBrep(rhinosurface.Geometry)

    #     for brep_face, face in zip(brep.Faces, subdmesh.faces()):
    #         loop = brep_face.OuterLoop
    #         curve = loop.To3dCurve()
    #         segments = curve.Explode()

    #         if len(segments) == 4:
    #             domain_u = brep_face.Domain(0)
    #             domain_v = brep_face.Domain(1)
    #             u0_xyz = brep_face.PointAt(domain_u[0], domain_v[0])
    #             u1_xyz = brep_face.PointAt(domain_u[1], domain_v[0])
    #             v0_xyz = brep_face.PointAt(domain_u[0], domain_v[0])
    #             v1_xyz = brep_face.PointAt(domain_u[0], domain_v[1])
    #             u0 = gkey_vertex[TOL.geometric_key(u0_xyz)]
    #             u1 = gkey_vertex[TOL.geometric_key(u1_xyz)]
    #             v0 = gkey_vertex[TOL.geometric_key(v0_xyz)]
    #             v1 = gkey_vertex[TOL.geometric_key(v1_xyz)]
    #             names = ["is_quad", "u_edge", "v_edge", "brep_face"]
    #             values = [True, (u0, u1), (v0, v1), brep_face]
    #             subdmesh.face_attributes(face, names, values)

    #         else:
    #             for curve, edge in zip(segments, subdmesh.face_halfedges(face)):
    #                 sp = curve.PointAtStart
    #                 ep = curve.PointAtEnd
    #                 u = gkey_vertex[TOL.geometric_key(sp)]
    #                 v = gkey_vertex[TOL.geometric_key(ep)]
    #                 subdmesh.edge_attribute(edge, "brep_curve", curve)
    #                 subdmesh.edge_attribute(edge, "brep_curve_dir", (u, v))

    #     return subdmesh

    # ==========================================================================
    # topology
    # ==========================================================================

    def subd_edge_strip(self, edge):
        """
        Find the edge strip through quad and nonquad faces.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        list[tuple[int, int]]

        """

        def strip_end_faces(strip):
            # return nonquads at the end of edge strips
            faces1 = self.edge_faces(strip[0])
            faces2 = self.edge_faces(strip[-1])
            nonquads = []
            for face in faces1 + faces2:
                if face is not None and len(self.face_vertices(face)) != 4:
                    nonquads.append(face)
            return nonquads

        strip = self.edge_strip(edge)

        all_edges = list(strip)

        end_faces = set(strip_end_faces(strip))
        seen = set()

        while len(end_faces) > 0:
            face = end_faces.pop()
            if face not in seen:
                seen.add(face)
                for u, v in self.face_halfedges(face):
                    halfedge = (u, v)
                    if halfedge not in all_edges:
                        rev_hf_face = self.halfedge_face((v, u))
                        if rev_hf_face is not None:
                            if len(self.face_vertices(rev_hf_face)) != 4:
                                end_faces.add(self.halfedge_face((v, u)))
                                all_edges.append(halfedge)
                                continue
                        halfedge_strip = self.edge_strip(halfedge)
                        all_edges.extend(halfedge_strip)
                        end_faces.update(strip_end_faces(halfedge_strip))
        return all_edges

    def edge_strip_faces(self, edge_strip):
        """
        Identify all edge faces of the edge strip.

        Parameters
        ----------
        edge_strip : list[tuple[int, int]]
            A list of edges.

        Returns
        -------
        list[int]

        """
        edge_strip_faces = set()
        for edge in edge_strip:
            face1, face2 = self.edge_faces(edge)
            if face1 is not None:
                edge_strip_faces.add(face1)
            if face2 is not None:
                edge_strip_faces.add(face2)
        return list(edge_strip_faces)

    def split_boundary(self, subdmesh):
        # type: (SubdMesh) -> list[list[int]]
        """
        Split the ordered list of boundary vertices at the corners of the quadmesh.

        Parameters
        ----------
        subdmesh : :class:`SubdMesh`

        Returns
        -------
        list[list[int]]

        """
        boundaries = subdmesh.vertices_on_boundaries()
        exterior = boundaries[0]
        opening = []
        openings = [opening]
        for vertex in exterior:
            opening.append(vertex)
            if subdmesh.vertex_degree(vertex) == 2:
                opening = [vertex]
                openings.append(opening)
        openings[-1] += openings[0]
        del openings[0]
        openings[:] = [opening for opening in openings if len(opening) > 2]
        return openings

    # ==========================================================================
    # remapping
    # ==========================================================================

    # def divide_brep_curve(self, edge, n):
    #     """
    #     Divide the brep curve corresponding to an edge and store the resulting points in the edge attributes.

    #     Parameters
    #     ----------
    #     edge : tuple[int, int]
    #         The identifier of the edge.
    #     n : int
    #         The number of segments.

    #     Returns
    #     -------
    #     list[Rhino.Geometry.Point3d]

    #     """
    #     curve = self.edge_attribute(edge, "brep_curve")
    #     params = curve.DivideByCount(n, True)
    #     pts = []
    #     for param in params:
    #         pt = curve.PointAt(param)
    #         pts.append(pt)
    #     self.edge_attribute(edge, "brep_curve_pts", pts)
    #     return pts

    def remap_boundary_vertices(self, subdmesh):
        # type: (SubdMesh) -> SubdMesh
        """
        Remap the boundary vertices of a subdmesh.

        Parameters
        ----------
        subdmesh : :class:`SubdMesh`
            Another subd mesh.

        Returns
        -------
        :class:`SubdMesh`

        """
        vertex_loops = self.split_boundary(subdmesh)
        for vertex_loop in vertex_loops:
            vertex_loop = [key[0] for key in groupby(vertex_loop)]
            u = vertex_loop[0]
            v = vertex_loop[-1]
            edge = (u, v)
            pts = self.edge_attribute(edge, "brep_curve_pts")
            if pts:
                if u != self.edge_attribute(edge, "brep_curve_dir")[0]:
                    pts = pts[::-1]
                for pt, key in zip(pts[1:-1], vertex_loop[1:-1]):
                    subdmesh.vertex_attribute(key, "x", pt.X)
                    subdmesh.vertex_attribute(key, "y", pt.Y)
                    subdmesh.vertex_attribute(key, "z", pt.Z)
        return subdmesh

    # ==========================================================================
    # subdivision
    # ==========================================================================

    def subdivide_quad(self, face):
        """
        Subdivide a quad face using the underlying BRep face geometry.

        The number of subdivisions in the U and V directions
        depends on the parameters ``nu`` and ``nv`` stored in the face attributes.
        The geometry of the BRep face is also stored in the face attributes.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`Mesh`

        """
        brep_face, nu, nv = self.face_attributes(face, names=["brep_face", "nu", "nv"])

        domain_u = brep_face.Domain(0)
        domain_v = brep_face.Domain(1)

        du = (domain_u[1] - domain_u[0]) / (nu)
        dv = (domain_v[1] - domain_v[0]) / (nv)

        gkey_vertex = {}
        subdmesh = Mesh()
        for vertex in self.face_vertices(face):
            x, y, z = self.vertex_coordinates(vertex)
            subdmesh.add_vertex(vertex, {"x": x, "y": y, "z": z})
            gkey_vertex[TOL.geometric_key((x, y, z))] = vertex

        point_at = brep_face.PointAt

        for i in range(nu):
            for j in range(nv):
                a = point_at(domain_u[0] + (i + 0) * du, domain_v[0] + (j + 0) * dv)
                b = point_at(domain_u[0] + (i + 1) * du, domain_v[0] + (j + 0) * dv)
                c = point_at(domain_u[0] + (i + 1) * du, domain_v[0] + (j + 1) * dv)
                d = point_at(domain_u[0] + (i + 0) * du, domain_v[0] + (j + 1) * dv)

                vertices = []
                for pt in [a, b, c, d]:
                    gkey = TOL.geometric_key(pt)
                    if gkey not in gkey_vertex:
                        gkey_vertex[gkey] = subdmesh.add_vertex(x=pt[0], y=pt[1], z=pt[2])
                    vertex = gkey_vertex[gkey]
                    vertices.append(vertex)
                subdmesh.add_face(vertices)

        return self.remap_boundary_vertices(subdmesh)

    def subdivide_nonquad(self, nonquad):
        """
        Apply recursive quad subdivision to a nonquad face using the underlying BRep face geometry.

        The number of subdivisions ``n`` is stored in the face attributes.
        The geometry of the BRep face is also stored in the face attributes.

        Parameters
        ----------
        nonquad : int
            The identifier of the face.

        Returns
        -------
        :class:`Mesh`

        """
        n = self.face_attribute(nonquad, "n")

        mesh = Mesh()
        vertices = self.face_vertices(nonquad)
        for vertex in vertices:
            x, y, z = self.vertex_coordinates(vertex)
            mesh.add_vertex(vertex, {"x": x, "y": y, "z": z})
        mesh.add_face(vertices)

        for _ in range(n):
            subd = mesh_fast_copy(mesh)  # type: Mesh

            edgepoints = []
            for u, v in mesh.edges():
                w = subd.split_edge((u, v), allow_boundary=True)
                edgepoints.append([w, True])

            face_xyz = {face: mesh.face_centroid(face) for face in mesh.faces()}

            for face in mesh.faces():
                vertex_descendant = {i: j for i, j in subd.face_halfedges(face)}
                vertex_ancestor = {j: i for i, j in subd.face_halfedges(face)}

                x, y, z = face_xyz[face]
                c = subd.add_vertex(x=x, y=y, z=z)

                for vertex in mesh.face_vertices(face):
                    a = vertex_ancestor[vertex]
                    d = vertex_descendant[vertex]
                    subd.add_face([a, vertex, d, c])

                # del subd.face[face]
                subd.delete_face(face)
            mesh = subd

        for edge in self.face_halfedges(nonquad):
            self.divide_brep_curve(edge, 2**n)

        subdmesh = Mesh.__from_data__(mesh.__data__)
        return self.remap_boundary_vertices(subdmesh)

    # def subdivide_all_faces(self):
    #     """
    #     Subdivide all the faces of the mesh, switching between a scheme based on the UV space of the underlying surface
    #     and a basic quad scheme, for quad and non-quad faces respectively.

    #     Returns
    #     -------
    #     :class:`Mesh`

    #     """
    #     subd_meshes = []
    #     quads = []
    #     non_quads = []

    #     boundary = set()

    #     for face in self.faces():
    #         if self.face_attribute(face, "is_quad"):
    #             quads.append(face)
    #         else:
    #             non_quads.append(face)

    #     for face in non_quads:
    #         subd_mesh = self.subdivide_nonquad(face)
    #         subd_meshes.append(subd_mesh)
    #         for vertex in subd_mesh.vertices_on_boundary():
    #             xyz = subd_mesh.vertex_coordinates(vertex)
    #             boundary.add(TOL.geometric_key(xyz))

    #     for face in quads:
    #         subd_mesh = self.subdivide_quad(face)
    #         subd_meshes.append(subd_mesh)
    #         for vertex in subd_mesh.vertices_on_boundary():
    #             xyz = subd_mesh.vertex_coordinates(vertex)
    #             boundary.add(TOL.geometric_key(xyz))

    #     mesh = meshes_join_and_weld(subd_meshes, precision="2f")

    #     fixed = []
    #     for vertex in mesh.vertices():
    #         xyz = mesh.vertex_coordinates(vertex)
    #         gkey = TOL.geometric_key(xyz)
    #         if gkey in boundary:
    #             fixed.append(vertex)

    #     mesh.smooth_area(fixed=fixed, kmax=100, damping=0.5)

    #     return mesh
