#! python3

import compas_rv
from compas_rui.forms import AboutForm


def RunCommand(is_interactive):

    form = AboutForm(
        title=compas_rv.title,
        description=compas_rv.description,
        version=compas_rv.__version__,
        website=compas_rv.website,
        copyright=compas_rv.__copyright__,
        license=compas_rv.__license__,
    )

    form.show()


# =============================================================================
# Run as main
# =============================================================================

if __name__ == "__main__":
    RunCommand(True)
