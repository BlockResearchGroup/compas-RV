# 7b. Modify ForceDiagram

|                                                                                              |                                                                               |                                                                                                                            |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_ForceDiagram-modify (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_force_modify</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_force_modify.py"><code>RV_force_modify.py</code></a></p> |

`RV_force_modify` allows users to make the following modifications to the `ForceDiagram`.

***

## Modify Attributes

### VertexAttributes

The following vertex attributes of the `ForceDiagram` can be modified.

* **is\_fixed** -  If set to `True`, the vertex will remain fixed during any force-density-based relaxation or `RV_tna_horizontal`. This is set to `False` by default.
* **x** - Current x-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.
* **y** - Current y-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.
* **z** - Current z-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.

### EdgeAttributes

The following edge attributes of the `ForceDiagram` can be modified.

* **lmax** - Maximum allowable length of the edge. This value is set to 10000000.0 by default.
* **lmin** - Minimum enforced length of the edge. This value is set to 0.0 by default.

***

## Sub-commands

The following sub-commands are built into `RV_force_modify` to enable geometric modifications to the `ForceDiagram`.&#x20;

### MoveVertices

This sub-command enables users to move any vertices of the `ForceDiagram`. This is a 2-dimensional transformation on the XY plane. The transformation can be unconstrained ("free"), or constrained to: either the X or Y axis, or the XY plane.
