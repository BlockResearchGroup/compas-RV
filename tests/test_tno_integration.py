import ast
import base64
import json
from pathlib import Path


HERE = Path(__file__).parent.parent


def class_fields(filepath, classname):
    tree = ast.parse(filepath.read_text())
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == classname:
            return {item.target.id for item in node.body if isinstance(item, ast.AnnAssign)}
    raise AssertionError("Class {} not found.".format(classname))


def test_tno_settings_only_contain_solver_wide_options():
    fields = class_fields(HERE / "src" / "compas_rv" / "settings.py", "TNOSettings")

    assert fields == {"solver", "max_iter", "starting_point", "printout"}


def test_pattern_templates_use_compas_tna_factories():
    source = (HERE / "commands" / "RV_pattern.py").read_text()

    assert "from compas_tna.diagrams" in source
    assert "from compas_rv.patterns" not in source
    assert not list((HERE / "src" / "compas_rv" / "patterns").glob("*.py"))


def test_session_clear_removes_session_data():
    session_source = (HERE / "src" / "compas_rv" / "session.py").read_text()
    command_source = (HERE / "commands" / "RV_scene_clear.py").read_text()

    assert "self.data.clear()" in session_source
    assert "session.clear()" in command_source
    assert "session.scene.clear()" not in command_source


def test_envelope_geometry_uses_the_envelope_layer():
    source = (HERE / "src" / "compas_rv" / "scene" / "formobject.py").read_text()
    command = (HERE / "commands" / "RV_envelope.py").read_text()

    assert 'envelope_layer = "RhinoVAULT::Envelope"' in source
    assert 'boundsgroup="RhinoVAULT::Envelope::Bounds"' in source
    assert 'crackgroup="RhinoVAULT::Envelope::Cracks"' in source
    assert 'ENVELOPE_LAYER = "RhinoVAULT::Envelope"' in command
    assert command.count("layer=ENVELOPE_LAYER") == 4


def test_analysis_commands_preserve_drawing_settings():
    tna = (HERE / "commands" / "RV_tna_vertical.py").read_text()
    tno = (HERE / "commands" / "RV_tno_analysis.py").read_text()

    assert "form.show_thrust = True" in tna
    assert "formobject.show_thrust = True" in tno
    assert "session.settings.drawing" not in tna
    assert "session.settings.drawing.show_loads = True" in tno


def test_tno_loads_and_support_displacements_are_visualised():
    command = (HERE / "commands" / "RV_tno_analysis.py").read_text()
    sceneobject = (HERE / "src" / "compas_rv" / "scene" / "formobject.py").read_text()

    assert '"Initial vertical load p0 (negative downward)"' in command
    assert 'NamedValuesForm(["Ux", "Uy", "Uz"]' in command
    assert '["ux", "uy", "uz"]' in command
    assert 'vertex_attribute(vertex, "pzext")' in sceneobject
    assert "draw_support_displacements()" in sceneobject


def test_pointed_vault_rise_uses_larger_half_span_as_minimum():
    source = (HERE / "commands" / "RV_envelope.py").read_text()

    assert "minimum_rise = 0.5 * max(size)" in source
    assert "minimum=minimum_rise" in source


def test_new_commands_have_ordered_toolbar_icons():
    project = json.loads((HERE / "compas-RV.rhproj").read_text())
    codes = {code["title"]: code for code in project["codes"]}
    titles = [code["title"] for code in project["codes"]]

    assert titles.index("RV_envelope") == titles.index("RV_tna_vertical") + 1
    assert titles.index("RV_loads") == titles.index("RV_envelope") + 1
    assert titles.index("RV_tno_analysis") == titles.index("RV_loads") + 1
    assert titles.index("RV_dem_blocks") == titles.index("RV_tno_analysis") + 1

    for title, icon in (("RV_envelope", "RV_envelope.svg"), ("RV_loads", "RV_loads.svg")):
        payload = base64.b64decode(codes[title]["image"]["light"]["data"])
        assert payload == (HERE / "resources" / "icons" / icon).read_bytes()


def test_tno_analysis_uses_prepared_formdiagram_loads():
    loads = (HERE / "commands" / "RV_loads.py").read_text()
    analysis = (HERE / "commands" / "RV_tno_analysis.py").read_text()

    assert '["FromEnvelope", "External", "FromFill", "ClearAll"]' in loads
    assert "apply_selfweight_to_formdiagram" in loads
    assert "apply_fill_weight_to_formdiagram" in loads
    assert 'vertex_attribute(vertex, "pz", pz + load)' in loads
    assert 'vertices_attribute(name="pz", value=0.0)' in loads
    assert "apply_selfweight_to_formdiagram" not in analysis


def test_form_and_thrust_selection_are_explicit():
    sceneobject = (HERE / "src" / "compas_rv" / "scene" / "formobject.py").read_text()
    form_modify = (HERE / "commands" / "RV_form_modify.py").read_text()
    thrust_modify = (HERE / "commands" / "RV_thrust_modify.py").read_text()
    loads = (HERE / "commands" / "RV_loads.py").read_text()
    analysis = (HERE / "commands" / "RV_tno_analysis.py").read_text()

    assert "def select_form_vertices" in sceneobject
    assert "def select_thrust_vertices" in sceneobject
    assert "def select_form_edges" in sceneobject
    assert "def select_thrust_edges" in sceneobject
    assert 'with self._selection_context("form"' in sceneobject
    assert 'with self._selection_context("thrust"' in sceneobject
    assert "if vertex in allowed" in sceneobject
    assert "if edge in allowed" in sceneobject

    assert "select_form_vertices" in form_modify
    assert "select_form_edges" in form_modify
    assert "select_thrust_vertices" in thrust_modify
    assert "select_thrust_edges" in thrust_modify
    assert "select_thrust_vertices" in loads
    assert analysis.count("select_thrust_vertices") == 2
