from compas.colors import Color
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_rv.datastructures import FormDiagram
from compas_rv.session import RVSession

from .diagramobject import RhinoDiagramObject


class RhinoFormObject(RhinoDiagramObject):
    session = RVSession()
    diagram: FormDiagram

    vertexcolor = ColorDictAttribute(default=Color.green())
    edgecolor = ColorDictAttribute(default=Color.green().darkened(50))
    facecolor = ColorDictAttribute(default=Color.green().lightened(25))

    def __init__(
        self,
        vertexgroup="RV::FormDiagram::Vertices",
        edgegroup="RV::FormDiagram::Edges",
        facegroup="RV::FormDiagram::Faces",
        **kwargs,
    ):
        super().__init__(
            vertexgroup=vertexgroup,
            edgegroup=edgegroup,
            facegroup=facegroup,
            **kwargs,
        )

    # =============================================================================
    # Properties
    # =============================================================================

    def edges(self):
        return self.diagram.edges_where(_is_edge=True)

    def faces(self, **kwargs):
        return self.diagram.faces_where(_is_loaded=True)

    # =============================================================================
    # Clear
    # =============================================================================

    # =============================================================================
    # Draw
    # =============================================================================

    # =============================================================================
    # Redraw
    # =============================================================================
