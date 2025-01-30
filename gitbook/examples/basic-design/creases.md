---
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Creases

<figure><img src="../../.gitbook/assets/examples_creases.png" alt=""><figcaption></figcaption></figure>

This example demonstrates how to attract forces in the Thrust Diagram by adjusting the vertices of the Force Diagram. This adjustment increases the magnitude of forces in the corresponding members of the Thrust Diagram, as their edges become elongated. By extending the edges in the Force Diagram, we replicate the effect of stiffened members in the vault.

{% file src="../../.gitbook/assets/examples_creases.3dm" %}

***

## 1. Create Pattern

**Command:** `RV_pattern` > `RhinoMesh`

Create a pattern from a mesh. You can start with the attached Rhino file or a session file.

<figure><img src="../../.gitbook/assets/examples_creases_0.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_0.json" %}

***

## 2. Identify Supports

**Command:** `RV_pattern_supports` > `Add`> `Manual`> `Select Vertices`

Manually set six boundary points. The middle points mark the start and end positions of the stiffened edges.

<figure><img src="../../.gitbook/assets/examples_creases_1.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_1.json" %}

***

## 3. Pattern Boundaries

**Command:** `RV_pattern_boundaries`

A sequence of edges in a form diagram, between two boundary points, cannot be straight in plan unless there are no internal forces in the non-boundary edges at the openings (e.g., barrel vault or cross vault). Therefore, we will introduce a slight curvature by applying the force density method.

<figure><img src="../../.gitbook/assets/examples_creases_2.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_2.json" %}

***

## 4. Form Diagram

**Command:** `RV_form`

The mesh geometry is converted into a line preview, marked with green lines.

<figure><img src="../../.gitbook/assets/examples_creases_3.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_3.json" %}

***

## 5. Force Diagram

**Command:** `RV_force`

Create a force diagram that shows the angle differences between the form and force diagrams. Ideally, they should become orthogonal to each other to achieve a compression-only shell.

<figure><img src="../../.gitbook/assets/examples_creases_4.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_4.json" %}

***

## 6. Horizontal Equilibrium

**Command:** `RV_tna_horizontal`

Run the command as is wihthout changing default parameters. Horizontal equilibrium is reached when no TextDot is visible, indicating that the angles between the force and form diagrams are orthogonal within the defined tolerance.

<figure><img src="../../.gitbook/assets/examples_creases_5.png" alt=""><figcaption><p>.</p></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_5.json" %}

***

## 7. Modify Force Diagram

**Command:** `RV_force_modify`> `MoveVertices` > `Manual`

Move half of the force diagram vertices on X axis to increase the length of the edges.

<figure><img src="../../.gitbook/assets/examples_creases_6.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_6.json" %}

***

## 8. Horizontal Equilibrium

**Command:** `RV_tna_horizontal`

Rerun the horizontal equilibrium with default parameters.

<figure><img src="../../.gitbook/assets/examples_creases_7.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_7.json" %}

***

## 9. Vertical Equilibrium

**Command:** `RV_tna_vertical`&#x20;

The final geometry is computed by running the vertical equilibrium command, keeping the z-height unchanged. For preview, we use the following options:`RV_settings > Drawing > show_pipes` and `show_forces`.

<figure><img src="../../.gitbook/assets/examples_creases_8.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_creases_8.json" %}
