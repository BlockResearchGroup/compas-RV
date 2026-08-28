#! python3
# venv: brg-csd
# r: compas_rv>=0.10.0

import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession


def invert_vertical_loads(formdiagram):
    for vertex in formdiagram.vertices():
        pz = formdiagram.vertex_attribute(vertex, "pz")
        formdiagram.vertex_attribute(vertex, "pz", -pz if pz is not None else 0.0)


def clear_optimised_loads(formdiagram):
    for vertex in formdiagram.vertices():
        formdiagram.unset_vertex_attribute(vertex, "pzext")


def select_loaded_vertices(formobject):
    candidates = list(formobject.diagram.vertices_where(is_support=False))
    return formobject.select_thrust_vertices(
        vertices=candidates,
        message="Select vertices for external loads",
        use_edges=False,
    )


def RunCommand():
    session = RVSession()

    formobject = session.find_formdiagram()
    if not formobject:
        return

    option = rs.GetString("Load source", "FromEnvelope", ["FromEnvelope", "External", "FromFill", "ClearAll"])
    if not option:
        return

    formdiagram = formobject.diagram
    envelope = None

    if option in ("FromEnvelope", "FromFill"):
        envelope = session.find_envelope()
        if not envelope:
            return

    if option == "FromEnvelope":
        normalize = rs.GetString("Normalize loads to envelope self-weight", "Yes", ["Yes", "No"])
        if not normalize:
            return

        envelope.apply_selfweight_to_formdiagram(formdiagram, normalize=normalize == "Yes")
        invert_vertical_loads(formdiagram)
        clear_optimised_loads(formdiagram)
        print("Self-weight from the envelope applied to the FormDiagram.")

    elif option == "External":
        vertices = select_loaded_vertices(formobject)
        if not vertices:
            return session.warn("Select at least one non-support vertex.")

        load = rs.GetReal("External vertical load (positive downward)", 1.0, minimum=0.0)
        if load is None:
            return

        for vertex in vertices:
            pz = formdiagram.vertex_attribute(vertex, "pz") or 0.0
            formdiagram.vertex_attribute(vertex, "pz", pz + load)
            print("Load at vertex {0} updated from {1:.2f} to {2:.2f}".format(vertex, pz, pz + load))
        clear_optimised_loads(formdiagram)

    elif option == "FromFill":
        if not envelope.fill:
            return session.warn("There is no Fill mesh. Re-create the envelope with a fill mesh.")

        invert_vertical_loads(formdiagram)
        try:
            envelope.apply_fill_weight_to_formdiagram(formdiagram)
        finally:
            invert_vertical_loads(formdiagram)
        clear_optimised_loads(formdiagram)
        print("Fill weight applied to the FormDiagram.")

    elif option == "ClearAll":
        formdiagram.vertices_attribute(name="pz", value=0.0)
        clear_optimised_loads(formdiagram)
        formdiagram.attributes["loads_from_envelope"] = False
        print("All vertical loads cleared from the FormDiagram.")

    else:
        raise NotImplementedError

    if option != "ClearAll":
        formdiagram.attributes["loads_from_envelope"] = True
    formobject.show_thrust = True
    session.settings.drawing.show_loads = True

    rs.UnselectAllObjects()
    formobject.redraw()
    rs.Redraw()

    if session.settings.autosave:
        session.record(name="Update Loads")


if __name__ == "__main__":
    RunCommand()
