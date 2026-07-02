from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import shutil

from study_bubbles.build_topic import _load_layout, build_single_file
from study_bubbles.container import load_container_config
from study_bubbles.style import ENGINE_ROOT, format_model_maps_summary, get_model_maps
from tools.sync_downloaded_layouts import sync_downloaded_layouts


def _build_topic(container, topic_id: str) -> int:
    topic_path = container.topics_dir / f"{topic_id}.studybubble.json"
    if not topic_path.exists():
        print(f"ERROR: topic file not found: {topic_path}")
        return 1

    layout_path: Path | None = None
    candidate = container.layouts_dir / f"{topic_id}.layout.json"
    if candidate.exists():
        layout_path = candidate

    out_html_path = container.outputs_dir / f"{topic_id}.html"
    out_html_path.parent.mkdir(parents=True, exist_ok=True)

    viewer_root = (container.engine_path / "viewer").resolve()
    if not viewer_root.exists():
        print(f"ERROR: viewer folder not found under engine path: {viewer_root}")
        return 1

    return build_single_file(
        topic_path=topic_path,
        out_html_path=out_html_path,
        layout_path=layout_path,
        project_root=container.root,
        viewer_root=viewer_root,
    )


def _topic_ids_from_updated_layouts(updated_files: list[Path]) -> list[str]:
    topic_ids: list[str] = []
    for path in updated_files:
        if path.name.endswith(".layout.json"):
            topic_ids.append(path.name[: -len(".layout.json")])
    return topic_ids


def _run_build(args: argparse.Namespace) -> int:
    try:
        container = load_container_config(cwd=Path.cwd())
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    topic_id = (args.topic or container.default_topic or "").strip()
    if not topic_id:
        print("ERROR: No topic id provided. Set [studybubble] default_topic in bubbles.ini or pass a topic id.")
        return 1
    return _build_topic(container, topic_id)


def _run_sync_layout(args: argparse.Namespace) -> int:
    try:
        container = load_container_config(cwd=Path.cwd())
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    downloads_dir = Path(args.downloads).resolve() if args.downloads else container.downloads_dir.resolve()
    if not downloads_dir.exists() or not downloads_dir.is_dir():
        print(f"FAIL: downloads_dir does not exist or is not a folder: {downloads_dir}")
        return 1

    report = sync_downloaded_layouts(
        downloads_dir=downloads_dir,
        layouts_dir=container.layouts_dir,
        dry_run=bool(args.dry_run),
    )
    topic_ids = _topic_ids_from_updated_layouts(report.updated_files)

    print(f"downloads_dir: {downloads_dir}")
    print(f"layouts_dir: {container.layouts_dir}")
    print(f"synced_layouts: {len(report.updated_files)}")
    print(f"backups_created: {len(report.backups_created)}")
    print(f"downloads_deleted: {report.deleted_count}")
    print(f"errors: {len(report.errors)}")
    for err in report.errors:
        print(f"WARN: {err}")

    if args.dry_run:
        print("dry_run: true")
        return 0

    exit_code = 0
    rebuilt = 0
    for topic_id in topic_ids:
        rc = _build_topic(container, topic_id)
        if rc == 0:
            rebuilt += 1
        else:
            exit_code = 1
    print(f"rebuilt_topics: {rebuilt}")
    return exit_code


def _run_model_maps(_args: argparse.Namespace) -> int:
    print(format_model_maps_summary())
    return 0


def _topic_id_from_filename(filename: str) -> str:
    if filename.endswith(".studybubble.json"):
        return filename[: -len(".studybubble.json")]
    if filename.endswith(".json"):
        return filename[: -len(".json")]
    return filename


def _build_topic_file(
    *,
    topic_path: Path,
    out_html_path: Path,
    layout_path: Path | None,
    project_root: Path,
    viewer_root: Path,
) -> int:
    return build_single_file(
        topic_path=topic_path,
        out_html_path=out_html_path,
        layout_path=layout_path,
        project_root=project_root,
        viewer_root=viewer_root,
    )


