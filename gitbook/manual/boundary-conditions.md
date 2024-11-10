# 2. Boundary Conditions

A `Pattern` object is a mesh datastructure that describes the topology of the structure. Several additional layers of information regarding the boundary conditions need to be added in order to give the `Pattern` a structural meaning: identification of the supports; treatment of the openings and open edges; and defining the loading condition.

## 2a. Identify Supports

<table><thead><tr><th></th><th width="228"></th><th></th></tr></thead><tbody><tr><td> <img src="../.gitbook/assets/RV_supports (2).svg" alt=""></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p></td><td><p><strong>source file</strong></p><p><a href="../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p></td></tr></tbody></table>

In RhinoVAULT, a _support_ is defined as a vertex of the structure that is fixed, and can have external horizontal reactions. `RV_pattern_supports` allows user to _Add_ ore _Remove_ supports from the `Pattern`.&#x20;

***

## 2b. Relax Pattern

<table><thead><tr><th></th><th width="237"></th><th></th></tr></thead><tbody><tr><td><img src="../.gitbook/assets/RV_relax.svg" alt="" data-size="original"></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p></td><td><p><strong>source file</strong></p><p><a href="../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p></td></tr></tbody></table>

An opening is a chain of edges at the boundary of a `Pattern`, in between two support vertices. In general, openings in TNA cannot be straight, unless there are no internal forces in the non-boundary edges at the openings (e.g. barrel vault or cross vault). In some applications where openings may already have some curvature, the relaxation will make the `Pattern` more "equilibrated" and optimal for the horizontal equilibrium solver later on.&#x20;

### Force Density method

This feature relaxes the entire `Pattern` using the _force density method_ ([Schek, 1974](https://www.sciencedirect.com/science/article/pii/0045782574900450)), resulting in curved openings. Force density of 1 is assigned to every edge. Note that supports should be properly defined in step 2a to achieve good results.

***

## 2c. Update Boundaries

<table><thead><tr><th width="221"></th><th width="253"></th><th></th></tr></thead><tbody><tr><td><img src="../.gitbook/assets/RV_boundaries (1).svg" alt="" data-size="original"></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_bnoundaries</code></p></td><td><p><strong>source file</strong></p><p><a href="../../plugin/RV_pattern_boundaries.py"><code>RV_pattern_boundaries.py</code></a></p></td></tr></tbody></table>

The treatment of the openings are very much dependent on the type of vault that is being investigated.  This feature enables users to control the curvature of each opening individually by defining the _sag_ value, which is calculated based on the percentage of the length of the opening. The $$q$$s for the boundary edges are automatically calculated based on the target _sag_ values, which are then used for the relaxation using the force density method.&#x20;

### Sag

Description

