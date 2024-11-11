# 4. Force diagram

|                                                                                    |                                                                        |                                                                                                           |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| <img src="../.gitbook/assets/RV_ForceDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_force</code></p> | <p><strong>source file</strong></p><p><a href="../../plugin/RV_force.py"><code>RV_force.py</code></a></p> |

Once the `FormDiagram` has been successfully created, the `ForceDiagram` can be created. When it is first created, the `ForceDiagram` is the dual diagram of the `FormDiagram`.&#x20;

A `ForceDiagram` is represented by the [COMPAS mesh datastructure](https://compas.dev/compas/latest/api/compas.datastructures.Mesh.html).&#x20;

***

## Centroidal Dual

The `ForceDiagram` is the topological dual of the `FormDiagram`, in the sense that both diagrams have the same number of edges and that vertices in one diagram correspond to faces in the other, and vice versa.

Initially, the `ForceDiagram` is created as the "centroidal dual" of the `FormDiagram`. This means that the geometry of the Force Diagram is defined by placing its vertices at the centroids of their corresponding faces in the `FormDiagram`.



<figure><img src="../.gitbook/assets/RV_dual-diagram.png" alt=""><figcaption><p><code>ForceDiagram</code> (rigiht) is created as the "centroidal dual" of the <code>FormDiagram</code> (left).</p></figcaption></figure>

<figure><img src="../.gitbook/assets/RV_dual-diagram_edges.png" alt=""><figcaption><p>The initial form and force diagrams are topologically dual, but not yet reciprocal. Here, the corresponding dual edges are highlighted for an arbitrary node.</p></figcaption></figure>
