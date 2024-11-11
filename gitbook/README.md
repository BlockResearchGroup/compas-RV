---
description: The official guide to using RhinoVAULT
cover: .gitbook/assets/RV_splash.jpg
coverY: 0
layout:
  cover:
    visible: true
    size: full
  title:
    visible: false
  description:
    visible: false
  tableOfContents:
    visible: false
  outline:
    visible: false
  pagination:
    visible: true
---

# About



<figure><img src=".gitbook/assets/RV_splash.jpg" alt=""><figcaption></figcaption></figure>

The Rhinoceros® plug-in [RhinoVAULT](https://www.food4rhino.com/en/app/rhinovault), originally developed by Dr. Matthias Rippmann at the Block Research Group at ETH Zurich, emerged from research on structural form finding using the _Thrust Network Analysis (TNA)_ approach to intuitively create and explore compression-only structures.

Using reciprocal diagrams, RhinoVAULT provides an intuitive, fast funicular form-finding method, adopting the same advantages of techniques such as _Graphic Statics_, but offering a viable extension to three-dimensional problems. Our goal is to share a transparent setup to let you not only create beautiful shapes but also to give you an understanding of the underlying structural principles.

The current development of RhinoVAULT is implemented based on the [COMPAS](https://compas-dev.github.io/) framework.

***

## Research Platform <a href="#research-platform" id="research-platform"></a>

‌RhinoVAULT is an open-source research and development platform for funicular form-finding built with [COMPAS](https://compas-dev.github.io/), a Python-based framework for computational research and collaboration in Architecture, Engineering, and Digital Fabrication.

RhinoVAULT is a plugin that is specifically developed for Rhino 8 and above, built entirely with open source packages from the COMPAS ecosystem and will, therefore, be available not only for Rhino and Grasshopper, but also for Blender and other tools with a Python scripting interface, and ultimately even in the browser.

***

## COMPAS

RhinoVAULT uses the following COMPAS packages. After installing RhinoVAULT with Yak, these requirements will be installed automatically if they are not yet available. Note that the tool ,ight be unresponsive for a few seconds while this happens. The packages are installed in a separate virtual environment named `rhinovault`.

* [compas](https://github.com/compas-dev/compas)
* [compas\_ags](https://github.com/blockresearchgroup/compas\_fd)
* [compas\_fd](https://github.com/blockresearchgroup/compas\_fd)
* [compas\_rui](https://github.com/blockresearchgroup/compas\_rui)
* [compas\_session](https://github.com/blockresearchgroup/compas\_session)
* [compas\_tna](https://github.com/blockresearchgroup/compas\_dr)

***

## Open Source

The development of RhinoVAULT is hosted on Github and is entirely open source, and we very much welcome your feedback. Please use the [issue tracker](https://github.com/BlockResearchGroup/compas-RV/issues) of the RhinoVAULT GitHub repository or the [COMPAS forum](https://forum.compas-framework.org/) to submit information about bugs, technical problems, or feature requests.
