import ast
from pathlib import Path


HERE = Path(__file__).parent.parent


def attribute_names(filepath):
    tree = ast.parse(filepath.read_text())
    return {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}


def test_commands_do_not_use_deleted_thrustdiagram_lookup():
    for filepath in (HERE / "commands").glob("RV_*.py"):
        assert "find_thrustdiagram" not in attribute_names(filepath), filepath.name


def test_commands_do_not_use_obsolete_thrust_visibility_attributes():
    obsolete = {
        "show_vertices_3d",
        "show_edges_3d",
        "show_faces_3d",
        "show_supports_3d",
        "show_fixed_3d",
        "show_free_3d",
    }

    for filepath in (HERE / "commands").glob("RV_*.py"):
        assert not obsolete.intersection(attribute_names(filepath)), filepath.name


def test_block_export_uses_the_formdiagram_as_thrust_geometry():
    source = (HERE / "commands" / "RV_dem_blocks.py").read_text()

    assert "session.find_formdiagram()" in source
    assert "form.diagram.copy()" in source
    assert "faces_where(_is_loaded=False)" in source
