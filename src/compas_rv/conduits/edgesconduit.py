from typing import Annotated
from typing import List
from typing import Tuple

import Rhino  # type: ignore
import System  # type: ignore

from compas.colors import Color
from compas_rhino.conduits import BaseConduit


class EdgesConduit(BaseConduit):
    """Display conduit for CableMesh edges as lines.

    Parameters
    ----------
    xyz : list of list of float
        The vertex coordinates.
    edges : list of tuple of int
        List of pairs of indices into the list of vertex coordinates.

    """

    xyz: List[Annotated[List[float], 3]]
    edges: List[Tuple[int, int]]
    thickness: int

    def __init__(self, xyz, edges, thickness=1, color=None, **kwargs):
        super().__init__(**kwargs)
        self.xyz = xyz
        self.edges = edges
        self.thickness = thickness
        self.color = color or Color(0, 0, 0)

    def PostDrawObjects(self, e):
        color = System.Drawing.Color.FromArgb(*self.color.rgb255)
        lines = []
        for i, j in self.edges:
            sp = self.xyz[i]
            ep = self.xyz[j]
            lines.append(
                Rhino.Geometry.Line(
                    Rhino.Geometry.Point3d(*sp),
                    Rhino.Geometry.Point3d(*ep),
                )
            )

        if lines:
            e.Display.DrawLines(lines, color, self.thickness)
