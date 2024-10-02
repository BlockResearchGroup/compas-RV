# COMPAS RhinoVAULT

> [!NOTE]
> The current version of COMPAS-RhinoVAULT on the Yak package server is `0.2.5`.
> Note that this is still a pre-release!

![RhinoVAULT](compas-RV.jpg)

RhinoVAULT is a plugin for Rhino for form finding of funicular force networks with vertical loads using Thurst Network Analysis. The current version of this plugin is based on COMPAS 2 and is available for Rhino 8.

## Installation

To install RhinoVAULT, use Rhino's package manager Yak.

![RhinoVAULT installation with Yak](resources/images/RhinoVAULT_yak.png)

## COMPAS Packages

RhinoVAULT uses the following COMPAS packages:

* [compas](https://github.com/compas-dev/compas)
* [compas_ags](https://github.com/blockresearchgroup/compas_fd)
* [compas_fd](https://github.com/blockresearchgroup/compas_fd)
* [compas_rui](https://github.com/blockresearchgroup/compas_rui)
* [compas_session](https://github.com/blockresearchgroup/compas_session)
* [compas_tna](https://github.com/blockresearchgroup/compas_dr)

After installing RhinoVAULT with Yak, these requirements will be installed automatically if they are not yet available.
Note that the tool ,ight be unresponsive for a few seconds while this happens.
The packages are installed in a separate virtual environment named `rhinovault`.

## User Interface

RhinoVAULT defines the following commands:

* `RV`
* `RV_pattern`
* `RV_pattern_modify`
* `RV_pattern_relax`
* `RV_pattern_supports`
* `RV_pattern_boundaries`
* `RV_form`
* `RV_force`
* `RV_tna_horizontal`
* `RV_tna_vertical`
* `RV_form_modify`
* `RV_force_modify`
* `RV_thrust_modify`
* `RV_scene_clear`
* `RV_scene_redraw`
* `RV_session_undo`
* `RV_session_redo`
* `RV_session_open`
* `RV_session_save`
* `RV_settings`

These commands can be executed at the Rhino Command Prompt (simply start typing the command name),
or using the RhinoVAULT toolbar.

![RhinoVAULT toolbar](resources/images/RhinoVAULT_toolbar.png)

## Documentation

For further "getting started" instructions, a tutorial, examples, and an detailed description of the individual commands and the user interface, please check out the online documentation here: [RhinoVAULT Gitbook](https://blockresearchgroup.gitbook.io/RhinoVAULT)

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/blockresearchgroup/compas-RV/issues).
