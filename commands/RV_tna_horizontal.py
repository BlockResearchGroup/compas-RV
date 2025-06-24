#! python3
# venv: brg-csd
# r: compas_rv>=0.9.2, tessagon


import rhinoscriptsyntax as rs  # type: ignore  # type: ignore

from compas_rv.conduits import HorizontalConduit
from compas_rv.session import RVSession
from compas_tna.equilibrium import horizontal_nodal


def RunCommand():
    def redraw(k, xy, edges):
        if k % conduit.refreshrate:
            return
        print(k)
        conduit.lines = [[[xy[i][1], -xy[i][0]], [xy[j][1], -xy[j][0]]] for i, j in edges]
        conduit.redraw()

    # =============================================================================
    # Check scene
    # =============================================================================

    session = RVSession()

    form = session.find_formdiagram()
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    force = session.find_forcediagram()
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    # =============================================================================
    # Options prompt
    # =============================================================================

    kmax = session.settings.tna.horizontal_kmax
    alpha = session.settings.tna.horizontal_alpha
    refresh = session.settings.tna.horizontal_refreshrate

    options = ["Alpha", "Iterations", "RefreshRate"]

    while True:
        option = rs.GetString("Press Enter to run or ESC to exit.", strings=options)

        if option is None:
            print("Horizontal equilibrium aborted!")
            return

        if not option:
            break

        if option == "Alpha":
            alpha_options = ["form{}".format(int(i * 10)) for i in range(11)]
            alpha_default = 0
            for i in range(11):
                if alpha == i * 10:
                    alpha_default = i
                    break
            temp = rs.GetString("Select parallelisation weight", alpha_options[alpha_default], alpha_options)
            if not temp:
                alpha = 100
            else:
                alpha = int(temp[4:])

        elif option == "Iterations":
            new_kmax = rs.GetInteger("Enter number of iterations", kmax, 1, 10000)
            if new_kmax or new_kmax is not None:
                kmax = new_kmax

        elif option == "RefreshRate":
            new_refresh = rs.GetInteger("Refresh rate for dynamic visualisation", refresh, 0, 1000)
            if new_refresh or new_refresh is not None:
                refresh = new_refresh

    if refresh > kmax:
        refresh = 0

    session.settings.tna.horizontal_kmax = kmax
    session.settings.tna.horizontal_alpha = alpha
    session.settings.tna.horizontal_refreshrate = refresh

    # =============================================================================
    # Compute horizontal
    # =============================================================================

    # if alpha == 100:
    #     update_force_from_form(force.diagram, form.diagram)

    if refresh > 0:
        # overlapping conduits and dots look messy
        form.clear_angles()
        force.clear_angles()

        conduit = HorizontalConduit([], refreshrate=refresh)
        with conduit.enabled():
            horizontal_nodal(form.diagram, force.diagram, kmax=kmax, alpha=alpha, callback=redraw)
    else:
        horizontal_nodal(form.diagram, force.diagram, kmax=kmax, alpha=alpha)

    force.diagram.update_position()

    # =============================================================================
    # Update scene
    # =============================================================================

    max_angle = max(form.diagram.edges_attribute("_a"))
    tol_angles = session.settings.tna.horizontal_max_angle

    if max_angle < tol_angles:
        print("Horizontal equilibrium found!")
        print(f"Maximum angle deviation: {max_angle} < {tol_angles}")

    else:
        print("Horizontal equilibrium NOT found! Consider running more iterations.")
        print(f"Maximum angle deviation: {max_angle} > {tol_angles}")

    rs.UnselectAllObjects()

    session.scene.redraw()
    rs.Redraw()

    if session.settings.autosave:
        session.record(name="TNA Horizontal")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