def _run_rebuild_all(_args: argparse.Namespace) -> int:
    learning_root = PROJECT_ROOT.parent
    viewer_root = (PROJECT_ROOT / "viewer").resolve()
    if not viewer_root.exists():
        print(f"ERROR: viewer folder not found: {viewer_root}")
        return 1

    exit_code = 0
    built = 0
    failed: list[str] = []

    print("=== StudyBubble rebuild-all (leaf dblclick fix) ===\n")

    for ini_path in sorted(learning_root.rglob("bubbles.ini")):
        if "studybubble_container_template" in ini_path.as_posix():
            continue
        container_root = ini_path.parent
        try:
            container = load_container_config(cwd=container_root)
        except FileNotFoundError as exc:
            print(str(exc))
            exit_code = 1
            continue

        topic_files = sorted(container.topics_dir.glob("*.studybubble.json"))
        if not topic_files:
            continue

        print(f"Container: {container_root.relative_to(learning_root)}")
        for topic_path in topic_files:
            topic_id = _topic_id_from_filename(topic_path.name)
            layout_path = container.layouts_dir / f"{topic_id}.layout.json"
            if not layout_path.is_file():
                layout_path = None
            out_html_path = container.outputs_dir / f"{topic_id}.html"
            rc = _build_topic_file(
                topic_path=topic_path,
                out_html_path=out_html_path,
                layout_path=layout_path,
                project_root=container.root,
                viewer_root=viewer_root,
            )
            if rc == 0:
                built += 1
                print(f"  PASS {topic_id}")
            else:
                failed.append(str(out_html_path))
                exit_code = 1
                print(f"  FAIL {topic_id}")
        print("")

    engine_topics_dir = PROJECT_ROOT / "topics"
    engine_out_dir = PROJECT_ROOT / "outputs" / "single_file"
    engine_layouts = PROJECT_ROOT / "layouts"
    if engine_topics_dir.is_dir():
        print("Engine demos: Study_bubbles/topics")
        for topic_path in sorted(engine_topics_dir.glob("*.studybubble.json")):
            topic_id = _topic_id_from_filename(topic_path.name)
            layout_path = engine_layouts / f"{topic_id}.layout.json"
            if not layout_path.is_file():
                layout_path = None
            out_html_path = engine_out_dir / f"{topic_id}.html"
            engine_out_dir.mkdir(parents=True, exist_ok=True)
            rc = _build_topic_file(
                topic_path=topic_path,
                out_html_path=out_html_path,
                layout_path=layout_path,
                project_root=PROJECT_ROOT,
                viewer_root=viewer_root,
            )
            if rc == 0:
                built += 1
                print(f"  PASS {topic_id}")
            else:
                failed.append(str(out_html_path))
                exit_code = 1
                print(f"  FAIL {topic_id}")
        print("")

    print("Model maps: references/model_maps")
    for model_map in get_model_maps():
        layout_path = model_map.layout_json if model_map.layout_json.is_file() else None
        rc = _build_topic_file(
            topic_path=model_map.topic_json,
            out_html_path=model_map.html,
            layout_path=layout_path,
            project_root=ENGINE_ROOT,
            viewer_root=viewer_root,
        )
        if rc == 0:
            built += 1
            print(f"  PASS {model_map.id}")
        else:
            failed.append(str(model_map.html))
            exit_code = 1
            print(f"  FAIL {model_map.id}")
    print("")

    print(f"Built: {built}")
    if failed:
        print(f"Failed ({len(failed)}):")
        for path in failed:
            print(f"  - {path}")

    return exit_code


def _run_import_layout(args: argparse.Namespace) -> int:
    try:
        container = load_container_config(cwd=Path.cwd())
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    layout_src = Path(args.layout_file).resolve()
    if not layout_src.is_file():
        print(f"ERROR: layout file not found: {layout_src}")
        return 1

    layout, layout_warnings, layout_errors = _load_layout(layout_src, None)
    for warning in layout_warnings:
        print(warning)
    for error in layout_errors:
        print(error)
    if layout_errors or layout is None:
        return 1

    topic_id = str(layout.get("topicId", "")).strip()
    if not topic_id:
        print("ERROR: layout file missing topicId")
        return 1

    container.layouts_dir.mkdir(parents=True, exist_ok=True)
    layout_dst = container.layouts_dir / f"{topic_id}.layout.json"
    shutil.copyfile(layout_src, layout_dst)
    print(f"PASS: layout copied to {layout_dst}")
    return _build_topic(container, topic_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="StudyBubble container CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_model_maps = sub.add_parser("model-maps", help="Show canonical model map paths")
    p_model_maps.set_defaults(handler=_run_model_maps)

    p_build = sub.add_parser("build", help="Build topic HTML from current container")
    p_build.add_argument("topic", nargs="?", default=None, help="Optional topic id override")
    p_build.set_defaults(handler=_run_build)

    p_import = sub.add_parser("import-layout", help="Import one layout file into layouts/ and rebuild")
    p_import.add_argument("layout_file", help="Path to exported .layout.json")
    p_import.set_defaults(handler=_run_import_layout)

    p_sync = sub.add_parser("sync-layout", help="Sync exported layout files from Downloads and rebuild")
    p_sync.add_argument("--downloads", default=None, help="Downloads folder override")
    p_sync.add_argument("--dry-run", action="store_true", help="Plan-only mode; do not copy/delete/rebuild")
    p_sync.set_defaults(handler=_run_sync_layout)

    p_rebuild_all = sub.add_parser(
        "rebuild-all",
        help="Rebuild every container map + engine demos + model maps (embeds current viewer)",
    )
    p_rebuild_all.set_defaults(handler=_run_rebuild_all)

    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
