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

<figure><img src="../../.gitbook/assets/examples_pillow_vault.png" alt=""><figcaption></figcaption></figure>

A pillow vault is a type of vaulted ceiling with convex, pillow-like sections, often formed by intersecting barrel vaults or domes, creating a smooth, rounded appearance. It is a simplest example where all mesh boundary vertices are set as supports.

{% file src="../../.gitbook/assets/examples_pillow_vault.3dm" %}

***

## 1. Create Pattern

**Command:** `RV_pattern` > `RhinoMesh`

Create a pattern from a mesh. You can start with the attached Rhino file or a session file.

<figure><img src="../../.gitbook/assets/examples_pillow_vault_0.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assetsexamples_pillow_vault_0.json" %}

***

## 2. Identify Supports

**Command:** `RV_pattern_supports` > `Add`> `Manual`> `Select Vertices`

Manually set the boundary points on the top and bottom edges of the mesh.

<figure><img src="../../.gitbook/assets/examples_pillow_vault_1.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_pillow_vault_1.json" %}

***

## 3. Form Diagram

**Command:** `RV_form`

The mesh geometry is converted into a line preview, marked with green lines.

<figure><img src="../../.gitbook/assets/examples_pillow_vault_2.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_pillow_vault_2.png" %}

***

## 4. Force Diagram

**Command:** `RV_force`

On the right side, the force diagram is created with TextDots marking the angle deviation between the form edge and its 90-degree rotated force edge. In the next step, horizontal equilibrium will be applied to reduce this deviation to zero.

<figure><img src="../../.gitbook/assets/examples_pillow_vault_3.png" alt=""><figcaption><p>.</p></figcaption></figure>

{% file src="../../.gitbook/assets/examples_pillow_vault_3.png" %}

***

## 5. Horizontal Equilibrium

**Command:** `RV_tna_horizontal`

Leave default parameters as is to reach the horizontal equilibrium. Since horizontal segments have almost no force, the force diagram collapses to a line.

<figure><img src="../../.gitbook/assets/examples_pillow_vault_4.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_pillow_vault_4.png" %}

***

## 6. Vertical Equilibrium

**Command:** `RV_tna_vertical` > `2`

The final geometry is computed by running the vertical equilibrium command, change the height to 2 to match the preview. For preview, we use the following options:`RV_settings > Drawing > show_pipes` and `show_forces`.

<figure><img src="../../.gitbook/assets/examples_pillow_vault_5.png" alt=""><figcaption></figcaption></figure>

{% file src="../../.gitbook/assets/examples_pillow_vault_5.png" %}
