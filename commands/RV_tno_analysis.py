#! python3
# venv: brg-csd
# r: compas_rv>=0.10.1

import numpy as np
import rhinoscriptsyntax as rs  # type: ignore
from compas_tno.analysis import Analysis

from compas_rui.forms import NamedValuesForm
from compas_rv.conventions import invert_formdiagram_signs
from compas_rv.session import RVSession
from compas_rv.solvers import update_force_from_form
from compas_tna.envelope import MeshEnvelope
from compas_tna.envelope import ParametricEnvelope

OBJECTIVES = [
    "MinimumThrust",
    "MaximumThrust",
    "MinimumThickness",
    "Bestfit",
    "MaximumLoad",
    "SupportDisplacement",
]


def get_optimisation_options(objective, envelope):
    constraint_options = [
        ("Funicular", True),
        ("Envelope", objective != "Bestfit"),
    ]
    if isinstance(envelope, ParametricEnvelope):
        constraint_options.append(("ReactionDirections", False))
    constraint_options = rs.CheckListBox(constraint_options, "Validate the constraints of the optimisation.", "TNO Constraints")
    if constraint_options is None:
        return

    variable_options = []
    if objective == "MinimumThickness":
        variable_options.append(("Thickness", True))
    variable_options.extend(
        [
            ("ForceDensities", True),
            ("SupportHeights", True),
        ]
    )
    if objective == "MaximumLoad":
        variable_options.append(("LoadMultiplier", True))
    variable_options = rs.CheckListBox(variable_options, "Validate the variables of the optimisation.", "TNO Variables")
    if variable_options is None:
        return

    constraint_names = {
        "Funicular": "funicular",
        "Envelope": "envelope",
        "ReactionDirections": "reac_bounds",
    }
    variable_names = {
        "Thickness": "t",
        "ForceDensities": "q",
        "SupportHeights": "zb",
        "LoadMultiplier": "lambdv",
    }

    constraints = [constraint_names[name] for name, checked in constraint_options if checked]
    variables = [variable_names[name] for name, checked in variable_options if checked]

    return constraints, variables


def get_load_direction(formobject):
    n = formobject.diagram.number_of_vertices()
    load_direction = np.zeros((n, 1))
    index_vertex = formobject.diagram.index_vertex()
    candidates = list(formobject.diagram.vertices_where(is_support=False))
    assigned = False

    while True:
        vertices = formobject.select_thrust_vertices(
            vertices=candidates,
            message="Select vertices for maximum applied load",
            use_edges=False,
        )
        if not vertices:
            break

        force = rs.GetReal("Initial vertical load p0 (negative downward)", -10.0)
        if force is None:
            return

        for vertex in vertices:
            load_direction[index_vertex[vertex]] = force
        assigned = True

        rs.UnselectAllObjects()
        more = rs.GetString("Apply initial loads on additional vertices", "No", ["No", "Yes"])
        if more != "Yes":
            break

    if not assigned:
        formobject.session.warn("Select at least one vertex and assign an initial load.")
        return

    return load_direction


def get_displacement_vector(defaults):
    form = NamedValuesForm(["Ux", "Uy", "Uz"], defaults, title="Support Displacement", width=350, height=180)
    if not form.show():
        return

    try:
        return [float(form.attributes[name]) for name in ("Ux", "Uy", "Uz")]
    except (TypeError, ValueError):
        rs.MessageBox("Ux, Uy and Uz must be numbers.", title="Invalid Support Displacement")


DISPLACEMENT_DIRECTIONS = ["Outward", "Inward", "Downward", "Manual"]


def get_displacement_values(formobject, vertices, manual_defaults, magnitude_default):
    """Prompt for the displacement to apply to a batch of selected supports.

    Returns
    -------
    tuple[dict[int, list[float]], list[float], float] or None
        A mapping from vertex to ``[ux, uy, uz]``, together with the updated
        manual-entry and magnitude defaults to reuse for the next prompt, or
        None if the user cancelled.
    """
    direction = rs.GetString("Support displacement direction", "Manual", DISPLACEMENT_DIRECTIONS)
    if not direction:
        return None

    if direction == "Manual":
        values = get_displacement_vector(manual_defaults)
        if values is None:
            return None
        return {vertex: values for vertex in vertices}, values, magnitude_default

    magnitude = rs.GetReal("{0} displacement magnitude".format(direction), magnitude_default, minimum=0.0)
    if magnitude is None:
        return None

    if direction == "Downward":
        vectors = {vertex: [0.0, 0.0, -magnitude] for vertex in vertices}
    else:
        outward = formobject.diagram.find_outward_displacement(vertices)
        sign = -1.0 if direction == "Inward" else 1.0
        vectors = {vertex: [sign * magnitude * ux, sign * magnitude * uy, 0.0] for vertex, (ux, uy, _) in outward.items()}

    return vectors, manual_defaults, magnitude


