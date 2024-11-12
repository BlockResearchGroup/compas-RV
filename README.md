# RhinoVAULT

> [!NOTE]
> The current version of RhinoVAULT on the Rhino Yak package server is `0.5.34.9081`.
> Note that this is still a pre-release!

![RhinoVAULT](compas-RV.jpg)

RhinoVAULT is a plugin for Rhino for form finding of funicular force networks with vertical loads using Thurst Network Analysis. The current version of this plugin is based on COMPAS 2 and is available for Rhino 8 only.

## User Guide

The RhinoVAULT user guide is available as a Gitbook: [RhinoVAULT Gitbook]([https://blockresearchgroup.gitbook.io/compas-rv](https://blockresearchgroup.gitbook.io/rhinovault))

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/blockresearchgroup/compas-RV/issues).

## Developer Guide

1. Create a dev environment with `conda` using `environment.yml`.

2. Overwrite all requirements of `requirements.txt` with editable source installs.

3. Overwrite all requirements in the site-env `rhinovault` in Rhino with editable installs from local source.
   For example, for `compas`

    ```bash
    conda activate rhinovault-dev
    cd path/to/local/compas
    python -m pip install -e . --target ~/.rhinocode/py39-rh8/site-envs/rhinovault-828OGCEY
    ```
