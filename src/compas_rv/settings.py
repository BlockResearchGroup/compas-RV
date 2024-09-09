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
            "tol.angles": FloatValue(5.0),
        }
    ),
    "FormDiagram": Settings(
        {
            "show.angles": BoolValue(True),
        }
    ),
    "ForceDiagram": Settings(
        {
            "show.angles": BoolValue(True),
        }
    ),
    "ThrustDiagram": Settings(
        {
            "show.reactions": BoolValue(True),
            "show.residuals": BoolValue(False),
            "show.forces": BoolValue(False),
            "show.loads": BoolValue(False),
            "show.selfweight": BoolValue(False),
            "scale.loads": FloatValue(1.0),
            "scale.forces": FloatValue(1.0),
            "scale.residuals": FloatValue(1.0),
            "scale.selfweight": FloatValue(1.0),
        }
    ),
    "TNA": Settings(
        {
            "vertical.kmax": IntValue(300),
            "vertical.zmax": FloatValue(4.0),
            "horizontal.kmax": IntValue(100),
            "horizontal.alpha": IntValue(100),
        }
    ),
}
