import System  # type: ignore
from Rhino.Geometry import Line  # type: ignore
from Rhino.Geometry import Point3d  # type: ignore
from System.Collections.Generic import List  # type: ignore

from compas_rhino.conduits import BaseConduit

# this needs to be reorganised
# there is not need to update anything since we don't go via RPC anymore
# the data IS live when probably associated with the conduit


class HorizontalConduit(BaseConduit):
    def __init__(self, lines, **kwargs):
        super(HorizontalConduit, self).__init__(**kwargs)
        self._default_thickness = 1.0
        self._default_color = System.Drawing.Color.FromArgb(255, 255, 255)
        self.lines = lines or []

    def DrawForeground(self, e):
        lines = List[Line](len(self.lines))
        for start, end in self.lines:
            lines.Add(Line(Point3d(start[0], start[1], 0), Point3d(end[0], end[1], 0)))
        e.Display.DrawLines(lines, self._default_color, self._default_thickness)
