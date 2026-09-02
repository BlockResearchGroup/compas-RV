from contextlib import contextmanager

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino.conversions
import compas_rhino.objects
from compas.colors import Color
from compas.geometry import Cylinder
from compas.geometry import Line
from compas.geometry import Vector
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute
from compas_rui.scene import RUIMeshObject
from compas_rv.datastructures import FormDiagram
from compas_rv.session import RVSession

from .diagramobject import RhinoDiagramObject


class RhinoFormObject(RhinoDiagramObject):
    session = RVSession()
    diagram: FormDiagram  # type: ignore

    # Planar form diagram colors (existing)
    vertexcolor = ColorDictAttribute(default=Color.green())
    edgecolor = ColorDictAttribute(default=Color.green().darkened(50))
    facecolor = ColorDictAttribute(default=Color.green().lightened(25))

    # Thrust diagram colors (for 3D representation)
    thrust_vertexcolor = ColorDictAttribute(default=Color.purple())
    thrust_edgecolor = ColorDictAttribute(default=Color.purple().darkened(50))
    thrust_facecolor = ColorDictAttribute(default=Color.purple().lightened(25))
    thrust_freecolor = ColorAttribute(default=Color.purple())
    thrust_anchorcolor = ColorAttribute(default=Color.red())
    thrust_fixedcolor = ColorAttribute(default=Color.cyan())

    residualcolor = ColorAttribute(default=Color.cyan())
    reactioncolor = ColorAttribute(default=Color.green())
    loadcolor = ColorAttribute(default=Color.green().darkened(50))
    displacementcolor = ColorAttribute(default=Color.orange())
    selfweightcolor = ColorAttribute(default=Color.white())
    compressioncolor = ColorAttribute(default=Color.blue())
    tensioncolor = ColorAttribute(default=Color.red())

    form_layer = "RhinoVAULT::FormDiagram"
    thrust_layer = "RhinoVAULT::ThrustDiagram"

    def __init__(
        self,
        vertexgroup="RhinoVAULT::FormDiagram::Vertices",
        edgegroup="RhinoVAULT::FormDiagram::Edges",
        facegroup="RhinoVAULT::FormDiagram::Faces",
        layer=form_layer,
        thrust_vertexgroup="RhinoVAULT::ThrustDiagram::Vertices",
        thrust_edgegroup="RhinoVAULT::ThrustDiagram::Edges",
        thrust_facegroup="RhinoVAULT::ThrustDiagram::Faces",
        loadgroup="RhinoVAULT::ThrustDiagram::Loads",
        displacementgroup="RhinoVAULT::ThrustDiagram::SupportDisplacements",
        selfweightgroup="RhinoVAULT::ThrustDiagram::Selfweight",
        forcegroup="RhinoVAULT::ThrustDiagram::Forces",
        labelgroup="RhinoVAULT::ThrustDiagram::Labels",
        reactiongroup="RhinoVAULT::ThrustDiagram::Reactions",
        residualgroup="RhinoVAULT::ThrustDiagram::Residuals",
        show_thrust=False,
        show_thrust_vertices=True,
        show_thrust_edges=True,
        show_thrust_faces=True,
        show_thrust_supports=True,
        show_thrust_fixed=True,
        show_thrust_free=False,
        **kwargs,
    ):
        super().__init__(
            vertexgroup=vertexgroup,
            edgegroup=edgegroup,
            facegroup=facegroup,
            layer=layer,
            **kwargs,
        )

        # Store thrust diagram layer groups
        self.thrust_vertexgroup = thrust_vertexgroup
        self.thrust_edgegroup = thrust_edgegroup
        self.thrust_facegroup = thrust_facegroup
        self.loadgroup = loadgroup
        self.displacementgroup = displacementgroup
        self.selfweightgroup = selfweightgroup
        self.forcegroup = forcegroup
        self.labelgroup = labelgroup
        self.reactiongroup = reactiongroup
        self.residualgroup = residualgroup

        self.show_supports = True
        self.show_fixed = True
        self.show_free = False

        self.show_thrust = show_thrust
        self.show_thrust_vertices = show_thrust_vertices
        self.show_thrust_edges = show_thrust_edges
        self.show_thrust_faces = show_thrust_faces
        self.show_thrust_supports = show_thrust_supports
        self.show_thrust_fixed = show_thrust_fixed
        self.show_thrust_free = show_thrust_free

        self._selection_thrust_vertices = None
        self._selection_thrust_edges = None
        self._selection_active = False

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def settings(self):
        settings = super().settings
        settings["show_thrust"] = self.show_thrust
        settings["show_thrust_vertices"] = self.show_thrust_vertices
        settings["show_thrust_edges"] = self.show_thrust_edges
        settings["show_thrust_faces"] = self.show_thrust_faces
        settings["show_thrust_supports"] = self.show_thrust_supports
        settings["show_thrust_fixed"] = self.show_thrust_fixed
        settings["show_thrust_free"] = self.show_thrust_free
        return settings

    def edges(self, **kwargs):
        return self.diagram.edges_where(_is_edge=True)

    def faces(self, **kwargs):
        return self.diagram.faces_where(_is_loaded=True)

    # =============================================================================
    # Select
    # =============================================================================

    @contextmanager
    def _selection_context(self, representation, vertices=False, edges=False, faces=False):
        state = {
            "show_vertices": self.show_vertices,
            "show_edges": self.show_edges,
            "show_faces": self.show_faces,
            "show_thrust": self.show_thrust,
            "selection_thrust_vertices": self._selection_thrust_vertices,
            "selection_thrust_edges": self._selection_thrust_edges,
            "selection_active": self._selection_active,
        }

        try:
            self._selection_active = True
            if representation == "form":
                self.show_vertices = vertices
                self.show_edges = edges
                self.show_faces = faces
                self.show_thrust = False
            elif representation == "thrust":
                self.show_vertices = False
                self.show_edges = False
                self.show_faces = False
                self.show_thrust = True
                self._selection_thrust_vertices = vertices
                self._selection_thrust_edges = edges
            else:
                raise ValueError("Unknown diagram representation: {}".format(representation))

            self.redraw()
            yield
        finally:
            self.show_vertices = state["show_vertices"]
            self.show_edges = state["show_edges"]
            self.show_faces = state["show_faces"]
            self.show_thrust = state["show_thrust"]
            self._selection_thrust_vertices = state["selection_thrust_vertices"]
            self._selection_thrust_edges = state["selection_thrust_edges"]
            self._selection_active = state["selection_active"]
            rs.UnselectAllObjects()
            self.redraw()

    def select_form_vertices(self, vertices=None, message="Select Form Vertices", use_edges=True):
        vertices = list(self.diagram.vertices()) if vertices is None else list(vertices)
        edges = list(self.edges()) if use_edges else False
        allowed = set(vertices)

        with self._selection_context("form", vertices=vertices, edges=edges):
            selected = super().select_vertices(message=message, use_edges=use_edges)

        if selected is None:
            return
        return list(dict.fromkeys(vertex for vertex in selected if vertex in allowed))

    def select_thrust_vertices(self, vertices=None, message="Select Thrust Vertices", use_edges=True):
        vertices = list(self.diagram.vertices()) if vertices is None else list(vertices)
        edges = list(self.edges()) if use_edges else False
        allowed = set(vertices)

        with self._selection_context("thrust", vertices=vertices, edges=edges):
            selected = super().select_vertices(message=message, use_edges=use_edges)

        if selected is None:
            return
        return list(dict.fromkeys(vertex for vertex in selected if vertex in allowed))

    def select_form_edges(self, edges=None, message="Select Form Edges"):
        edges = list(self.edges()) if edges is None else list(edges)
        allowed = set(edges)

        with self._selection_context("form", edges=edges):
            selected = super().select_edges(message=message)

        if selected is None:
            return
        return list(dict.fromkeys(edge for edge in selected if edge in allowed))

    def select_thrust_edges(self, edges=None, message="Select Thrust Edges"):
        edges = list(self.edges()) if edges is None else list(edges)
        allowed = set(edges)

        with self._selection_context("thrust", edges=edges):
            selected = super().select_edges(message=message)

        if selected is None:
            return
        return list(dict.fromkeys(edge for edge in selected if edge in allowed))

    def select_form_faces(self, faces=None):
        faces = list(self.faces()) if faces is None else list(faces)
        allowed = set(faces)

        with self._selection_context("form", faces=faces):
            selected = super().select_faces_manual()

        if selected is None:
            return
        return list(dict.fromkeys(face for face in selected if face in allowed))

    def select_edges_loop(self):
        guids = compas_rhino.objects.select_lines(message="Select Loop Edges")
        edges = []
        for guid in guids or []:
            edge = self._guid_edge.get(guid)
            if edge is not None:
                edges += list(self.diagram.edge_loop(edge))
        return edges

    def select_edges_strip(self):
        guids = compas_rhino.objects.select_lines(message="Select Strip Edges")
        edges = []
        for guid in guids or []:
            edge = self._guid_edge.get(guid)
            if edge is not None:
                edges += list(self.diagram.edge_strip(edge))
        return edges

    # =============================================================================
    # Clear
    # =============================================================================

    # =============================================================================
    # Draw Planar
    # =============================================================================

    def draw_formdiagram(self):
        """Draw the form diagram in planar mode (z=0 for all vertices)."""
        self.layer = self.form_layer
        # Store original z coordinates
        original_z = {}
        for vertex in self.diagram.vertices():
            original_z[vertex] = self.diagram.vertex_attribute(vertex, "z")
            self.diagram.vertex_attribute(vertex, "z", 0)

        # Use existing planar colors
        for vertex in self.diagram.vertices():
            if self.diagram.vertex_attribute(vertex, "is_support"):
                self.vertexcolor[vertex] = self.anchorcolor
            elif self.diagram.vertex_attribute(vertex, "is_fixed"):
                self.vertexcolor[vertex] = self.fixedcolor
            else:
                self.vertexcolor[vertex] = self.freecolor

        # Draw using parent class method
        guids = super().draw()

        # Restore original z coordinates
        for vertex, z in original_z.items():
            self.diagram.vertex_attribute(vertex, "z", z)

        return guids

    # =============================================================================
    # Draw Thrust Diagram
    # =============================================================================

    def compute_pipe_colors(self, tol=1e-3) -> None:
        edges = list(self.edges())
        forces = [self.diagram.edge_attribute(edge, "_f") for edge in edges]
        if not forces or any(force is None for force in forces):
            return
        magnitudes = [abs(f) for f in forces]
        fmin = min(magnitudes)
        fmax = max(magnitudes)

        if fmax - fmin < tol:
            # the size of the range is already checked here
            # no need to do this again in the loop
            return

        colors = []
        for force, magnitude in zip(forces, magnitudes):
            # this will need to be updated when we include tension edges
            colors.append(Color.from_i((magnitude - fmin) / (fmax - fmin)))

        return dict(zip(edges, colors))

    def draw_thrustdiagram(self):
        self.layer = self.thrust_layer
        if self.session.settings.drawing.show_thrust_faces:
            self.draw_thrust_faces()
        self.draw_thrust_vertices()
        self.draw_thrust_edges()

        if self._selection_active:
            return self.guids

        if self.session.settings.drawing.show_reactions:
            self.draw_thrust_reactions()
        if self.session.settings.drawing.show_loads:
            self.draw_thrust_loads()
        if self.session.settings.drawing.show_support_displacements:
            self.draw_support_displacements()
        if self.session.settings.drawing.show_selfweight:
            self.draw_thrust_selfweight()
        if self.session.settings.drawing.show_pipes:
            self.draw_thrust_pipes()
        if self.session.settings.drawing.show_force_labels:
            self.draw_thrust_force_labels()
        return self.guids

    def draw_thrust_vertices(self):
        settings = self.session.settings.drawing
        if self._selection_thrust_vertices is not None:
            vertices = self._selection_thrust_vertices
        else:
            vertices = []
            if settings.show_thrust_vertices:
                if settings.show_thrust_free:
                    vertices += list(self.diagram.vertices_where(is_support=False, is_fixed=False))
                if settings.show_thrust_fixed:
                    vertices += list(self.diagram.vertices_where(is_fixed=True))
                if settings.show_thrust_supports:
                    vertices += list(self.diagram.vertices_where(is_support=True))

        show_vertices = self.show_vertices
        self.show_vertices = vertices
        try:
            guids = super().draw_vertices(
                anchorcolor=self.thrust_anchorcolor,
                fixedcolor=self.thrust_fixedcolor,
                freecolor=self.thrust_freecolor,
            )
        finally:
            self.show_vertices = show_vertices

        if guids:
            if self.thrust_vertexgroup:
                self.add_to_group(self.thrust_vertexgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_thrust_edges(self):
        if self._selection_thrust_edges is not None:
            edges = self._selection_thrust_edges
        else:
            edges = []
            if self.session.settings.drawing.show_thrust_edges:
                edges = list(self.diagram.edges_where(_is_edge=True))

        if edges:
            for edge in edges:
                self.edgecolor[edge] = self.thrust_edgecolor

        show_edges = self.show_edges
        self.show_edges = edges
        try:
            guids = RUIMeshObject.draw_edges(self)
        finally:
            self.show_edges = show_edges

        if guids:
            if self.thrust_edgegroup:
                self.add_to_group(self.thrust_edgegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_thrust_faces(self):
        faces = list(self.diagram.faces_where(_is_loaded=True))
        for face in faces:
            self.facecolor[face] = self.thrust_facecolor

        show_faces = self.show_faces
        self.show_faces = faces
        try:
            guids = RUIMeshObject.draw_faces(self)
        finally:
            self.show_faces = show_faces

        if guids:
            if self.thrust_facegroup:
                self.add_to_group(self.thrust_facegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_thrust_reactions(self):
        guids = []

        scale = self.session.settings.drawing.scale_reactions
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=True):
            residual = Vector(*self.diagram.vertex_attributes(vertex, ["_rx", "_ry", "_rz"]))
            vector = residual * scale

            if vector.length > tol:
                name = "{}.vertex.{}.reaction".format(self.diagram.name, vertex)
                attr = self.compile_attributes(name=name, color=Color.green(), arrow="start")
                point = self.diagram.vertex_point(vertex)
                line = Line.from_point_and_vector(point, vector)
                guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                guids.append(guid)

                if self.session.settings.drawing.show_reaction_labels and residual.length >= self.session.settings.drawing.tol_labels:
                    text = "{0:.1f}".format(residual.length)
                    attr = self.compile_attributes(name=name + ".label", color=self.reactioncolor)
                    guid = sc.doc.Objects.AddTextDot(text, compas_rhino.conversions.point_to_rhino(line.midpoint), attr)
                    guids.append(guid)

        if guids:
            if self.reactiongroup:
                self.add_to_group(self.reactiongroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_thrust_loads(self):
        guids = []

        scale = self.session.settings.drawing.scale_loads
        color = self.loadcolor
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=False):
            load = self.diagram.vertex_attributes(vertex, ["px", "py", "pz"])
            pzext = self.diagram.vertex_attribute(vertex, "pzext")
            if pzext is not None:
                load[2] += pzext

            if load is not None:
                vector = Vector(*load) * scale
                if vector.length > tol:
                    name = "{}.vertex.{}.load".format(self.diagram.name, vertex)
                    attr = self.compile_attributes(name=name, color=color, arrow="start")
                    point = self.diagram.vertex_point(vertex)
                    line = Line.from_point_and_vector(point, vector)
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.loadgroup:
                self.add_to_group(self.loadgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_support_displacements(self):
        guids = []

        scale = self.session.settings.drawing.scale_support_displacements
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=True):
            displacement = self.diagram.vertex_attributes(vertex, ["ux", "uy", "uz"])
            if displacement is None:
                continue

            vector = Vector(*displacement) * scale
            if vector.length <= tol:
                continue

            name = "{}.vertex.{}.supportdisplacement".format(self.diagram.name, vertex)
            attr = self.compile_attributes(name=name, color=self.displacementcolor, arrow="end")
            point = self.diagram.vertex_point(vertex)
            line = Line.from_point_and_vector(point, vector)
            guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
            guids.append(guid)

        if guids:
            if self.displacementgroup:
                self.add_to_group(self.displacementgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_thrust_selfweight(self):
        guids = []

        scale = self.session.settings.drawing.scale_selfweight
        color = self.selfweightcolor
        tol = self.session.settings.drawing.tol_vectors

        for vertex in self.diagram.vertices_where(is_support=False):
            thickness = self.diagram.vertex_attribute(vertex, "t")

            if thickness:
                area = self.diagram.vertex_area(vertex)
                weight = area * thickness
                point = self.diagram.vertex_point(vertex)
                vector = Vector(0, 0, -weight * scale)
                if vector.length > tol:
                    line = Line.from_point_and_vector(point, vector)
                    name = "{}.vertex.{}.selfweight".format(self.diagram.name, vertex)
                    attr = self.compile_attributes(name=name, color=color, arrow="end")
                    guid = sc.doc.Objects.AddLine(compas_rhino.conversions.line_to_rhino(line), attr)
                    guids.append(guid)

        if guids:
            if self.selfweightgroup:
                self.add_to_group(self.selfweightgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_thrust_pipes(self):
        guids = []

        scale = self.session.settings.drawing.scale_pipes
        tol = self.session.settings.drawing.tol_pipes

        pipe_colors = self.compute_pipe_colors()

        for edge in self.edges():
            force = self.diagram.edge_attribute(edge, "_f")

            if force:
                line = self.diagram.edge_line(edge)
                radius = abs(force) * scale

                color = self.compressioncolor
                if self.session.settings.drawing.show_forces and pipe_colors:
                    color = pipe_colors[edge]

                if radius > tol:
                    pipe = Cylinder.from_line_and_radius(line, radius)
                    name = "{}.edge.{}.force".format(self.diagram.name, edge)
                    attr = self.compile_attributes(name=name, color=color)
                    guid = sc.doc.Objects.AddBrep(compas_rhino.conversions.cylinder_to_rhino_brep(pipe), attr)
                    guids.append(guid)

        if guids:
            if self.forcegroup:
                self.add_to_group(self.forcegroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    def draw_thrust_force_labels(self):
        guids = []

        for edge in self.diagram.edges_where(_is_edge=True):
            q = self.diagram.edge_attribute(edge, "q")
            if q is None:
                continue

            force = q * self.diagram.edge_length(edge)
            if abs(force) < self.session.settings.drawing.tol_labels:
                continue

            name = "{}.edge.{}.force.label".format(self.diagram.name, edge)
            attr = self.compile_attributes(name=name, color=self.compressioncolor)
            text = "{0:.1f}".format(force)
            point = self.diagram.edge_midpoint(edge)
            guid = sc.doc.Objects.AddTextDot(text, compas_rhino.conversions.point_to_rhino(point), attr)
            guids.append(guid)

        if guids:
            if self.labelgroup:
                self.add_to_group(self.labelgroup, guids)
            elif self.group:
                self.add_to_group(self.group, guids)

        self._guids += guids
        return guids

    # =============================================================================
    # Draw
    # =============================================================================

    def draw(self):
        """Draw method shows 2D and 3D if enabled, otherwise shows 2D only."""
        self.draw_formdiagram()
        if self.show_thrust:
            self.draw_thrustdiagram()
        return self.guids

    # =============================================================================
    # Redraw
    # =============================================================================

    def redraw(self):
        rs.EnableRedraw(False)
        self.clear()
        self.draw()
        rs.EnableRedraw(True)
        rs.Redraw()

    def redraw_vertices(self):
        self.redraw()

    def redraw_edges(self):
        self.redraw()

    def redraw_faces(self):
        self.redraw()
