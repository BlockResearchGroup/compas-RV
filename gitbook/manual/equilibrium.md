# 4. Force diagram

|                                                                                    |                                                                        |                                                                                                           |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| <img src="../.gitbook/assets/RV_ForceDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_force</code></p> | <p><strong>source file</strong></p><p><a href="../../plugin/RV_force.py"><code>RV_force.py</code></a></p> |

Once the `FormDiagram` has been successfully created, the `ForceDiagram` can be created. When it is first created, the `ForceDiagram` is the dual diagram of the `FormDiagram`.&#x20;

A `ForceDiagram` is represented by the mesh datastructure.&#x20;

***

## Centroidal Dual

The Force Diagram is the dual of the Form Diagram, in the sense that both diagrams have the same number of edges and that vertices in one diagram correspond to faces in the other, and vice versa.

Initially, the Force Diagram is created as the "centroidal dual" of the Form Diagram. This means that the geometry of the Force Diagram is defined by placing its vertices at the centroids of their corresponding faces in the Form Diagram.

<figure><img src="../.gitbook/assets/forcediagram-dual.jpg" alt=""><figcaption><p>The initial form and force diagrams are topologically dual, but not yet reciprocal</p></figcaption></figure>

***

## Deviation Angles

Description
