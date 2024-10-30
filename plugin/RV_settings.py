#! python3
# venv: rhinovault
# r: compas, compas_rui, compas_rv, compas_session, compas_tna

import rhinoscriptsyntax as rs  # type: ignore

from compas_rui.forms import NamedValuesForm
from compas_rv.session import RVSession


def update_settings(model, title):
    names = [name for name, info in model.model_fields.items()]
    values = [getattr(model, name) for name in names]
    form = NamedValuesForm(names, values, title=title)
    if form.show():
        for name, value in form.attributes.items():
            setattr(model, name, value)


def RunCommand():
    session = RVSession()

    options1 = ["TNA", "Drawing"]
    option1 = rs.GetString(message="Settings Section", strings=options1)
    if not option1:
        return

    if option1 == "TNA":
        options2 = ["Horizontal", "Vertical"]
        option2 = rs.GetString(message="Settings Section", strings=options2)
        if not option2:
            return

        title = f"{option1} {option2}"

        if option2 == "Horizontal":
            update_settings(session.settings.tna.horizontal, title=title)

        elif option2 == "Vertical":
            update_settings(session.settings.tna.vertical, title=title)

    elif option1 == "Drawing":
        options2 = ["FormDiagram", "ForceDiagram", "ThrustDiagram"]
        option2 = rs.GetString(message="Settings Section", strings=options2)
        if not option2:
            return

        title = f"{option1} {option2}"

        if option2 == "FormDiagram":
            pass

        elif option2 == "ForceDiagram":
            pass

        elif option2 == "ThrustDiagram":
            update_settings(session.settings.drawing.thrust, title=title)

    session.scene.redraw()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
