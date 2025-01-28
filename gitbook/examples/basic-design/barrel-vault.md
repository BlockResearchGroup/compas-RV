# Creases



## Rhino Geometry

Download Rhino3D File:

{% file src="../../.gitbook/assets/creases.zip" %}

## Create Pattern

|                                                                                  |                                                                          |                                                                                                                  |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_pattern (2).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_pattern</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern.py"><code>RV_pattern.py</code></a></p> |

**Command:** `RV_pattern` > `RhinoMesh` > `Select a Mesh`

<figure><img src="../../.gitbook/assets/creases_0.png" alt=""><figcaption><p>The display of the Mesh input changes when the <code>RV_pattern</code> command is initiated.</p></figcaption></figure>



## Identify Supports

<table><thead><tr><th></th><th width="228"></th><th></th></tr></thead><tbody><tr><td> <img src="../../.gitbook/assets/RV_supports (2).svg" alt=""></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p></td><td><p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p></td></tr></tbody></table>

**Command:** `RV_pattern_supports` > `Add`> `Manual`> `Select Vertices`> `Enter`

<figure><img src="../../.gitbook/assets/creases_1.png" alt=""><figcaption><p>Select the four corner vertices of the Mesh.</p></figcaption></figure>



## Pattern Relax

<table><thead><tr><th width="221"></th><th width="253"></th><th></th></tr></thead><tbody><tr><td><img src="../../.gitbook/assets/RV_boundaries (1).svg" alt="" data-size="original"></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_boundaries</code></p></td><td><p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_boundaries.py"><code>RV_pattern_boundaries.py</code></a></p></td></tr></tbody></table>

**Command:** `RV_pattern_boundaries > Enter`

<figure><img src="../../.gitbook/assets/creases_3.png" alt=""><figcaption><p>To avoid straight edges, the patter is relax using fd solver, with default value q=1.</p></figcaption></figure>

## Form Diagram

|                                                                                      |                                                                       |                                                                                                            |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_FormDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_form</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_form.py"><code>RV_form.py</code></a></p> |

**Command:** `RV_form`\


<figure><img src="../../.gitbook/assets/creases_4.png" alt=""><figcaption><p>The mesh geometry is converted to a line preview.</p></figcaption></figure>

## Form Diagram

|                                                                                       |                                                                        |                                                                                                              |
| ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_ForceDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_force</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_force.py"><code>RV_force.py</code></a></p> |

**Command:** `RV_force`

<figure><img src="../../.gitbook/assets/creases_5.png" alt=""><figcaption><p>On the right side, the force diagram is created with TextDots marking the angle deviation between the form edge and its 90-degree rotated force edge. The next step, horizontal equilibrium, will aim to reduce this deviation to zero.</p></figcaption></figure>

## Horizontal Equilibrium

|                                                                                        |                                                                                 |                                                                                                                                |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_horizontal-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_horizontal</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_horizontal.py"><code>RV_tna_horizontal.py</code></a></p> |

**Command:** `RV_tna_horizontal` > `Iterations` > `1000`

<figure><img src="../../.gitbook/assets/creases_6.png" alt=""><figcaption><p>The horizontal equilibrium minimizes the angles as much as possible, aiming to bring them close to zero.</p></figcaption></figure>

## Modify Force Diagram

|                                                                                              |                                                                               |                                                                                                                            |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_ForceDiagram-modify (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_force_modify</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_force_modify.py"><code>RV_force_modify.py</code></a></p> |

**Command:** `RV_force_modify`> `Move Vertices` > `Manual > X`\
\
**or**

**Command:** `RV_force_modify`> `EdgeAttributes` > `Manual > Select Lines > lmin=5`

<figure><img src="../../.gitbook/assets/creases_7.png" alt=""><figcaption><p>Select the vertices on the right side and arbitrary move to the left side.</p></figcaption></figure>

## Horizontal Equilibrium

|                                                                                        |                                                                                 |                                                                                                                                |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_horizontal-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_horizontal</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_horizontal.py"><code>RV_tna_horizontal.py</code></a></p> |

**Command:** `RV_tna_horizontal` > `Iterations` > `1000`

<figure><img src="../../.gitbook/assets/creases_9.png" alt=""><figcaption><p>The horizontal equilibrium is recomputed to obtain minimal forces at the corners.</p></figcaption></figure>

## Vertical Equilibrium

|                                                                                      |                                                                               |                                                                                                                            |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_vertical-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_vertical</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_vertical.py"><code>RV_tna_vertical.py</code></a></p> |

**Command:** `RV_tna_vertical`&#x20;

<figure><img src="../../.gitbook/assets/creases_8.png" alt=""><figcaption><p>Vertical projection to get 3D geometry.<br>The pipes as colors can be turned on RV_settings > Drawing > show_pipes and show_forces.</p></figcaption></figure>
