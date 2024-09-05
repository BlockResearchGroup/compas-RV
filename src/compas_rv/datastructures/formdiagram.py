from compas_tna.diagrams import FormDiagram

from .diagram import Diagram
from .pattern import Pattern  # noqa: F401


class FormDiagram(Diagram, FormDiagram):
    """
    Data structure for form diagrams.
    """

    @classmethod
    def from_pattern(cls, pattern):
        # type: (Pattern) -> FormDiagram
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
