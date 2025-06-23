from pydantic import BaseModel
from pydantic import Field

from compas_session.settings import Settings


class TNASettings(BaseModel):
    horizontal_kmax: int = 100
    horizontal_alpha: float = 100
    horizontal_max_angle: float = Field(default=5.0, title="Maximum Angle Deviation", description="The maximum allowed angle between corresponding edges.")
    horizontal_refreshrate: int = 5

    vertical_kmax: int = 300
    vertical_zmax: float = 4.0


class DrawingSettings(BaseModel):
    show_angles: bool = True
    show_forces: bool = False

    show_reactions: bool = True
    show_residuals: bool = False
    show_pipes: bool = False
    show_loads: bool = False
    show_selfweight: bool = False

    show_thickness: bool = False

    scale_reactions: float = 0.1
    scale_residuals: float = 1.0
    scale_pipes: float = 0.01
    scale_loads: float = 1.0
    scale_selfweight: float = 1.0

    tol_vectors: float = 1e-3
    tol_pipes: float = 1e-2


class RVSettings(Settings):
    autoupdate: bool = False
    autosave: bool = True

    tna: TNASettings = TNASettings()
    drawing: DrawingSettings = DrawingSettings()
