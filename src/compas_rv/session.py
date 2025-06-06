import rhinoscriptsyntax as rs  # type: ignore

from compas.scene import Scene
from compas_rhino.scene import RhinoSceneObject
from compas_rv.settings import RVSettings
from compas_session.session import Session


def find_all_by_itemtype(scene: Scene, itemtype) -> list[RhinoSceneObject]:
    sceneobjects = []
    for obj in scene.objects:
        if isinstance(obj.item, itemtype):
            sceneobjects.append(obj)
    return sceneobjects


class RVSession(Session):
    settings: RVSettings  # type: ignore

    def __new__(cls, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        return super().__new__(cls, name="RhinoVAULT")

    def __init__(self, **kwargs):
        if "name" in kwargs:
            del kwargs["name"]
        super().__init__(name="RhinoVAULT", settings=RVSettings(), **kwargs)

    def clear(self, clear_scene=True, clear_context=True):
        for sceneobject in self.scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()  # type: ignore
        self.scene.clear(clear_scene=clear_scene, clear_context=clear_context)

    def clear_conduits(self):
        for sceneobject in self.scene.objects:
            if hasattr(sceneobject, "clear_conduits"):
                sceneobject.clear_conduits()  # type: ignore

    def find_pattern(self, warn=True):
        from compas_rv.datastructures import Pattern
        from compas_rv.scene import RhinoPatternObject

        form: RhinoPatternObject = self.scene.find_by_itemtype(Pattern)  # type: ignore
        if form:
            return form
        if warn:
            rs.MessageBox("There is no Pattern.", title="Warning")

    def find_formdiagram(self, warn=True):
        from compas_rv.datastructures import FormDiagram
        from compas_rv.scene import RhinoFormObject

        form: RhinoFormObject = self.scene.find_by_itemtype(FormDiagram)  # type: ignore
        if form:
            return form
        if warn:
            rs.MessageBox("There is no FormDiagram.", title="Warning")

    def find_forcediagram(self, warn=True):
        from compas_rv.datastructures import ForceDiagram
        from compas_rv.scene import RhinoForceObject

        force: RhinoForceObject = self.scene.find_by_itemtype(ForceDiagram)  # type: ignore
        if force:
            return force
        if warn:
            rs.MessageBox("There is no ForceDiagram.", title="Warning")

    def find_thrustdiagram(self, warn=True):
        from compas_rv.datastructures import ThrustDiagram
        from compas_rv.scene import RhinoThrustObject

        thrust: RhinoThrustObject = self.scene.find_by_itemtype(ThrustDiagram)  # type: ignore
        if thrust:
            return thrust
        if warn:
            rs.MessageBox("There is no ThrustDiagram.", title="Warning")

    def clear_all_patterns(self, redraw=True):
        from compas_rv.datastructures import Pattern

        for obj in find_all_by_itemtype(self.scene, Pattern):
            obj.clear()
            self.scene.remove(obj)
        if redraw:
            self.scene.redraw()
            rs.Redraw()

    def clear_all_diagrams(self, redraw=True):
        self.clear_all_formdiagrams(redraw=False)
        self.clear_all_forcediagrams(redraw=False)
        self.clear_all_thrustdiagrams(redraw=False)
        if redraw:
            self.scene.redraw()
            rs.Redraw()

    def clear_all_formdiagrams(self, redraw=True):
        from compas_rv.datastructures import FormDiagram

        for obj in find_all_by_itemtype(self.scene, FormDiagram):
            obj.clear()
            self.scene.remove(obj)
        if redraw:
            self.scene.redraw()
            rs.Redraw()

    def clear_all_forcediagrams(self, redraw=True):
        from compas_rv.datastructures import ForceDiagram

        for obj in find_all_by_itemtype(self.scene, ForceDiagram):
            obj.clear()
            self.scene.remove(obj)
        if redraw:
            self.scene.redraw()
            rs.Redraw()

    def clear_all_thrustdiagrams(self, redraw=True):
        from compas_rv.datastructures import ThrustDiagram

        for obj in find_all_by_itemtype(self.scene, ThrustDiagram):
            obj.clear()
            self.scene.remove(obj)
        if redraw:
            self.scene.redraw()
            rs.Redraw()

    def confirm(self, message):
        result = rs.MessageBox(message, buttons=4 | 32 | 256 | 0, title="Confirmation")
        return result == 6

    def warn(self, message):
        return rs.MessageBox(message, title="Warning")
