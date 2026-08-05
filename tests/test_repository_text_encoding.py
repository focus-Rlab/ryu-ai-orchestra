from pathlib import Path


TEXT_SUFFIXES = {".md", ".json", ".py", ".toml", ".yml", ".yaml"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__"}


def test_repository_text_files_are_utf8():
    root = Path(__file__).resolve().parents[1]
    failures = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{path.relative_to(root)}: {exc}")
    assert failures == []
