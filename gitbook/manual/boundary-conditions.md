# 2. Boundary Conditions

A `Pattern` object is a mesh datastructure that describes the topology of the structure. Several additional layers of information regarding the boundary conditions need to be added in order to give the `Pattern` a structural meaning: identification of the supports; treatment of the openings and open edges; and defining the loading condition.

## 2a. Identify Supports

|                                                 |                                                                                                                                                                                                                         |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  ![](<../.gitbook/assets/RV\_supports (2).svg>) | <p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p><p></p><p><strong>source fil</strong>e</p><p><a href="../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p> |

In RhinoVAULT, a _support_ is defined as a vertex of the structure that is fixed, and can have external horizontal reactions. `RV_pattern_supports` allows user to _Add_ ore _Remove_ supports from the `Pattern`. The vertices can be selected using these modes:

* **All**: all vertices
* **Boundary**: all boundary vertices
* **Degree**: selects vertices based on a defined _vertex degree_ (number of edges that are connected to that vertex)
* **EdgeLoop**: selects all vertices along the edge loop of the selected edge
* **Manual**: manually select vertices

***

## 2b. Relax Pattern

|                                                                         |                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img src="../.gitbook/assets/RV_relax.svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p><p></p><p><strong>source fil</strong>e</p><p><a href="../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p> |



***

## 2c. Update Boundaries

|                                                                                  |                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <img src="../.gitbook/assets/RV_boundaries (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_pattern_bnoundaries</code></p><p></p><p><strong>source fil</strong>e</p><p><a href="../../plugin/RV_pattern_boundaries.py"><code>RV_pattern_boundaries.py</code></a></p> |

