import numpy as np
import scipy.sparse as sps

from compas.linalg import spsolve_with_known
from compas.matrices import connectivity_matrix
from compas_rv.datastructures import ForceDiagram
from compas_rv.datastructures import FormDiagram
from compas_tna.equilibrium.diagrams import rot90


def update_force_from_form(force: ForceDiagram, form: FormDiagram):
    vertex_index = form.vertex_index()

    xy = np.array(form.vertices_attributes("xy"), dtype=np.float64)
    edges = [[vertex_index[u], vertex_index[v]] for u, v in form.edges_where(_is_edge=True)]
    C: sps.csr_matrix = connectivity_matrix(edges, "csr")
    Q = sps.diags([form.edges_attribute("q", keys=list(form.edges_where(_is_edge=True)))], [0])
    uv = C.dot(xy)

    _vertex_index = force.vertex_index()

    _known = [0]

    _xy = np.array(force.vertices_attributes("xy"), dtype=np.float64)
    _xy[:] = rot90(_xy, +1.0)

    _edges = force.ordered_edges(form)
    _edges[:] = [(_vertex_index[u], _vertex_index[v]) for u, v in _edges]

    _C: sps.csr_matrix = connectivity_matrix(_edges, "csr")
    _Ct = _C.transpose()

    _xy = spsolve_with_known(_Ct.dot(_C), _Ct.dot(Q).dot(uv), _xy, _known)
    _xy[:] = rot90(_xy, -1.0)

    for vertex, attr in force.vertices(True):
        index = _vertex_index[vertex]
        attr["x"] = _xy[index, 0]
        attr["y"] = _xy[index, 1]
