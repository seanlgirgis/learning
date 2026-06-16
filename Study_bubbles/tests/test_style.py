from __future__ import annotations

from study_bubbles.style import (
    CANONICAL_STYLE_ID,
    get_model_map,
    get_model_maps,
    get_style_metadata,
    suggest_map_type,
)


def test_registry_loads_two_model_maps() -> None:
    maps = get_model_maps()
    assert len(maps) == 2
    ids = {model_map.id for model_map in maps}
    assert ids == {"iac_why_terraform_exists", "terraform_core_workflow"}


def test_model_map_files_exist() -> None:
    for model_map in get_model_maps():
        assert model_map.exists(), model_map.id
        assert model_map.layout_json.is_file(), model_map.id


def test_style_metadata_includes_canonical_id() -> None:
    metadata = get_style_metadata()
    assert metadata["styleId"] == CANONICAL_STYLE_ID
    assert len(metadata["modelMaps"]) == 2


def test_suggest_map_type_workflow() -> None:
    topic = {
        "groups": [{"id": "map_navigation", "label": "Map Navigation"}],
        "mapResources": [],
        "nodes": [],
    }
    assert suggest_map_type(topic) == "workflow"


def test_get_model_map_by_id() -> None:
    model_map = get_model_map("terraform_core_workflow")
    assert model_map is not None
    assert model_map.map_type == "workflow"