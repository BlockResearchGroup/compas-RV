# \*Funnel Shell



## Rhino Geometry

Download Rhino3D File:

{% file src="broken-reference" %}

## Create Pattern

|                                                                                  |                                                                          |                                                                                                                  |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_pattern (2).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_pattern</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern.py"><code>RV_pattern.py</code></a></p> |

**Command:** `RV_pattern` > `RhinoMesh` > `Select a mesh`

<figure><img src="broken-reference" alt=""><figcaption><p>The display of the Mesh input changes when the <code>RV_pattern</code> command is initiated.</p></figcaption></figure>



## Identify Supports

<table><thead><tr><th></th><th width="228"></th><th></th></tr></thead><tbody><tr><td> <img src="../../.gitbook/assets/RV_supports (2).svg" alt=""></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p></td><td><p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p></td></tr></tbody></table>

**Command:** `RV_pattern_supports` > `Add`> `Manual`> `Select Vertices`> `Enter`

<figure><img src="broken-reference" alt=""><figcaption><p>Select the strips of vertices on the two opposite sides of the Mesh.</p></figcaption></figure>



## Form Diagram

|                                                                                      |                                                                       |                                                                                                            |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_FormDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_form</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_form.py"><code>RV_form.py</code></a></p> |

**Command:** `RV_form`\


<figure><img src="broken-reference" alt=""><figcaption><p>The mesh geometry is converted to a line preview.</p></figcaption></figure>

## Force Diagram

|                                                                                       |                                                                        |                                                                                                              |
| ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_ForceDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_force</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_force.py"><code>RV_force.py</code></a></p> |

**Command:** `RV_force`

<figure><img src="broken-reference" alt=""><figcaption><p>On the right side, the force diagram is created with TextDots marking the angle deviation between the form edge and its 90-degree rotated force edge. The next step, horizontal equilibrium, will aim to reduce this deviation to zero.</p></figcaption></figure>

## Horizontal Equilibrium

|                                                                                        |                                                                                 |                                                                                                                                |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_horizontal-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_horizontal</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_horizontal.py"><code>RV_tna_horizontal.py</code></a></p> |

**Command:** `RV_tna_horizontal` > `Iterations` > `1000`

<figure><img src="broken-reference" alt=""><figcaption><p>The horizontal equilibrium minimizes the angles as much as possible, aiming to bring them close to zero.</p></figcaption></figure>

## Vertical Equilibrium

|                                                                                      |                                                                               |                                                                                                                            |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_vertical-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_vertical</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_vertical.py"><code>RV_tna_vertical.py</code></a></p> |

**Command:** `RV_tna_vertical`&#x20;

<figure><img src="broken-reference" alt=""><figcaption><p>Vertical projection to get 3D geometry.</p></figcaption></figure>

## Modify Vertical Thrust

|                                                                                           |                                                                                |                                                                                                                              |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_ThrustDiagram-modify.svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_thrust_modify</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_thrust_modify.py"><code>RV_thrust_modify.py</code></a></p> |

`RV_thrust_modify > VertexAttributes > Manual > Select Boundary Vertices > Enter > z=3`

<figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

## Vertical Equilibrium

|                                                                                      |                                                                               |                                                                                                                            |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_vertical-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_vertical</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_vertical.py"><code>RV_tna_vertical.py</code></a></p> |

**Command:** `RV_tna_vertical`&#x20;

<figure><img src="broken-reference" alt=""><figcaption><p>Vertical projection to get 3D geometry. In RV_Settings > Drawing > set show_forces and show_pipes to True.</p></figcaption></figure>

