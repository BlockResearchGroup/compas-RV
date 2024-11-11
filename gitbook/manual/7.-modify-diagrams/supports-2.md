# 7c. Modify ThrustDiagram

## Modify ThrustDiagram

|                                                                                           |                                                                                |                                                                                                                              |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_ThrustDiagram-modify.svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_thrust_modify</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_thrust_modify.py"><code>RV_thrust_modify.py</code></a></p> |

`RV_thrust_modify` allows users to make the following modifications to the ThrustDiagram.

***

## Modify Attributes

The following atributes of vertices, edges or faces can be made using `RV_thrust_modify` .&#x20;

### VertexAttributes

The following vertex attributes of the `ThrustDiagram` can be modified.

* **is\_fixed** - If set to `True`, the corresponding vertex of the `FormDiagram` will remain fixed during any force-density-based relaxation. This is set to `False` by default.
* **is\_support** - if set to `True`, the vertex will become a support in the `ThrustDiagram` and remain fixed during `RV_tna_vertical`. This is set to `False` by default.
* **px** - The x component of an additional load to be applied at the vertex. This value is set to 0.0 by default.
* **py** - The y component of an additional load to be applied at the vertex. This value is set to 0.0 by default.
* **pz** - The z component of an additional load to be applied at the vertex. This value is set to 0.0 by default.
* **t** - The thickness of the `ThrustDiagram` at the vertex. This value in combination with the tributary area of the vertex determines the self-weight at that vertex. This value is set to 1.0 by default.
* **x** - Current x-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.
* **y** - Current y-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.
* **z** - Current z-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.

### EdgeAttributes

The following edge attributes of the `ThrustDiagram` can be modified.

* **hmax** - This is the upper limit of the allowable internal horizontal force of the edge. This value is set to 10000000.0 by default.
* **hmin** - This is the lower limit of the allowable internal horizontal force of the edge. This value is set to 0 by default.
* **lmax** - This is the upper limit of the allowable length of the edge. This value is set to 10000000.0 by default.
* **lmin** - This is the lower limit of the allowable length of the edge. This value is set to 0 by default.

### FaceAttributes

Not implemented.

***

## Sub-commands

The following sub-commands are built into `RV_thrust_modify` to enable geometric modificiations to the `ThrustDiagram`.&#x20;

### MoveSupports

This sub-command enables users to move supports of the `ThrustDiagram`. This transformation is constrained to the z-axis.&#x20;

### ScaleForces

This sub-command enables interactive scaling of the target height, and visualize the resulting geometry of the `ThrustDiagram` in real time.
