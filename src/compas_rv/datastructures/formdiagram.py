from compas_tna.diagrams import FormDiagram

from .diagram import Diagram
from .pattern import Pattern


class FormDiagram(Diagram, FormDiagram):
    """
    Data structure for form diagrams.
    """

    @classmethod
    def from_pattern(cls, pattern: Pattern) -> "FormDiagram":
        """Construct a form diagram from a pattern.

        Parameters
        ----------
        pattern : Pattern
            The pattern from which the diagram should be constructed.
        feet : {1, 2}, optional
            The number of horizontal force directions that should be added to the supports.

        Returns
        -------
        FormDiagram
            The form diagram.
        """
        form: FormDiagram = pattern.copy(cls=cls)
        form.update_boundaries()
        return form

    # because it might clash with the parent function
    def edges_on_boundaries(self):
        boundaries = []
        for face in self.faces_where(_is_loaded=False):
            boundary = []
            for edge in self.face_halfedges(face):
                if self.edge_attribute(edge, name="_is_edge"):
                    boundary.append(edge)
            boundaries.append(boundary)
        return boundaries
