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

# Barrel Vault

<figure><img src="../../.gitbook/assets/barrel_10.png" alt=""><figcaption></figcaption></figure>

In this tutorial, we will explore the basic features of RhinoVAULT to determine the equilibrium shape of a barrel vault with two boundary supports. To form-find the barrel vault, we will adjust the form diagram parameters for the allowable internal horizontal force limits: [**hmax**](../../manual/7.-modify-diagrams/supports.md) (upper limit) and [**hmin**](../../manual/7.-modify-diagrams/supports.md) (lower limit).

A barrel vault is unique because its edges orthogonal to the arches carry almost no load (e.g., **1e-5**), while the edges along the arches share the same internal horizontal force (e.g., **2**). The exception occurs at the boundary, where half of the horizontal force is used (e.g., **1**) for the small tributary area. Due to this special force distribution, the force diagram collapses into a single line.

{% file src="../../.gitbook/assets/barrel.3dm" %}

***

## 1. Create Pattern

**Command:** `RV_pattern` > `RhinoMesh`

Create a pattern from a mesh. You can start with the attached Rhino file or a session file.

<figure><img src="../../.gitbook/assets/barrel_0 (1).png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/rhinovault_barrel_0.json" %}

***

## 2. Identify Supports

**Command:** `RV_pattern_supports` > `Add`> `Manual`> `Select Vertices`

Manually set the boundary points on the top and bottom edges of the mesh.

<figure><img src="../../.gitbook/assets/barrel_1.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/rhinovault_barrel_1.json" %}

***

## 3. Form Diagram

**Command:** `RV_form`

The mesh geometry is converted into a line preview, marked with green lines.

<figure><img src="../../.gitbook/assets/barrel_2.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/barrel_2.png" %}

***

## 4. Modify Form Diagram

**Command:** `RV_form_modify`> `Edge Constraints` > `Manual`\
Set the horizontal edge constraints (h\_min and h\_max) to: a) 0.00001, b) vertical edges to 2, and c) vertical boundary edges to 1. This is done because horizontal edges ideally carry no load, and boundary arches have a tributary area twice as large as the outer ones.

<figure><img src="../../.gitbook/assets/barrel_3.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/barrel_4.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/barrel_5.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/rhinovault_barrel_3.json" %}

***

## 5. Force Diagram

**Command:** `RV_force`

On the right side, the force diagram is created with TextDots marking the angle deviation between the form edge and its 90-degree rotated force edge. In the next step, horizontal equilibrium will be applied to reduce this deviation to zero.

<figure><img src="../../.gitbook/assets/barrel_6.png" alt=""><figcaption><p>.</p></figcaption></figure>

{% file src="../../.gitbook/assets/rhinovault_barrel_4.json" %}

***

## 6. Horizontal Equilibrium

**Command:** `RV_tna_horizontal` > `Iterations` > `1000`

Set the iteration to 1000 to reach the horizontal equilibrium. Since horizontal segments have almost no force, the force diagram collapses to a line.

<figure><img src="../../.gitbook/assets/barrel_7.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/rhinovault_barrel_5.json" %}

***

## 7. Vertical Equilibrium

**Command:** `RV_tna_vertical`

The final geometry is computed by running the vertical equilibrium command, keeping the z-height unchanged. For preview, we use the following options:`RV_settings > Drawing > show_pipes` and `show_forces`.

<figure><img src="../../.gitbook/assets/barrel_8.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/barrel_8.png" %}
