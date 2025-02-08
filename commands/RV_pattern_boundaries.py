#! python3
# venv: brg-csd
# r: compas_rv>=0.8.1


import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.drawing
import compas_rhino.objects
from compas.geometry import centroid_points
from compas_rv.session import RVSession


def draw_labels(pattern, openings):
    labels = []
    for i, opening in enumerate(openings):
        points = pattern.mesh.vertices_attributes("xyz", keys=opening)
        centroid = centroid_points(points)
        labels.append({"pos": centroid, "text": str(i)})
    return compas_rhino.drawing.draw_labels(labels, layer="Pattern", clear=False, redraw=True)


# NOTE: this could be replaced by an interactive solver
# like the one used for interactive scaling in FormFinder


def RunCommand():
    session = RVSession()

    form = session.find_formdiagram(warn=False)
    force = session.find_forcediagram(warn=False)

    if form or force:
        return session.warn("Please remove all form and force diagrams before using pattern commands.")

    pattern = session.find_pattern()
    if not pattern:
        return

    # =============================================================================
    # Init openings
    # =============================================================================

    rs.UnselectAllObjects()

    openings, targets = pattern.mesh.init_openings(minsag=0.1)
    pattern.redraw()

    # =============================================================================
    # Update openings
    # =============================================================================

    rs.UnselectAllObjects()

    guids = draw_labels(pattern, openings)

    options1 = ["All"] + [f"Boundary_{index}" for index in range(len(openings))]
    options2 = [f"Sag_{i * 10}" for i in range(1, 5)]

    while True:
        option1 = rs.GetString("Select boundary", strings=options1)
        if not option1:
            break

        N = list(range(len(openings))) if option1 == "All" else [int(option1.split("_")[-1])]

        while True:
            option2 = rs.GetString("Select sag percentage", strings=options2)
            if not option2:
                break

            target = float(option2.split("_")[-1]) / 100

            for n in N:
                targets[n] = target

            pattern.mesh.match_opening_sag_targets(openings, targets)

            compas_rhino.objects.delete_objects(guids, purge=True)
            pattern.redraw()
            guids = draw_labels(pattern, openings)
            rs.Redraw()

    compas_rhino.objects.delete_objects(guids, purge=True)

    # =============================================================================
    # Update scene
    # =============================================================================

    rs.UnselectAllObjects()

    pattern.show_vertices = list(set(list(pattern.mesh.vertices_where(is_support=True)) + list(pattern.mesh.vertices_where(is_fixed=True))))
    pattern.show_edges = False
    pattern.show_faces = True

    pattern.redraw()

    if session.settings.autosave:
        session.record(name="Update Pattern Boundaries")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
