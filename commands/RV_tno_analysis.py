#! python3
# venv: brg-csd
# r: compas_rv>=0.9.5

import numpy as np
import rhinoscriptsyntax as rs  # type: ignore

from compas_rv.session import RVSession
from compas_tna.envelope import MeshEnvelope
from compas_tno.analysis import Analysis


OBJECTIVES = [
    "MinimumThrust",
    "MaximumThrust",
    "MinimumThickness",
    "Bestfit",
    "MaximumLoad",
    "SupportDisplacement",
]


def get_load_direction(formobject):
    n = formobject.diagram.number_of_vertices()
    load_direction = np.zeros((n, 1))
    index_vertex = formobject.diagram.index_vertex()

    while True:
        formobject.show_vertices = list(formobject.diagram.vertices())
        formobject.redraw()
        vertices = formobject.select_vertices()
        if not vertices:
            break

        force = rs.GetReal("Load multiplier direction (negative downward)", -10.0)
        if force is None:
            return

        for vertex in vertices:
            load_direction[index_vertex[vertex]] = force

        rs.UnselectAllObjects()
        more = rs.GetString("Apply loads on additional vertices", "No", ["No", "Yes"])
        if more != "Yes":
            break

    return load_direction


def get_support_displacement(formobject):
    supports = list(formobject.diagram.supports())
    displacement = np.zeros((len(supports), 3))

    while True:
        formobject.show_vertices = supports
        formobject.redraw()
        vertices = formobject.select_vertices()
        if not vertices:
            break

        ux = rs.GetReal("Ux", -1.0)
        if ux is None:
            return
        uy = rs.GetReal("Uy", -1.0)
        if uy is None:
            return
        uz = rs.GetReal("Uz", 0.0)
        if uz is None:
            return

        for vertex in vertices:
            displacement[supports.index(vertex)] = np.array([ux, uy, uz])
            print("Applied displacement [{0}, {1}, {2}] to support {3}".format(ux, uy, uz, vertex))

        rs.UnselectAllObjects()
        more = rs.GetString("Define additional displacement vectors", "No", ["No", "Yes"])
        if more != "Yes":
            break

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
        return Analysis.create_minthrust_analysis(formdiagram, envelope, **kwargs)
    if objective == "MaximumThrust":
        return Analysis.create_maxthrust_analysis(formdiagram, envelope, **kwargs)
    if objective == "MinimumThickness":
        if isinstance(envelope, MeshEnvelope):
            formobject.session.warn("Minimum thickness analysis is only available for parametric envelopes.")
            return
        return Analysis.create_minthk_analysis(formdiagram, envelope, **kwargs)
    if objective == "Bestfit":
        return Analysis.create_bestfit_analysis(formdiagram, envelope, **kwargs)
    if objective == "MaximumLoad":
        load_direction = get_load_direction(formobject)
        if load_direction is None:
            return
        return Analysis.create_max_load_analysis(formdiagram, envelope, load_direction=load_direction, max_lambd=settings.max_lambd, **kwargs)
    if objective == "SupportDisplacement":
        support_displacement = get_support_displacement(formobject)
        if support_displacement is None:
            return
        return Analysis.create_compl_energy_analysis(formdiagram, envelope, support_displacement=support_displacement, **kwargs)

    raise NotImplementedError


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

    envelope.apply_bounds_to_formdiagram(formobject.diagram)

    if abs(sum(formobject.diagram.vertices_attribute("pz"))) < 0.001:
        return session.warn("There are no loads applied to the form diagram. Create an envelope or assign loads before running TNO analysis.")

    objective = rs.GetString("TNO objective", session.settings.tno.objective, OBJECTIVES)
    if not objective:
        return
    session.settings.tno.objective = objective

    solver = rs.GetString("Solver", session.settings.tno.solver, ["SLSQP", "IPOPT"])
    if not solver:
        return
    session.settings.tno.solver = solver

    analysis = create_analysis(objective, formobject, envelope)
    if not analysis:
        return

    analysis.set_up_optimiser()
    analysis.run()
    session["analysis"] = analysis

    report_result(objective, analysis)

    formobject.show_thrust = True
    session.settings.drawing.show_reactions = True
    session.settings.drawing.show_pipes = True

    rs.UnselectAllObjects()
    formobject.redraw()

    if session.settings.autosave:
        session.record(name="TNO Analysis")


if __name__ == "__main__":
    RunCommand()
