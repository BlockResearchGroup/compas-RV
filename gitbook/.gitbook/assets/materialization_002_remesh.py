#! python3
# venv: brg-csd
# r: compas_rv

import pathlib

import compas
from compas.datastructures import Mesh
from compas.scene import Scene
from compas import json_dump
from compas.datastructures.mesh.remesh import trimesh_remesh
from compas.geometry import Line
from compas.geometry import normal_triangle
from compas.geometry import KDTree
from compas_model.geometry import intersection_ray_triangle

# =============================================================================
# Load data
# =============================================================================

IFILE = pathlib.Path(__file__).parent / "001_mesh.json"
mesh = compas.json_load(IFILE)

# =============================================================================
# Trimesh
#
# - convert a copy of the mesh to a trimesh using "quads to triangles"
# - note that this doesn't work for other patterns
# =============================================================================

trimesh: Mesh = mesh.copy()
trimesh.quads_to_triangles()

# =============================================================================
# Trimesh: Remeshing
#
# - remesh using CGAL
# - use a percentage of the average edge length of the original mesh as target length
# =============================================================================


length = sum(mesh.edge_length(edge) for edge in mesh.edges()) / mesh.number_of_edges()

def project(mesh: Mesh, k, args):
    for vertex in mesh.vertices():
        if mesh.is_vertex_on_boundary(vertex):
            continue
        point = mesh.vertex_point(vertex)
        _, nbr, _ = tree.nearest_neighbor(point)
        triangles = vertex_triangles[nbr]
        for triangle in triangles:
            normal = normal_triangle(triangle)
            ray = Line.from_point_direction_length(point, normal, 10)
            result = intersection_ray_triangle(ray, triangle)
            if result:
                mesh.vertex_attributes(vertex, "xyz", result)
                break

vertex_index = {vertex: index for index, vertex in enumerate(trimesh.vertices())}
vertex_triangles = {vertex_index[vertex]: [trimesh.face_points(face) for face in trimesh.vertex_faces(vertex)] for vertex in trimesh.vertices()}
vertices = trimesh.vertices_attributes("xyz")
tree = KDTree(vertices)

fixed = list(trimesh.vertices_on_boundary())
free = set(list(trimesh.vertices())) - set(fixed)

trimesh_remesh(trimesh, length, kmax=300, tol=0.1, allow_boundary_split=False, callback=project)


# =============================================================================
# Serialize
# =============================================================================

json_dump(trimesh, pathlib.Path(__file__).parent / "002_mesh.json")

# =============================================================================
# Visualisation
# =============================================================================

scene = Scene()
scene.clear_context()
scene.add(trimesh)
scene.draw()
