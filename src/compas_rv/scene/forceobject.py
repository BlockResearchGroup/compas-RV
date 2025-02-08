from compas.colors import Color
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_rv.datastructures import ForceDiagram
from compas_rv.datastructures import FormDiagram
from compas_rv.session import RVSession

from .diagramobject import RhinoDiagramObject


class RhinoForceObject(RhinoDiagramObject):
    session = RVSession()
    diagram: ForceDiagram

    vertexcolor = ColorDictAttribute(default=Color.blue())
    edgecolor = ColorDictAttribute(default=Color.blue().darkened(50))
    facecolor = ColorDictAttribute(default=Color.blue().lightened(25))

    def __init__(
        self,
        vertexgroup="RV::ForceDiagram::Vertices",
        edgegroup="RV::ForceDiagram::Edges",
        facegroup="RV::ForceDiagram::Faces",
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

    def forces(self):
        primal: FormDiagram = self.diagram.primal
        edges = [self.diagram.primal_edge(edge) for edge in self.edges()]
        return primal.edges_attribute("_f", keys=edges)

    # =============================================================================
    # Clear
    # =============================================================================

    # =============================================================================
    # Draw
    # =============================================================================

    # =============================================================================
    # Redraw
    # =============================================================================
