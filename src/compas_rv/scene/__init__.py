from compas.plugins import plugin
from compas.scene.context import register

from compas_rv.datastructures import ForceDiagram
from compas_rv.datastructures import FormDiagram
from compas_rv.datastructures import Pattern
from compas_rv.datastructures import ThrustDiagram

from .forceobject import RhinoForceObject
from .formobject import RhinoFormObject
from .patternobject import RhinoPatternObject
from .thrustobject import RhinoThrustObject


@plugin(category="factories", pluggable_name="register_scene_objects", requires=["Rhino"])
def register_scene_objects_rhino():
    register(Pattern, RhinoPatternObject, context="Rhino")
    register(FormDiagram, RhinoFormObject, context="Rhino")
    register(ThrustDiagram, RhinoThrustObject, context="Rhino")
    register(ForceDiagram, RhinoForceObject, context="Rhino")
