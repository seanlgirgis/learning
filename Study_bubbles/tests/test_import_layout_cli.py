from __future__ import annotations

import json
from pathlib import Path

from tools import studybubble as cli


def _write_container(root: Path, topic_id: str) -> None:
    engine = Path(__file__).resolve().parents[1]
    (root / "bubbles.ini").write_text(
        "\n".join(
            [
                "[studybubble]",
                f"name = {topic_id}",
                "mode = single-file",
                f"default_topic = {topic_id}",
                "topics_dir = topics",
                "layouts_dir = layouts",
                "outputs_dir = outputs",
                "assets_dir = assets",
                "",
                "[engine]",
                f"path = {engine.as_posix()}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    topics = root / "topics"
    topics.mkdir(parents=True, exist_ok=True)
    topic = json.loads((engine / "topics" / "tiny_capacity_demo.studybubble.json").read_text(encoding="utf-8"))
    topic["id"] = topic_id
    (topics / f"{topic_id}.studybubble.json").write_text(json.dumps(topic, indent=2), encoding="utf-8")


def test_import_layout_copies_and_rebuilds(tmp_path: Path, monkeypatch) -> None:
    topic_id = "layout_import_test"
    _write_container(tmp_path, topic_id)
    layout_src = tmp_path / "exported.layout.json"
    layout_src.write_text(
        json.dumps(
            {
                "topicId": topic_id,
                "topicTitle": "Layout Import Test",
                "version": 1,
                "nodes": {
                    "telemetry": {"x": 111.0, "y": 222.0},
                    "baseline": {"x": 333.0, "y": 444.0},
                    "forecast": {"x": 555.0, "y": 666.0},
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    rc = cli.main(["import-layout", str(layout_src)])
    assert rc == 0

    layout_dst = tmp_path / "layouts" / f"{topic_id}.layout.json"
    out_html = tmp_path / "outputs" / f"{topic_id}.html"
    assert layout_dst.is_file()
    assert out_html.is_file()
    assert '"x": 111.0' in out_html.read_text(encoding="utf-8")