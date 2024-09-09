#! python3

import compas_rv.settings
from compas_rui.forms import SettingsForm
from compas_rv.datastructures import ForceDiagram
from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import ThrustDiagram
from compas_rv.scene import RhinoForceObject
from compas_rv.scene import RhinoFormObject
from compas_rv.scene import RhinoThrustObject
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")
    scene = session.scene()

    form: RhinoFormObject = scene.find_by_itemtype(itemtype=FormDiagram)
    force: RhinoForceObject = scene.find_by_itemtype(itemtype=ForceDiagram)
    thrust: RhinoThrustObject = scene.find_by_itemtype(itemtype=ThrustDiagram)

    if form:
        if "FormDiagram" in compas_rv.settings.SETTINGS:
            for key, value in compas_rv.settings.SETTINGS["FormDiagram"].items():
                name = "_".join(key.split("."))
                if hasattr(form, name):
                    value.set(getattr(form, name))

    if force:
        if "ForceDiagram" in compas_rv.settings.SETTINGS:
            for key, value in compas_rv.settings.SETTINGS["ForceDiagram"].items():
                name = "_".join(key.split("."))
                if hasattr(force, name):
                    value.set(getattr(force, name))

    if thrust:
        if "ThrustDiagram" in compas_rv.settings.SETTINGS:
            for key, value in compas_rv.settings.SETTINGS["ThrustDiagram"].items():
                name = "_".join(key.split("."))
                if hasattr(thrust, name):
                    value.set(getattr(thrust, name))

    settingsform = SettingsForm(settings=compas_rv.settings.SETTINGS, use_tab=True)
    if settingsform.show():

        if form:
            if "FormDiagram" in compas_rv.settings.SETTINGS:
                for key, value in compas_rv.settings.SETTINGS["FormDiagram"].items():
                    name = "_".join(key.split("."))
                    setattr(form, name, value.value)

        if force:
            if "ForceDiagram" in compas_rv.settings.SETTINGS:
                for key, value in compas_rv.settings.SETTINGS["ForceDiagram"].items():
                    name = "_".join(key.split("."))
                    setattr(force, name, value.value)

        if thrust:
            if "ThrustDiagram" in compas_rv.settings.SETTINGS:
                for key, value in compas_rv.settings.SETTINGS["ThrustDiagram"].items():
                    name = "_".join(key.split("."))
                    setattr(thrust, name, value.value)

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="Update Settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
