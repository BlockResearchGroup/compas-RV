#! python3
# venv: rhinovault
# r: compas>=2.5, compas_rui>=0.3.1, compas_session>=0.4.1, compas_tna>=0.5

import rhinoscriptsyntax as rs  # type: ignore
from pydantic import BaseModel

from compas_rui.forms import NamedValuesForm
from compas_rv.session import RVSession

# Switch to using ModelFieldsForm


def update_settings(model, title):
    names = []
    values = []
    for name, info in model.model_fields.items():
        if issubclass(info.annotation, BaseModel):
            continue
        names.append(name)
        values.append(getattr(model, name))
    form = NamedValuesForm(names, values, title=title)
    if form.show():
        for name, value in form.attributes.items():
            setattr(model, name, value)


# =============================================================================
# Command
# =============================================================================


def RunCommand():
    session = RVSession()

    options = ["RhinoVAULT", "TNA", "Drawing"]
    option = rs.GetString(message="Settings Section", strings=options)
    if not option:
        return

    if option == "RhinoVAULT":
        update_settings(session.settings, title=option)

    elif option == "TNA":
        update_settings(session.settings.tna, title=option)

    elif option == "Drawing":
        update_settings(session.settings.drawing, title=option)

    session.scene.redraw()

    if session.settings.autosave:
        session.record(name="Update settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand()
