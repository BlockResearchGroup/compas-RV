# 1b. Modify Pattern

|                                                                                     |                                                                    |                                                                                                                   |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| <img src="../../.gitbook/assets/RV_pattern-modify.svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p>RV_pattern_modify</p> | <p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_modify.py">RV_pattern_modify.py</a></p> |

`RV_pattern_modify` allows users to make the following modifications to the `Pattern`.

***

## Modify Attributes&#x20;

### VertexAttributes

The following vertex attributes of the `ForceDiagram` can be modified.

* **is\_fixed** - If set to `True`, the vertex will remain fixed during any modifications made to the Pattern, until it is set to `False`. Fixed vertices are displayed in blue. This is set to False by default.&#x20;
* **is\_fixed** - If set to `True`, the vertex will be converted to a support remain fixed during any modifications made to the Pattern, until it is set to `False`. Support vertices are displayed in red. This is set to `False` by default.&#x20;
* **x** - Current x-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.
* **y** - Current y-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.
* **z** - Current z-coordinate of the vertex. This value is automatically computed, although can be changed manually to re-locate vertices to specific positions.

{% hint style="info" %}
In RhinoVAULT, the following vertex-selection options are provided:

* **All**: all vertices
* **Boundary**: all boundary vertices
* **Degree**: selects vertices based on a defined _vertex degree_ (number of edges that are connected to that vertex)
* **EdgeLoop**: selects all vertices along the edge loop of the selected edge
* **EdgeStrip**: selects all vertices on the edge strip of a selected edge
* **Manual**: manually select vertices
{% endhint %}

### EdgeAttributes

The following edge attributes of the `ForceDiagram` can be modified.

* **lmax** - Maximum allowable length of the edge. This value is set to 10000000.0 by default.
* **lmin** - Minimum enforced length of the edge. This value is set to 1e-06 by default.
* **q** - force density of the edge. This value is set to 1.0 by default.

{% hint style="info" %}
In RhinoVAULT, the following edge-selection options are provided:

* **All**: all edges
* **Boundary**: all boundary edges
* **EdgeLoop**: selects all edges along the edge loop of the selected edge
* **EdgeStrip**: selects all edges on the edge strip of a selected edge (only works effectively for a quad mesh or an area of mesh with consecutively joined quad faces)
* **Manual**: manually select edges
{% endhint %}
