from compas_rui.values import BoolValue
from compas_rui.values import FloatValue
from compas_rui.values import IntValue
from compas_rui.values import Settings

SETTINGS = {
    "Session": Settings(
        {
            "autosave.events": BoolValue(True),
        }
    ),
    "RhinoVAULT": Settings(
        {
            "show.forces": BoolValue(False),
            "show.angles": BoolValue(True),
            "tol.angles": FloatValue(5.0),
        }
    ),
    "TNA": Settings(
        {
            "vertical.kmax": IntValue(300),
            "vertical.zmax": FloatValue(4.0),
            "horizontal.kmax": IntValue(100),
            "horizontal.alpha": IntValue(100),
            "horizontal.refreshrate": IntValue(10),
        }
    ),
}
