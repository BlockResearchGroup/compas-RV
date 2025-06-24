#! python3
# venv: brg-csd
# r: compas_rv>=0.9.2, tessagon

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

    options = ["RhinoVault", "ThrustNetworkAnalysis", "Drawing"]

    while True:
        option = rs.GetString(message="Choose a settings section, or escape/cancel to exit.", strings=options)
        if not option:
            break

        if option == "RhinoVault":
            update_settings(session.settings, title=option)

        elif option == "ThrustNetworkAnalysis":
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
