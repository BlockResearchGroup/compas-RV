# 2b. Relax Pattern

<table><thead><tr><th></th><th width="237"></th><th></th></tr></thead><tbody><tr><td><img src="../../.gitbook/assets/RV_relax.svg" alt="" data-size="original"></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_supports</code></p></td><td><p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_supports.py"><code>RV_pattern_supports.py</code></a></p></td></tr></tbody></table>

An opening is a chain of edges at the boundary of a `Pattern`, in between two support vertices. In general, openings in TNA cannot be straight, unless there are no internal forces in the non-boundary edges at the openings (e.g. barrel vault or cross vault). In some applications where openings may already have some curvature, the relaxation will make the `Pattern` more "equilibrated" and optimal for the horizontal equilibrium solver later on.&#x20;

### Force Density method

This feature relaxes the entire `Pattern` using the _force density method_ ([Schek, 1974](https://www.sciencedirect.com/science/article/pii/0045782574900450)), resulting in curved openings. Force density of 1 is assigned to every edge. Note that supports should be properly defined in step 2a to achieve good results.
