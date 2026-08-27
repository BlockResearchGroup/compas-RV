VERTEX_ATTRIBUTES = ["px", "py", "pz", "pzext", "_rx", "_ry", "_rz"]
EDGE_ATTRIBUTES = ["q", "_f"]


def invert_formdiagram_signs(formdiagram):
    """Invert the equilibrium sign convention of a form diagram.

    Notes
    -----
    Applying this function twice restores the original values.

    """
    for vertex in formdiagram.vertices():
        values = formdiagram.vertex_attributes(vertex, VERTEX_ATTRIBUTES)
        formdiagram.vertex_attributes(vertex, VERTEX_ATTRIBUTES, [-value if value is not None else None for value in values])

    for edge in formdiagram.edges_where(_is_edge=True):
        values = formdiagram.edge_attributes(edge, EDGE_ATTRIBUTES)
        formdiagram.edge_attributes(edge, EDGE_ATTRIBUTES, [-value if value is not None else None for value in values])
