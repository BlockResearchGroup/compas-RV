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
        self.data.clear()

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

    def find_envelope(self, warn=True):
        from compas_tna.envelope import Envelope

        envelopeobject = self.scene.find_by_itemtype(Envelope)
        if envelopeobject:
            return envelopeobject

        # Migrate sessions created before envelopes became scene objects.
        envelope = self.get("envelope")
        if envelope:
            return self.add_envelope(envelope, remove_legacy=True)

        if warn:
            rs.MessageBox("There is no Envelope.", title="Warning")

    def add_envelope(self, envelope, remove_legacy=False):
        """Add an envelope to the scene using the current drawing settings."""
        from compas.datastructures import Mesh

        meshes = [envelope.intrados, envelope.middle, envelope.extrados, getattr(envelope, "fill", None)]
        mesh_guids = {str(mesh.guid) for mesh in meshes if mesh is not None}
        component_names = {"Intrados", "Middle", "Extrados", "Fill"}
        for sceneobject in list(self.scene.objects):
            item = sceneobject.item
            is_legacy_component = remove_legacy and isinstance(item, Mesh) and sceneobject.name in component_names
            if item is not None and (str(item.guid) in mesh_guids or is_legacy_component):
                sceneobject.clear()
                self.scene.remove(sceneobject)

        if "envelope" in self:
            del self.data["envelope"]

        return self.scene.add(
            envelope,
            name="Envelope",
            layer="RhinoVAULT::Envelope",
        )

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

    def clear_envelope(self, redraw=True):
        formobject = self.find_formdiagram(warn=False)
        if formobject:
            formobject.diagram.attributes["loads_from_envelope"] = False

        envelopeobject = self.find_envelope(warn=False)
        if not envelopeobject:
            return

        envelopeobject.clear()
        self.scene.remove(envelopeobject)

        if redraw:
            self.scene.redraw()
            rs.Redraw()

    def confirm(self, message):
        result = rs.MessageBox(message, buttons=4 | 32 | 256 | 0, title="Confirmation")
        return result == 6

    def warn(self, message):
        return rs.MessageBox(message, title="Warning")
