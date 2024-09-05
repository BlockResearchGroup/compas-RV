#! python3

import ast

import rhinoscriptsyntax as rs  # type: ignore

from compas_session.namedsession import NamedSession


def RunCommand(is_interactive):

    session = NamedSession(name="RhinoVAULT")

    names = sorted(list(session.CONFIG.keys()))
    values = [session.CONFIG[name] for name in names]

    values = rs.PropertyListBox(names, values, message="Update Config", title="FormFinder")

    if values:
        for name, value in zip(names, values):
            try:
                session.CONFIG[name] = ast.literal_eval(value)
            except (ValueError, TypeError):
                session.CONFIG[name] = value

    if session.CONFIG["autosave.events"]:
        session.record(eventname="Update Settings")


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
