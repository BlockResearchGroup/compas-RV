# Getting Started

COMPAS RhinoVAULT is a plugin for Rhino 8 and uses the new CPython runtime.
It can be installed using Yak, Rhino's package manager.

{% hint style="warning" %}
COMPAS Masonry is **only available for Rhino 8.**
{% endhint %}

## Requirements

* [Rhino 8](https://www.rhino3d.com/)

## Installation

* Start Rhino 8 and launch Yak by typing `PackageManager` on the Rhino command line.
* Search the online packages for "RhinoVAULT".
* Select "COMPAS RhinoVAULT" from the list.
* Install.

<figure>
    <img src="/gitbook/.gitbook/assets/RhinoVAULT_yak.png" alt="COMPAS RhinoVAULT in package manager Yak" />
    <figcaption>
        <p>COMPAS RhinoVAULT can be installed using Yak, the package manager of Rhino.</p>
    </figcaption>
</figure>

## COMPAS Packages

RhinoVAULT uses the following COMPAS packages:

* [compas](https://github.com/compas-dev/compas)
* [compas_fd](https://github.com/blockresearchgroup/compas_fd)
* [compas_rui](https://github.com/blockresearchgroup/compas_rui)
* [compas_session](https://github.com/blockresearchgroup/compas_session)
* [compas_tna](https://github.com/blockresearchgroup/compas_tna)

After installing RhinoVAULT with Yak, these requirements will be installed automatically if they are not yet available.
Note that the tool might be unresponsive for a few seconds while this happens.
The packages are installed in a separate virtual environment named `rhinovault`.

## Toolbar

COMPAS RhinoVAULT defines the following Rhino commands:

> [!WARNING]
> This list is incomplete...

* `RV`
* `RV_session_undo`
* `RV_session_redo`
* `RV_session_open`
* `RV_session_save`
* `RV_scene_clear`
* `RV_scene_redraw`
* `RV_settings`

These commands can be executed at the Rhino Command Prompt (simply start typing the command name),
or using the RhinoVAULT toolbar.

<figure><img src="/gitbook/.gitbook/assets/RhinoVAULT_toolbar.png" alt="COMPAS RhinoVAULT toolbar"><figcaption><p>COMPAS RhinoVAULT commands are available via the toolbar.</p></figcaption></figure>

If the toolbar is not visible after installing RhinoVAULT,
you can load it from the "Toolbars" page.
To open the "Toolbars" page, type `Toolbars` on the Rhino command line...

<figure><img src="/gitbook/.gitbook/assets/Rhino_toolbars.png" alt="Rhino Toolbars page"><figcaption><p>Load the toolbar using the "Toolbars" page.</p></figcaption></figure>

## Check the Installation

To check the installation, simply press the left-most button on the toolbar.
This will install any missing COMPAS packages and display a "Splash" screen when the installation is completed.
Close the screen by agreeing to the [legal terms](../additional-information/legal-terms.md) of using COMPAS-RhinoVAULT.

Note that installing the packages (and the dependencies of the packages) may take some time,
so don't worry if the the dialog doesn't pop up immediately...

<figure><img src="/gitbook/.gitbook/assets/RhinoVAULT_splash.png" alt="RhinoVAULT splash"><figcaption><p>Once all missing COMPAS packages and their dependencies are installed, a "Splash" screen pops up.</p></figcaption></figure>
