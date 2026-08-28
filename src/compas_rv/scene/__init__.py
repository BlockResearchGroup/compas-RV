from compas.plugins import plugin
from compas.scene.context import register

from compas_rv.datastructures import ForceDiagram, FormDiagram, Pattern

from .forceobject import RhinoForceObject
from .formobject import RhinoFormObject
from .patternobject import RhinoPatternObject


@plugin(category="factories", pluggable_name="register_scene_objects", requires=["Rhino"])
def register_scene_objects_rhino():
    register(Pattern, RhinoPatternObject, context="Rhino")
    register(FormDiagram, RhinoFormObject, context="Rhino")
    register(ForceDiagram, RhinoForceObject, context="Rhino")
