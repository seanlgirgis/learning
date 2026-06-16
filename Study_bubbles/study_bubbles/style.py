from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]
MODEL_MAPS_ROOT = ENGINE_ROOT / "references" / "model_maps"
REGISTRY_PATH = MODEL_MAPS_ROOT / "registry.json"

CANONICAL_STYLE_ID = "terraform_learnterraform_v1"
CANONICAL_STYLE_NAME = "LearnTerraform TerraForm StudyBubble Style"
MAX_NODE_COUNT = 20
RECOMMENDED_NODE_MIN = 8
RECOMMENDED_NODE_MAX = 15


@dataclass(frozen=True)
class ModelMap:
    id: str
    map_type: str
    title: str
    bubble_count: int
    html: Path
    topic_json: Path
    layout_json: Path
    studybook_source_html: str

    def exists(self) -> bool:
        return self.html.is_file() and self.topic_json.is_file()


def _resolve_under_model_maps(relative: str) -> Path:
    return (MODEL_MAPS_ROOT / relative).resolve()


def load_registry() -> dict:
    if not REGISTRY_PATH.is_file():
        raise FileNotFoundError(f"Model map registry not found: {REGISTRY_PATH}")
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Model map registry root must be a JSON object.")
    return data


def get_model_maps() -> list[ModelMap]:
    registry = load_registry()
    maps: list[ModelMap] = []
    for entry in registry.get("model_maps", []):
        if not isinstance(entry, dict):
            continue
        maps.append(
            ModelMap(
                id=str(entry["id"]),
                map_type=str(entry["type"]),
                title=str(entry["title"]),
                bubble_count=int(entry["bubble_count"]),
                html=_resolve_under_model_maps(str(entry["html"])),
                topic_json=_resolve_under_model_maps(str(entry["topic_json"])),
                layout_json=_resolve_under_model_maps(str(entry["layout_json"])),
                studybook_source_html=str(entry.get("studybook_source_html", "")),
            )
        )
    return maps


def get_model_map(map_id: str) -> ModelMap | None:
    for model_map in get_model_maps():
        if model_map.id == map_id:
            return model_map
    return None


def get_style_metadata() -> dict:
    registry = load_registry()
    return {
        "styleId": registry.get("style_id", CANONICAL_STYLE_ID),
        "styleName": registry.get("style_name", CANONICAL_STYLE_NAME),
        "modelMaps": [
            {
                "id": model_map.id,
                "type": model_map.map_type,
                "title": model_map.title,
                "bubbleCount": model_map.bubble_count,
                "html": str(model_map.html.relative_to(ENGINE_ROOT)),
            }
            for model_map in get_model_maps()
        ],
        "nodeCount": {
            "max": MAX_NODE_COUNT,
            "recommendedMin": RECOMMENDED_NODE_MIN,
            "recommendedMax": RECOMMENDED_NODE_MAX,
        },
        "recallDoc": "MODEL_MAPS.md",
    }


def suggest_map_type(topic: dict) -> str:
    """Guess landscape vs workflow from topic shape (for authoring hints)."""
    groups = topic.get("groups") or []
    group_labels = {
        str(group.get("label", "")).strip().lower()
        for group in groups
        if isinstance(group, dict)
    }
    if "map navigation" in group_labels:
        return "workflow"
    if topic.get("mapResources"):
        return "workflow"
    node_count = len(topic.get("nodes") or [])
    if node_count <= 12 and any("workflow" in label for label in group_labels):
        return "workflow"
    return "landscape"


def format_model_maps_summary() -> str:
    lines = [
        f"Canonical style: {CANONICAL_STYLE_NAME} ({CANONICAL_STYLE_ID})",
        f"Recall doc: {ENGINE_ROOT / 'MODEL_MAPS.md'}",
        "",
        "Model maps:",
    ]
    for model_map in get_model_maps():
        lines.append(
            f"- [{model_map.map_type}] {model_map.title} ({model_map.bubble_count} bubbles)"
        )
        lines.append(f"  html: {model_map.html}")
        lines.append(f"  topic: {model_map.topic_json}")
    return "\n".join(lines)