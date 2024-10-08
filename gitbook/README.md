---
description: The official guide to using RhinoVAULT
---

# About

<figure><img src=".gitbook/assets/compas-RV_popup.jpg" alt=""><figcaption></figcaption></figure>

The Rhinoceros® plug-in [RhinoVAULT](https://www.food4rhino.com/en/app/rhinovault), originally developed by Dr. Matthias Rippmann at the Block Research Group at ETH Zurich, emerged from research on structural form finding using the _Thrust Network Analysis (TNA)_ approach to intuitively create and explore compression-only structures.

Using reciprocal diagrams, RhinoVAULT provides an intuitive, fast funicular form-finding method, adopting the same advantages of techniques such as _Graphic Statics_, but offering a viable extension to three-dimensional problems. Our goal is to share a transparent setup to let you not only create beautiful shapes but also to give you an understanding of the underlying structural principles.

The current version of RhinoVAULT is implemented based on the [COMPAS](https://compas-dev.github.io/) framework.&#x20;

***

## Research Platform <a href="#research-platform" id="research-platform"></a>

‌RhinoVAULT is an open-source research and development platform for funicular form-finding built with [COMPAS](https://compas-dev.github.io/), a Python-based framework for computational research and collaboration in Architecture, Engineering, and Digital Fabrication.&#x20;

RhinoVAULT is a plugin that is specifically developed for Rhino 8 and above, built entirely with open source packages from the COMPAS ecosystem and will, therefore, be available not only for Rhino and Grasshopper, but also for Blender and other tools with a Python scripting interface, and ultimately even in the browser.

***

## COMPAS

The core functionality of RhinoVAULT is based on the following COMPAS packages and can be used in any environment that supports Python. The core pipeline is set up flexibly without any dependencies to a specific CAD software; CAD software simply functions as the visualisation canvas and UI.

* [compas](https://github.com/compas-dev/compas)
  * Base data structures
  * File support
  * Numerical solvers
  * Geometry processing
* [compas\_tna](https://github.com/blockresearchgroup/compas\_tna)
  * Form, Force and Thrust Diagrams
  * Horizontal equilibrium
  * Vertical equilibrium

For the design of force patterns in Form Diagrams, we use

* [compas\_singular](https://github.com/BlockResearchGroup/compas\_singular)
  * Pattern design based on topological features and placement of singularities in quad meshes.
* [compas\_skeleton](https://github.com/blockresearchgroup/compas\_skeleton)
  * Pattern design based on line skeletons.
* [compas\_triangle](https://github.com/blockresearchgroup/compas\_triangle)
  * Pattern design based on Constrained/Conforming Delaunay Triangulations.

CAD integration packages make this core functionality available in specific software like Blender or Rhino. The current release of RhinoVAULT provides only a plugin for Rhino (Blender and Grasshopper integration is under development and will be available soon):

* [compas\_rhino](https://github.com/compas-dev/compas)
  * Geometry and data structure conversions.
  * Drawing functionality.
  * Selections and interaction.
* [compas\_cloud](https://github.com/BlockResearchGroup/compas\_cloud)
  * Remote Procedure Calls

***

## Open Source

The development of RhinoVAULT is hosted on Github and is entirely open source, and we very much welcome your feedback. Please use the [issue tracker](https://github.com/BlockResearchGroup/compas-RV/issues) of the RhinoVAULT GitHub repository or the [COMPAS forum](https://forum.compas-framework.org/) to submit information about bugs, technical problems, or feature requests.

***

## Disclaimer

The development of RhinoVAULT is currently led by the Block Research Group at ETH Zurich, with many other contributors from the research community. It is shared freely under the MIT License in the hope that you will enjoy it and use it for original and creative work. It can be freely shared and used for academic and commercial purposes, but with proper attribution.

If you use RhinoVAULT for projects, publications or other applications, please cite:

```
@misc{compas-RV,
    title = {{RhinoVAULT}: Funicular Form Finding for Rhinoceros},
    author = {Tom Van Mele, Juney Lee, Li Chen},
    year = {2024},
    doi = {},
    url = {https://github.com/BlockResearchGroup/compas-RV},
}
```

Please refer to the original paper that laid the foundation for RhinoVAULT:

* Rippmann, M., Lachauer, L. and Block, P. Interactive Vault Design, International Journal of Space Structures 27 (4): 219-230, 2012 &#x20;
* Rippmann, M. and Block, P. Funicular Shell Design Exploration, Proceedings of the 33rd Annual Conference of the ACADIA Waterloo/Buffalo/Nottingham, Canada 2013    &#x20;
