# COMPAS RhinoVAULT

Implementation of RhinoVAULT using COMPAS

> [!NOTE]  
> This package contains the source code of the Rhino plugin RhinoVAULT.
> Its functionality is meant to be used inside Rhino 8 only.
> In anymother environment it will simply not work.

> [!WARNING]  
> This plugin is under active development,
> and uses the still somewhat unstable CPython infrastructure
> of Rhino 8 through the new ScriptEditor.
> Therefore, unexpected errors may occur here and there.
> Please let us know via the [Issue Tracker](https://github.com/BlockResearchGroup/compas-RV/issues) if you have problems.

## Installation

Stable releases can be installed from PyPI.

```bash
pip install compas_rv
```

To install the latest version for development, do:

```bash
git clone https://github.com/blockresearchgroup/compas_rv.git
cd compas_rv
pip install -e ".[dev]"
```

## Documentation

For further "getting started" instructions, a tutorial, examples, and an API reference,
please check out the online documentation here: [COMPAS RhinoVAULT docs](https://blockresearchgroup.github.io/compas_rv)

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com/blockresearchgroup/compas_rv/issues).
