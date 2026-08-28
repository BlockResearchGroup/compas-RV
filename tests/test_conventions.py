from compas_rv.conventions import invert_formdiagram_signs


class FormDiagram:
    def __init__(self):
        self.vertex = {
            0: {"px": 1.0, "py": 2.0, "pz": 3.0, "pzext": 7.0, "_rx": 4.0, "_ry": 5.0, "_rz": 6.0},
            1: {"px": 0.0, "py": 0.0, "pz": 7.0, "pzext": None, "_rx": 0.0, "_ry": 0.0, "_rz": 0.0},
        }
        self.edge = {(0, 1): {"q": 8.0, "_f": 9.0, "_is_edge": True}}

    def vertices(self):
        return iter(self.vertex)

    def edges_where(self, **conditions):
        return (edge for edge, attributes in self.edge.items() if all(attributes[name] == value for name, value in conditions.items()))

    def vertex_attributes(self, vertex, names, values=None):
        if values is None:
            return [self.vertex[vertex][name] for name in names]
        for name, value in zip(names, values):
            self.vertex[vertex][name] = value

    def edge_attributes(self, edge, names, values=None):
        if values is None:
            return [self.edge[edge][name] for name in names]
        for name, value in zip(names, values):
            self.edge[edge][name] = value


def test_invert_formdiagram_signs_is_involutive():
    formdiagram = FormDiagram()

    invert_formdiagram_signs(formdiagram)

    assert formdiagram.vertex[0] == {"px": -1.0, "py": -2.0, "pz": -3.0, "pzext": -7.0, "_rx": -4.0, "_ry": -5.0, "_rz": -6.0}
    assert formdiagram.vertex[1] == {"px": -0.0, "py": -0.0, "pz": -7.0, "pzext": None, "_rx": -0.0, "_ry": -0.0, "_rz": -0.0}
    assert formdiagram.edge[(0, 1)] == {"q": -8.0, "_f": -9.0, "_is_edge": True}

    invert_formdiagram_signs(formdiagram)

    assert formdiagram.vertex[0] == {"px": 1.0, "py": 2.0, "pz": 3.0, "pzext": 7.0, "_rx": 4.0, "_ry": 5.0, "_rz": 6.0}
    assert formdiagram.vertex[1] == {"px": 0.0, "py": 0.0, "pz": 7.0, "pzext": None, "_rx": 0.0, "_ry": 0.0, "_rz": 0.0}
    assert formdiagram.edge[(0, 1)] == {"q": 8.0, "_f": 9.0, "_is_edge": True}