def get_support_displacement(formobject):
    supports = list(formobject.diagram.supports())
    displacement = np.zeros((len(supports), 3))
    assignments = {}
    manual_defaults = [-1.0, -1.0, 0.0]
    magnitude_default = 1.0

    while True:
        vertices = formobject.select_thrust_vertices(
            vertices=supports,
            message="Select supports for displacement",
            use_edges=False,
        )
        if not vertices:
            break

        result = get_displacement_values(formobject, vertices, manual_defaults, magnitude_default)
        if result is None:
            return
        vectors, manual_defaults, magnitude_default = result

        for vertex in vertices:
            values = vectors[vertex]
            displacement[supports.index(vertex)] = np.array(values)
            assignments[vertex] = values
            print("Applied displacement {0} to support {1}".format(values, vertex))

        rs.UnselectAllObjects()
        more = rs.GetString("Define additional displacement vectors", "No", ["No", "Yes"])
        if more != "Yes":
            break

    if not assignments:
        formobject.session.warn("Select at least one support and assign a displacement vector.")
        return

    for support in supports:
        formobject.diagram.vertex_attributes(support, ["ux", "uy", "uz"], assignments.get(support, [0.0, 0.0, 0.0]))

    return displacement


def create_analysis(objective, formobject, envelope):
    settings = formobject.session.settings.tno
    formdiagram = formobject.diagram
    kwargs = {
        "printout": settings.printout,
        "max_iter": settings.max_iter,
        "starting_point": settings.starting_point,
        "solver": settings.solver,
    }

    if objective == "MinimumThrust":
        analysis = Analysis.create_minthrust_analysis(formdiagram, envelope, **kwargs)
    elif objective == "MaximumThrust":
        analysis = Analysis.create_maxthrust_analysis(formdiagram, envelope, **kwargs)
    elif objective == "MinimumThickness":
        if isinstance(envelope, MeshEnvelope):
            formobject.session.warn("Minimum thickness analysis is only available for parametric envelopes.")
            return
        analysis = Analysis.create_minthk_analysis(formdiagram, envelope, **kwargs)
    elif objective == "Bestfit":
        analysis = Analysis.create_bestfit_analysis(formdiagram, envelope, **kwargs)
    elif objective == "MaximumLoad":
        load_direction = get_load_direction(formobject)
        if load_direction is None:
            return
        max_lambd = rs.GetReal("Maximum load multiplier", 9999.0, minimum=0.0)
        if max_lambd is None:
            return
        analysis = Analysis.create_max_load_analysis(formdiagram, envelope, load_direction=load_direction, max_lambd=max_lambd, **kwargs)
    elif objective == "SupportDisplacement":
        support_displacement = get_support_displacement(formobject)
        if support_displacement is None:
            return
        analysis = Analysis.create_compl_energy_analysis(formdiagram, envelope, support_displacement=support_displacement, **kwargs)
    else:
        raise NotImplementedError

    return analysis


def report_result(objective, analysis):
    result = analysis.result
    fopt = result.fopt

    if objective in ("MinimumThrust", "MaximumThrust"):
        print("Optimal horizontal thrust calculated: {0:.3f}".format(fopt))
    elif objective == "MinimumThickness":
        print("Minimum thickness calculated: {0:.3f}".format(fopt))
        if result.exitflag == 0:
            analysis.envelope.thickness = fopt
            analysis.envelope.update_envelope()
    elif objective == "MaximumLoad":
        print("Maximum load multiplier calculated: {0:.3f}".format(fopt))
    elif objective == "SupportDisplacement":
        print("Complementary energy to assigned displacements: {0:.3f}".format(fopt))
    elif objective == "Bestfit":
        print("Optimal squared vertical distance to middle surface: {0:.3f}".format(fopt))


def RunCommand():
    session = RVSession()

    formobject = session.find_formdiagram()
    if not formobject:
        return

    envelope = session.find_envelope()
    if not envelope:
        return

    objective = rs.GetString("TNO objective", "MinimumThrust", OBJECTIVES)
    if not objective:
        return

    options = get_optimisation_options(objective, envelope)
    if not options:
        return
    constraints, variables = options

    analysis = create_analysis(objective, formobject, envelope)
    if not analysis:
        return

    analysis.optimiser.set_constraints(constraints)
    analysis.optimiser.set_variables(variables)

    invert_formdiagram_signs(formobject.diagram)
    try:
        # Apply the envelope bounds and use the loads prepared on the FormDiagram.
        envelope.apply_bounds_to_formdiagram(formobject.diagram)
        if "reac_bounds" in constraints:
            analysis.apply_reaction_bounds()

        if abs(sum(formobject.diagram.vertices_attribute("pz"))) < 0.001:
            return session.warn("There are no loads applied to the FormDiagram. Use RV_loads before running TNO analysis.")

        analysis.set_up_optimiser()
        analysis.run()
        session["analysis"] = analysis
    finally:
        invert_formdiagram_signs(formobject.diagram)

    forceobject = None
    if analysis.result.success:
        if objective == "MaximumLoad":
            session.settings.drawing.show_loads = True
        forceobject = session.find_forcediagram(warn=False)
        if forceobject:
            update_force_from_form(forceobject.diagram, formobject.diagram)
            forceobject.diagram.update_position()
            forceobject.diagram.update_angle_deviations()

    report_result(objective, analysis)

    formobject.show_thrust = True

    rs.UnselectAllObjects()
    formobject.redraw()
    if forceobject:
        forceobject.redraw()

    if session.settings.autosave:
        session.record(name="TNO Analysis")


if __name__ == "__main__":
    RunCommand()
