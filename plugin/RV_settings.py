#! python3

import compas_rv.settings
from compas_rui.forms import SettingsForm
from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")

    form = SettingsForm(settings=compas_rv.settings.SETTINGS, use_tab=True)
    if form.show():
        print(form.settings)

    if compas_rv.settings.SETTINGS["Session"]["autosave.events"]:
        session.record(eventname="Update Settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
