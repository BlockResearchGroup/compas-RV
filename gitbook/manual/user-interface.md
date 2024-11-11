# Workflow & UI

## TNA workflow

<figure><img src="../.gitbook/assets/RV_workflow-diagram.jpg" alt=""><figcaption><p>Thrust Network Analysis (Block, 2009)</p></figcaption></figure>

The relationship between: the compression equilibrium shape, the thrust network or the "thrust diagram" (G); its planar projection (primal grid Γ, or the "form diagram"); and the reciprocal diagram (dual grid Γ\*, or the "force diagram" ).

***

## RhinoVAULT workflow

The workflow of RhinoVAULT is based on the theoretical framework and workflow of TNA, which can be broken down into 7 main steps, and 2 auxiliary steps.

<figure><img src="../.gitbook/assets/RV_workflow.jpg" alt=""><figcaption><p>RhinoVAULT workflow</p></figcaption></figure>

{% stepper %}
{% step %}
### 1. Create and Modify Pattern

A `Pattern` describes the topology of the `FormDiagram`. A `Pattern` is a collection of vertices interconnected by lines or "edges".  RhinoVAULT provides several methods for generating a `Pattern` and various mechanisms to modify and refine its geometry.
{% endstep %}

{% step %}
### Define Boundary Conditions

In this step, additional information is added to the `Pattern`, such as identification of the support vertices and refinement of the geometry of the unsupported boundaries.
{% endstep %}

{% step %}
### Create Form Diagram

Once the support vertices have been defined and the boundaries have been properly modified, the `FormDiagram` can be created from the `Pattern`.
{% endstep %}

{% step %}
### Create Force Diagram

Once the `FormDiagram` has been successfully created, the `ForceDiagram` can be created. In its initial state, the `ForceDiagram` is the topological dual of the `FormDiagram`; the two diagrams are not yet reciprocal (in horizontal equilibrium). &#x20;
{% endstep %}

{% step %}
### Horizontal Equilibrium

In order for the `FormDiagram` and the `ForceDiagram` to be reciprocal, the edges of one diagram needs to be perpendicular to the corresponding edge in the other diagram. `RV_tna_horizontal` iteratively repositions the vertices of the `FormDiagram` and/or `ForceDiagram` until the perpendicularity criteria (within desired angle tolerance) is met.
{% endstep %}

{% step %}
### Vertical Equilibrium

Once the `FormDiagram` and `ForceDiagram` are reciprocal, the geometry of the `ThrustDiagram` can be computed. The `ThrustDiagram` is equivalent to the `FormDiagram` with the updated z coordinates of its vertices (therefore updated self-weight at each vertex).&#x20;

Given a desired target height, `RV_tna_vertical` iteratively re-scales the `ThrustDiagram` in the z-axis, until the highest vertex of the `ThrustDigram` lies at the desired target height.
{% endstep %}

{% step %}
### Modify Diagrams

Once the vertical equilibrium has been computed, the three diagrams can be interactively modified by the user to continue form-finding explorations.
{% endstep %}

{% step %}
### Settings

Settings allows you to modify various parameters for the solving algorithms and display options.
{% endstep %}

{% step %}
### Utilities

There are several utility functions provided by RhinoVAULT: opening and saving RhinoVAULT session files; redo and undo; redraw scene; and clear scene.
{% endstep %}
{% endstepper %}

***

## RhinoVAULT UI

There are two ways of accessing the functions and features of RhinoVAULT:

* Using the Rhino command lines
* RhionVAULT toolbar

### Rhino command line

RhinoVAULT includes the following Rhino commands, which can be executed from the Rhino Command Prompt (simply start typing the command name).

* `RV`
* `RV_pattern`
* `RV_pattern_modify`
* `RV_pattern_relax`
* `RV_pattern_supports`
* `RV_pattern_boundaries`
* `RV_form`
* `RV_force`
* `RV_tna_horizontal`
* `RV_tna_vertical`
* `RV_form_modify`
* `RV_force_modify`
* `RV_thrust_modify`
* `RV_scene_clear`
* `RV_scene_redraw`
* `RV_session_undo`
* `RV_session_redo`
* `RV_session_open`
* `RV_session_save`
* `RV_settings`

<figure><img src="../.gitbook/assets/RV_command-line.png" alt=""><figcaption><p>Accessing RhinoVAULT commands from the command line.</p></figcaption></figure>

### Toolbar

All of the functionalities of RhinoVAULT are accessible through the toolbar. The toolbar is organized in the sequential order (0, 1, 2, 3... to 9 from left to right) of the steps of the [RhinoVAULT workflow](user-interface.md#rhinovault-workflow).&#x20;

<figure><img src="../.gitbook/assets/RV_toolbar-numbered.jpg" alt=""><figcaption><p>The arrangement of the RhinoVAULT toolbar according to the TNA workflow.</p></figcaption></figure>
