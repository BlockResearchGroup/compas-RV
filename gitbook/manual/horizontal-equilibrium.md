# 5. Horizontal equilibrium

|                                                                                     |                                                                                 |                                                                                                                             |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| <img src="../.gitbook/assets/RV_horizontal-eq (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_tna_horizontal</code></p> | <p><strong>source file</strong></p><p><a href="../../plugin/RV_tna_horizontal.py"><code>RV_tna_horizontal.py</code></a></p> |

This function geometrically reconfigures the the edges of the ForceDiagram, such that the corresponding edges of the FormDiagram and Forcediagram become parallel (in the conventional graphic statics sense), or perpendicular (the 90° rotated, RhinoVAULT convention). The resulting ForceDiagram and FormDiagram are reciprocal where the two diagrams are topological duals of the other and all pairs of corresponding edges are parallel (within tolerance).

***

## Reciprocal Diagrams

In order for the Form and Force Diagram to describe the distribution of horizontal thrust in a three-dimensional network of compression forces in equilibrium with vertical loads applied to its nodes, they need to be not only dual, but also reciprocal.&#x20;

Two diagrams are reciprocal if they are dual, and if their corresponding edges are at a constant angle with each other. Typically, corresponding edges are required to be parallel, or perpendicular, but any other constant angle is sufficient as well.

In RhinoVAULT, the Form and Force Diagram are considered reciprocal if corresponding edges are perpendicular.

<figure><img src="../.gitbook/assets/forcediagram-reciprocal.jpg" alt=""><figcaption><p>After horizontal equilibrium has been found, the form and force diagrams are now reciprocal.</p></figcaption></figure>

***

## Horizontal Forces

Once the Form and Force Diagram are reciprocal they describe the horizontal equilibrium of the corresponding three-dimensional force network. The edges of the Form Diagram define the directions and points of application of the forces, whereas the edges of the Force Diagram define the distribution of force magnitudes along those directions.

The magnitudes of horizontal forces are equal to the lengths of the edges in the Force Diagram, multiplied with a scaling factor.&#x20;

***

## Algorithm Parameters

### Alpha

In RhinoVAULT, horizontal equilibrium is computed by parallelising the edges of the Form and Force Diagram to corresponding target vectors. These target vectors are defined as the weighted average of the vectors of corresponding edge pairs. Therefore, the most important parameter for the calculation of horizontal equilibrium in RV2 is `alpha`, which is the weighting factor for the calculation of the target vectors.

If `alpha = 100`, the target vectors are completely defined by the vectors of the edges of the Form Diagram. This means that only the geometry of the Force Diagram will be updated to achieve horizontal equilibrium. This is the default.

If `alpha = 0`, the target vectors are completely defined by the edges of the force diagram. Therefore only the Form Diagram will be updated.

For all other values, the target vectors are calculated using the following formula:

$$
t_i = \alpha \cdot \hat{e}_{i, form} + (1 - \alpha) \cdot \hat{e}_{i, force}
$$

Note that using `alpha` efficiently requires a bit of practice and experience. Since the Form Diagram defines the intended  layout of horizontal forces and RV2 has many tools for designing force layouts that provide a good starting point for form finding explorations, it is usually a good idea to start with `alpha = 100`. However, once you have the horizontal equilibrium under control, playing around with lower `alpha` values can have a significant influence on finding nicely balanced force distributions.

### Iterations

Computing horizontal equilibrium is an iterative process. The default number of iterations is `100`. For sensible force layouts, this value should go a long way. However, there are many cases in which more iterations are required. For example, if the Form Diagram has multiple open/unsupported edges, and especially if those edges have a low "sag" value, more iterations will typically be required to reduce all angle deviations between corresponding edges to less than 5 degrees.

Computing horizontal equilibrium is quite fast. Therefore, don't hesitate to set the number of iterations to `1000` or more if the need arises. However, don't go completely overboard either (`10000` iterations is quite excessive in most cases), because the calculation has no stoppage criterion, since it tends to be more computationally expensive to check for convergence than to just run all the requested iterations.

Furthermore, resolving all angle deviations is not an absolute requirement, and is in many cases unnecessary. For example, the angle deviations between very short edges tend to be quite persistent as they are dominated by edges with (much) longer lengths during the calculation process. Since short edges in the Force Diagram also represent (relatively) small horizontal forces, these deviations can often be ignored.

### Refreshrate

The iterations of the horizontal equilibrium calculation process is dynamically visualised. The rate at which the diagrams are updated is controlled by the refreshrate. The default value is `10`, which means that the diagrams are updated every 10 iterations.

For large diagrams the dynamic visualisation slows down the calculations a little bit. In these cases, and/or for high numbers of iterations (`> 1000`), it is therefore advisable to set the refreshrate to a higher value. For example, if the number of iterations is `1000`, then a refresh rate of `100` seems more appropriate.



***

##



