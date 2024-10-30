from pydantic import BaseModel

from compas_session.settings import Settings


class HorizontalSettings(BaseModel):
    kmax: int = 100
    alpha: float = 100


class VerticalSettings(BaseModel):
    kmax: int = 300
    zmax: float = 4.0


class TNASettings(BaseModel):
    horizontal: HorizontalSettings = HorizontalSettings()
    vertical: VerticalSettings = VerticalSettings()


class FormDrawingSettings(BaseModel):
    show_angles: bool = False


class ForceDrawingSettings(BaseModel):
    show_angles: bool = False


class ThrustDrawingSettings(BaseModel):
    show_reactions: bool = True
    show_residuals: bool = False
    show_forces: bool = False
    show_loads: bool = False
    show_selfweight: bool = False

    scale_reactions: float = 1.0
    scale_residuals: float = 1.0
    scale_forces: float = 1.0
    scale_loads: float = 1.0
    scale_selfweight: float = 1.0

    tol_vectors: float = 1e-3
    tol_pipes: float = 1e-2


class DrawingSettings(BaseModel):
    form: FormDrawingSettings = FormDrawingSettings()
    force: ForceDrawingSettings = ForceDrawingSettings()
    thrust: ThrustDrawingSettings = ThrustDrawingSettings()


class RVSettings(Settings):
    tna: TNASettings = TNASettings()
    drawing: DrawingSettings = DrawingSettings()
