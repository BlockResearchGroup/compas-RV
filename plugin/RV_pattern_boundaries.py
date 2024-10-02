#! python3
# venv: rhinovault
# r: compas>=2.4, compas_rui, compas_session, compas_tna>=0.5


import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.drawing
import compas_rhino.objects
import compas_rv.settings
from compas.geometry import centroid_points
from compas.itertools import pairwise
from compas_rv.datastructures import Pattern
from compas_rv.scene import RhinoPatternObject
from compas_session.namedsession import NamedSession


def draw_labels(pattern, openings):
    labels = []
    for i, opening in enumerate(openings):
        points = pattern.mesh.vertices_attributes("xyz", keys=opening)
        centroid = centroid_points(points)
        labels.append({"pos": centroid, "text": str(i)})
    return compas_rhino.drawing.draw_labels(labels, layer="Pattern", clear=False, redraw=True)


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    pattern: RhinoPatternObject = scene.find_by_itemtype(itemtype=Pattern)
    if not pattern:
        return

    # =============================================================================
    # Init openings
    # =============================================================================

    rs.UnselectAllObjects()

    openings = pattern.mesh.split_boundary()
    guids = draw_labels(pattern, openings)

    targets = []
    for opening in openings:
        sag = pattern.mesh.compute_sag(opening)
        sag = max(sag, 0.05)
        targets.append(sag)

    pattern.mesh.relax()

    count = 0
    while count < 10:
        count += 1
        current = [pattern.mesh.compute_sag(opening) for opening in openings]

        if all((sag - target) ** 2 < 0.01 for sag, target in zip(current, targets)):
            break

        for sag, target, opening in zip(current, targets, openings):
            scale = sag / target
            for u, v in pairwise(opening):
                q = pattern.mesh.edge_attribute((u, v), name="q")
                pattern.mesh.edge_attribute((u, v), name="q", value=scale * q)

        pattern.mesh.relax()

    rs.EnableRedraw(False)
    compas_rhino.objects.delete_objects(guids, purge=True)
    pattern.clear()
    pattern.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Update openings
    # =============================================================================

    rs.UnselectAllObjects()

    guids = draw_labels(pattern, openings)

    options1 = ["All"] + [f"Boundary_{index}" for index in range(len(openings))]
    options2 = [f"Sag_{i * 5}" for i in range(1, 11)]

    while True:
        option1 = rs.GetString("Select boundary", strings=options1)
        if not option1:
            break

        N = list(range(len(openings))) if option1 == "All" else [int(option1.split("_")[-1])]

        while True:
            option2 = rs.GetString("Select sag percentage", strings=options2)
            if not option2:
                break

            for n in N:
                targets[n] = float(option2.split("_")[-1]) / 100

                count = 0
                while count < 10:
                    count += 1
                    current = [pattern.mesh.compute_sag(opening) for opening in openings]

                    if all((sag - target) ** 2 < 0.001 for sag, target in zip(current, targets)):
                        break

                    for sag, target, opening in zip(current, targets, openings):
                        scale = sag / target
                        for edge in pairwise(opening):
                            q = pattern.mesh.edge_attribute(edge, name="q")
                            pattern.mesh.edge_attribute(edge, name="q", value=scale * q)

                    pattern.mesh.relax()

            rs.EnableRedraw(False)
            compas_rhino.objects.delete_objects(guids, purge=True)
            pattern.clear()
            pattern.draw()
            guids = draw_labels(pattern, openings)
            rs.EnableRedraw(True)
            rs.Redraw()

    compas_rhino.objects.delete_objects(guids, purge=True)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_supports = True
    pattern.show_fixed = True
    pattern.show_free = False
    pattern.show_edges = False

    rs.EnableRedraw(False)
    pattern.clear()
    pattern.draw()
    rs.EnableRedraw(True)
    rs.Redraw()

    # =============================================================================
    # Save session
    # =============================================================================

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(name="Update Pattern Boundaries")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
