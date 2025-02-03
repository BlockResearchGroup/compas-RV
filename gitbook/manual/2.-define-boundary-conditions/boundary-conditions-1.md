# 2b. Relax Pattern

<table><thead><tr><th></th><th width="237"></th><th></th></tr></thead><tbody><tr><td><img src="../../.gitbook/assets/RV_relax.svg" alt="" data-size="original"></td><td><p><strong>Rhino command name</strong></p><p><code>RV_pattern_relax</code></p></td><td><p><strong>source file</strong></p><p><a href="../../../plugin/RV_pattern_relax.py"><code>RV_pattern_relax.py</code></a></p></td></tr></tbody></table>

An opening is a chain of edges at the boundary of a `Pattern`, in between two support vertices. In general, openings in shell structures cannot be straight in plan, unless there are no internal forces in the non-boundary edges at the openings (e.g. barrel vault or cross vault).

`RV_pattern_relax` relaxes the entire `Pattern` to introduce curvature to the openings and boundaries. The relaxation is done based on the _force density method (FDM)_ ([Schek, 1974](https://www.sciencedirect.com/science/article/pii/0045782574900450)), which calculates the equilibrium shape by assigning a ratio of axial force magnitude **F** to length **L** (force density, **q=F/L**) to each element or edge in the structure, which allows for the efficient computation of form-finding solutions.&#x20;

Instead of solving directly for lengths and forces, FDM assigns these force densities as fixed parameters, simplifying the equations. The method then solves for equilibrium by ensuring that forces at each node balance in three-dimensional space. This involves setting up equilibrium equations for each node in terms of force densities rather than individual force magnitudes and lengths.

Because the force densities are constants, the equilibrium equations become linear, which makes FDM computationally efficient and stable. This linearity allows FDM to handle complex shapes and materials without iterative, nonlinear solutions required by some other methods.

The default value for **q** for all edges are 1. When `RV_pattern_relax` is triggered, FDM is applied to the `Pattern` using the **q** values of all the edges. [`Identify supports`](boundary-conditions.md) is a crucial step to complete before relaxing the `Pattern`, as the number and location of the supports will impact the geometry of the resulting relaxed `Pattern`. &#x20;

{% hint style="danger" %}
Make sure to have supports defined before relaxing the `Pattern`!
{% endhint %}
