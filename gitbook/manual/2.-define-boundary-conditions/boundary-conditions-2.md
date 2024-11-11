# 2c. Update Boundaries

<table><thead><tr><th width="221"></th><th width="253"></th><th></th></tr></thead><tbody><tr><td><img src="../../.gitbook/assets/RV_boundaries (1).svg" alt="" data-size="original"></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_bnoundaries</code></p></td><td><p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_boundaries.py"><code>RV_pattern_boundaries.py</code></a></p></td></tr></tbody></table>

The treatment of the openings are very much dependent on the type of vault that is being investigated.  This feature enables users to control the curvature of each opening individually by defining the _sag_ value, which is calculated based on the percentage of the length of the opening. The $$q$$s for the boundary edges are automatically calculated based on the target _sag_ values, which are then used for the relaxation using the force density method.&#x20;

### Sag

Description

