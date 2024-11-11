# 3. Form diagram

|                                                                                   |                                                                       |                                                                                                         |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| <img src="../.gitbook/assets/RV_FormDiagram (1).svg" alt="" data-size="original"> | <p><strong>Rhino command name</strong></p><p><code>RV_form</code></p> | <p><strong>source file</strong></p><p><a href="../../plugin/RV_form.py"><code>RV_form.py</code></a></p> |

`FormDiagram` is the 2D projection of the `ThrustDiagram`. The boundary condition information, such as the support locations and loading conditions, is automatically inherited from the `Pattern`. Any edges of the pattern, of which both endpoints are supports are removed from the `FormDiagram`.&#x20;

A `FormDiagram` is represented by the [COMPAS mesh datastructure](https://compas.dev/compas/latest/api/compas.datastructures.Mesh.html).

<figure><img src="../.gitbook/assets/formdiagram_boundary-edges.jpg" alt=""><figcaption><p>Depending on how the support vertices are defined, corners of the Pattern are automatically processed during the creation of the <code>FormDiagram</code>.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/formdiagram_corners.jpg" alt=""><figcaption><p>Automatic removal of the corner supports of a quad grid mesh, which have edges at that support that are fully constrained.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/formdiagram_corners-triangle.jpg" alt=""><figcaption><p>Automatic removal of the corner supports in a tri mesh, which have edges at that support that are fully constrained.</p></figcaption></figure>
