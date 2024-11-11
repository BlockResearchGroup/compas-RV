# 7a. Modify FormDiagram

|                                                                                             |                                                                              |                                                                                                                          |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| <img src="../../.gitbook/assets/RV_FormDiagram-modify (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_form_modify</code></p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_form_modify.py"><code>RV_form_modify.py</code></a></p> |

`RV_form_modify` allows users to make the following modifications to the `FormDiagram`.

***

## Sub-commands&#x20;

The following sub-commands are built into `RV_form_modify` to enable geometric modifications to the `ForceDiagram`.&#x20;

### Dropdowns

This sub-command allows users to create new dropdown supports. This will move the vertices to z=0, and convert it to a support. `RV_tna_vertical` will need to be recomputed to obtain the updated `ThrustDiagram`.

### Supports

Not implemented.

### Loads

This sub-command allows users to impose additional point loads to the selected vertices, by modifying the value for `pz`. The user can also modify the thickness `t` for the vertex, thereby changing the self-weight at that vertex.

### Openings

Not implemented.

### EdgeConstraints

The following edge attributes of the `FormDiagram` can be modified.

* **hmax** - This is the upper limit of the allowable internal horizontal force of the edge. This value is set to 10000000.0 by default.
* **hmin** - This is the lower limit of the allowable internal horizontal force of the edge. This value is set to 0 by default.
* **lmax** - This is the upper limit of the allowable length of the edge. This value is set to 10000000.0 by default.
* **lmin** - This is the lower limit of the allowable length of the edge. This value is set to 0 by default.

### ForceDensities

Not implemented.
