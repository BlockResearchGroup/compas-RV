# 2a. Identify Supports

<table><thead><tr><th></th><th width="228"></th><th></th></tr></thead><tbody><tr><td> <img src="../.gitbook/assets/RV_supports (2).svg" alt=""></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p></td><td><p><strong>source file</strong></p><p><a href="../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p></td></tr></tbody></table>

A `Pattern` object is a mesh datastructure that describes the topology of the structure. Several additional layers of information regarding the boundary conditions need to be added in order to give the `Pattern` a structural meaning: identification of the supports, and treatment of the openings and open edges.

In RhinoVAULT, a _support_ is defined as a vertex of the structure that is fixed, and can have external horizontal reactions. `RV_pattern_supports` allows user to _Add_ ore _Remove_ supports from the `Pattern`.&#x20;
