# 8. Settings

## Settings

|                                                                                |                                                                           |                                                                                                                 |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| <img src="../.gitbook/assets/RV_settings (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_settings</code></p> | <p><strong>source file</strong></p><p><a href="../../plugin/RV_settings.py"><code>RV_settings.py</code></a></p> |

Under `Settings`, global parameters (`RhinoVAULT`, `ThrustNetworkAnalysis`) and visualization (`Drawing`) options can be modified. For each of the categories, various parameters and display settings can be modified. The modifiable parameters for each category are summarized below.

***

## Settings categories

### RhinoVAULT

These are the global parameters for RhinoVAULT.

* **`autosave`** - If set to `True`, session files are saved every time a change has been made in the scene. Set to `True` by default.
* **`autoupdate`**  - If set to `True`, any modifications made in the scene will automatically update the `ThrustDiagram`. Set to `False` by default.

### ThrustNetworkAnalysis

These are the parameters related to [Horizontal equilibrium](horizontal-equilibrium.md) and [Vertical equilibrium](fitting.md) solvers.

* **`horizontal_kmax`** - Number of iterations to be executed by `RV_tna_horizontal` (horizontal equilibrium solver). This number can be reset before the solver is run. This number is set to 100 by default.
* **`horizontal_alpha`** - Percentage value (0.0 to 100.0) that determines how much influence `FormDiagram` has during `RV_tna_horizontal`. For example, an `Alpha` value of 100.0 means that the `FormDiagram` remains fixed and only the `ForceDiagram` will be reconfigures, while an Alpha value of 50 will reconfigure both the `FormDiagram` and `ForceDiagram` with equal weight. This value is set to 100.0 by default.
* **`horizontal_max_angle`** - Tolerance value for displaying angle deviations. If the maximum angle deviation between a pair of corresponding edges in the `FormDiagram` and the `ForceDiagram` is greater than this value, angle deviation will be displayed in the scene with a Rhino dot. This value is set to 5.0 by default.
* **`horizontal_refreshrate`** - Number of iterations to skip during dynamic visualization of `RV_tna_horizontal`. For example, a value of 1 will visualize every iteration step, and therefore take much longer for the final result to be displayed. This value is set to 5 by default.
* **`vertical_kmax`** - Number of iterations to be executed by `RV_tna_vertical` (vertical equilibrium solver).  This number is set to 300 by default.
* **`vertical_zmax`** - Default target height for the `ThrustDiagram`. This value is automatically computed and set by the dimensions of the bounding box of the `FormDiagram` in the scene.

### Drawing

These are the visualization parameters for various RhinoVAULT elements.

* **show\_angles** - This is set to `True` by default.
* **show\_forces** - This is set to `False` by default.
* **show\_reactions** - This is set to `True` by default.
* **show\_residuals** - This is set to `False` by default.
* **show\_pipes** - This is set to `False` by default.
* **show\_loads** - This is set to `False` by default.
* **show\_selfweight** - This is set to `False` by default.
* **show\_thickness** - This is set to `False` by default.
* **scale\_reactions** - This value is set to 0.1 by default.
* **scale\_residuals** - This value is set to 1.0 by default.
* **scale\_pipes** - This is value is set to 0.01 by default.
* **scale\_loads** - This value is set to 1.0 by default.
* **scale\_selfweight** - This value is set to 1.0 by default.
* **tol\_vectors** - This value is set to 0.001 by default.
* **tol\_pipes** - This value is set to 0.01 by default.
