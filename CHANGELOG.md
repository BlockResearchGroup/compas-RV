# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.1] 2026-08-31

* Changed the RhinoCode command requirements to `compas_rv >=0.10.0`.

### Added

### Changed

### Removed

## [0.10.0] 2026-08-28

### Added

* Added envelope creation from parametric vaults, middle meshes, and bound meshes, with dedicated Rhino scene layers and drawing controls.
* Added TNO analysis for minimum and maximum thrust, minimum thickness, best fit, maximum applied load, and support displacement objectives.
* Added objective-specific optimisation constraints and variables, with SLSQP and IPOPT solver selection.
* Added assessment load workflows for envelope self-weight, external point loads, fill weight, and clearing all loads.
* Added 3D thrust-network drawing, editing, and explicit form/thrust vertex and edge selection on the `FormDiagram` scene object.
* Added envelope bounds and crack visualisation, force and reaction labels, load vectors, support displacement vectors, and configurable thrust faces, edges, vertices, and pipes.
* Added outward, inward, downward, and manual support displacement presets.
* Added direct template-pattern creation through `compas_tna`, including pattern-specific discretisation options.
* Added toolbar commands and icons for envelope creation, load assignment, TNO analysis, block export, thrust inspection, and session export.

### Changed

* Changed the 3D thrust network to use the existing `FormDiagram` as the single source of equilibrium geometry and force data, while retaining compatibility with existing RhinoVAULT save files.
* Changed TNA vertical equilibrium, thrust editing, diagram export, and DEM block export to operate directly on the `FormDiagram`.
* Changed envelope-based analysis loads to remain fixed during equilibrium updates and added an explicit RV/TNO sign-convention bridge.
* Changed successful TNO analyses to update an existing `ForceDiagram` from the optimised form forces.
* Changed maximum-load analysis to collect initial loads on selected thrust-network vertices and display the optimised load vectors.
* Changed support-displacement analysis to collect and display displacement vectors on selected 3D supports.
* Changed thrust-load drawing to display the sum of `pz` and the optimised `pzext` contribution.
* Changed pointed-vault input validation so the rise is at least half of the larger span, and changed dome envelopes to use a fixed dense discretisation.
* Changed the minimum `compas_tno` requirement to `0.4.0`.
* Changed the Rhino 8 toolbar order and icons to expose the TNA, TNO, modification, and session workflows.

### Removed

* Removed the separate `ThrustDiagram` data structure and `RhinoThrustObject` scene object.
* Removed the obsolete `RV_form_solve` command.
* Removed the local pattern-template implementations superseded by the `compas_tna` factories.


## [0.9.5] 2025-07-04

### Added

### Changed

### Removed


## [0.9.4] 2025-06-26

### Added

### Changed

### Removed


## [0.9.3] 2025-06-25

### Added

### Changed

### Removed


## [0.9.2] 2025-06-24

### Added

### Changed

### Removed


## [0.9.1] 2025-06-06

### Added

### Changed

* Fixed bug in open/save paths.

### Removed


## [0.9.0] 2025-06-04

### Added

* Added `compas_cgal`.
* Added `compas_libigl`.
* Added `compas_rv.solvers.update_force_from_form`.

### Changed

* Changed minimal version of `compas` to `2.12`.

### Removed


## [0.8.1] 2025-02-08

### Added

### Changed

* Changed assignment of groups to instance attributes.

### Removed


## [0.8.0] 2025-02-08

### Added

* Added `vertexgroup`, `edgegroup`, `facegroup` to `RhinoPatternObject`.
* Added `vertexgroup`, `edgegroup`, `facegroup` to `RhinoFormObject`.
* Added `vertexgroup`, `edgegroup`, `facegroup` to `RhinoForceObject`.
* Added `vertexgroup`, `edgegroup`, `facegroup` to `RhinoThrustObject`.

### Changed

### Removed


## [0.7.0] 2025-02-07

### Added

* Added "Pattern from Skeleton".

### Changed

* Changed `compas_rui` minimal requirements.
* Fixed bug in selection by edge loop of pattern vertices.

### Removed


## [0.6.0] 2025-02-07

### Added

* Added "Pattern from Triangulation".
* Added `compas_triangle` to requirements.

### Changed

### Removed


## [0.5.0] 2025-02-03

### Added

### Changed

### Removed
