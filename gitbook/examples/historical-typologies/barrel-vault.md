# Barrel Vault

<figure><img src="../../.gitbook/assets/barrel_0.png" alt=""><figcaption></figcaption></figure>

In this tutorial, we will explore the basic features of RhinoVAULT to determine the equilibrium shape of a barrel vault with two boundary supports. To form-find the barrel vault, we will adjust the form diagram parameters for the allowable internal horizontal force limits: [**hmax** ](barrel-vault.md#modify-form-diagram)(upper limit) and [**hmin** ](barrel-vault.md#modify-form-diagram)(lower limit).

A barrel vault is unique because its edges orthogonal to the arches carry almost no load (e.g., **1e-5**), while the edges along the arches share the same internal horizontal force (e.g., **2**). The exception occurs at the boundary, where half of the horizontal force is used (e.g., **1**) for the small tributary area. Due to this special force distribution, the force diagram collapses into a single line.\


1. Pattern
2. Boundary Conditions
3. Form Diagram
4. Modify Form Diagram
5. Force Diagram
6. Horizontal Equilibrium
7. Vertical Equilibrium

For preview, we use `RV_settings > Drawing > show_pipes` and `show_forces` options.

## Rhino Geometry

Download Rhino3D File:

{% file src="../../.gitbook/assets/barrel.3dm" %}

## Create Pattern

|                                                                                  |                                                                          |                                                                                                                  |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_pattern (2).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_pattern</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern.py"><code>RV_pattern.py</code></a></p> |

**Command:** `RV_pattern` > `RhinoLines` > `Select lines`

<figure><img src="../../.gitbook/assets/cross_vault_0.jpg" alt=""><figcaption><p>The display of the Mesh input changes when the <code>RV_pattern</code> command is initiated.</p></figcaption></figure>



## Identify Supports

<table><thead><tr><th></th><th width="228"></th><th></th></tr></thead><tbody><tr><td> <img src="../../.gitbook/assets/RV_supports (2).svg" alt=""></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p></td><td><p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p></td></tr></tbody></table>

**Command:** `RV_pattern_supports` > `Add`> `Manual`> `Select Vertices`> `Enter`

<figure><img src="../../.gitbook/assets/0_creases_2.jpg" alt=""><figcaption><p>Select the strips of vertices on the two opposite sides of the Mesh.</p></figcaption></figure>



## Form Diagram

|                                                                                      |                                                                       |                                                                                                            |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_FormDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_form</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_form.py"><code>RV_form.py</code></a></p> |

**Command:** `RV_form`\


<figure><img src="../../.gitbook/assets/0_creases_3.jpg" alt=""><figcaption><p>The mesh geometry is converted to a line preview.</p></figcaption></figure>

## Modify Form Diagram

|                                                                                             |                                                                              |                                                                                                                          |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_FormDiagram-modify (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_form_modify</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_form_modify.py"><code>RV_form_modify.py</code></a></p> |

**Command:** `RV_form_modify`> `Edge Constraints` > `Manual`\


<figure><img src="../../.gitbook/assets/0_creases_4.jpg" alt=""><figcaption><p>Select the edges, marked in black rectangles, and set the horizontal components (h_min and h_max) to: a) 0.00001, b) 2, and c) 1. This is done because horizontal edges ideally carry no load, and boundary arches have a tributary area twice as large as the outer ones.</p></figcaption></figure>

## Force Diagram

|                                                                                       |                                                                        |                                                                                                              |
| ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_ForceDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_force</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_force.py"><code>RV_force.py</code></a></p> |

**Command:** `RV_force`

<figure><img src="../../.gitbook/assets/0_creases_5.jpg" alt=""><figcaption><p>On the right side, the force diagram is created with TextDots marking the angle deviation between the form edge and its 90-degree rotated force edge. The next step, horizontal equilibrium, will aim to reduce this deviation to zero.</p></figcaption></figure>

## Horizontal Equilibrium

|                                                                                        |                                                                                 |                                                                                                                                |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_horizontal-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_horizontal</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_horizontal.py"><code>RV_tna_horizontal.py</code></a></p> |

**Command:** `RV_tna_horizontal` > `Iterations` > `1000`

<figure><img src="../../.gitbook/assets/0_creases_6.jpg" alt=""><figcaption><p>Since horizontal segments has almost no forces the force diagram collapses to a line. Nice!</p></figcaption></figure>

## Vertical Equilibrium

|                                                                                      |                                                                               |                                                                                                                            |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_vertical-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_vertical</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_tna_vertical.py"><code>RV_tna_vertical.py</code></a></p> |

**Command:** `RV_tna_vertical`&#x20;

<figure><img src="../../.gitbook/assets/0_creases_7.jpg" alt=""><figcaption><p>Vertical projection to get 3D geometry.</p></figcaption></figure>
