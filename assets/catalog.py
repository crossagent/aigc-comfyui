"""Register and stage reusable, non-model assets in this workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import TypedDict, cast


ROOT = Path(__file__).resolve().parent.parent
ORIGINALS = ROOT / "assets" / "originals"
TASKS = ROOT / "tasks"
CATALOG = ROOT / "assets" / "catalog.json"
ASSET_ID = re.compile(r"[a-z0-9][a-z0-9._-]*\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class CatalogError(Exception):
    pass


class AssetRecord(TypedDict):
    path: str
    bytes: int
    sha256: str
    source: str


class AssetCatalog(TypedDict):
    schema_version: int
    assets: dict[str, AssetRecord]


def digest(path: Path) -> str:
    hash_value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            hash_value.update(block)
    return hash_value.hexdigest()


def load_catalog() -> AssetCatalog:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise CatalogError(f"Unsupported catalog format: {CATALOG}")
    if not isinstance(data.get("assets"), dict):
        raise CatalogError(f"Catalog assets must be an object: {CATALOG}")
    for asset_id, record in data["assets"].items():
        asset_path(asset_id, record)
    return cast(AssetCatalog, data)


def asset_path(asset_id: str, record: object) -> Path:
    if not ASSET_ID.fullmatch(asset_id):
        raise CatalogError(f"Invalid asset ID in catalog: {asset_id!r}")
    if not isinstance(record, dict):
        raise CatalogError(f"Asset {asset_id}: record must be an object")
    relative = record.get("path")
    if not isinstance(relative, str) or not relative.startswith("assets/originals/"):
        raise CatalogError(f"Asset {asset_id}: path must be under assets/originals/")
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ORIGINALS.resolve()):
        raise CatalogError(f"Asset {asset_id}: path escapes assets/originals/: {relative}")
    if type(record.get("bytes")) is not int or record["bytes"] < 0:
        raise CatalogError(f"Asset {asset_id}: bytes must be a nonnegative integer")
    if not isinstance(record.get("sha256"), str) or not SHA256.fullmatch(record["sha256"]):
        raise CatalogError(f"Asset {asset_id}: sha256 must be 64 lowercase hex characters")
    if not isinstance(record.get("source"), str) or not record["source"].strip():
        raise CatalogError(f"Asset {asset_id}: source must be a nonempty description")
    return path


def check_asset(asset_id: str, record: object) -> Path:
    path = asset_path(asset_id, record)
    if not path.is_file():
        raise CatalogError(f"Asset {asset_id}: file missing at {path}; restore the binary outside Git")
    actual_size = path.stat().st_size
    if actual_size != record["bytes"]:
        raise CatalogError(
            f"Asset {asset_id}: size mismatch at {path}: expected {record['bytes']}, got {actual_size}"
        )
    actual_hash = digest(path)
    if actual_hash != record["sha256"]:
        raise CatalogError(
            f"Asset {asset_id}: SHA-256 mismatch at {path}: expected {record['sha256']}, got {actual_hash}"
        )
    return path


def save_catalog(data: AssetCatalog) -> None:
    temporary = CATALOG.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(CATALOG)


def register(asset_id: str, file_name: str, source: str) -> None:
    if not ASSET_ID.fullmatch(asset_id):
        raise CatalogError(f"Invalid asset ID {asset_id!r}; use lowercase letters, digits, '.', '_' or '-'")
    if not source.strip():
        raise CatalogError("Source description must not be empty")
    path = Path(file_name).expanduser().resolve()
    if not path.is_file() or not path.is_relative_to(ORIGINALS.resolve()):
        raise CatalogError(f"Register an existing file under {ORIGINALS}; received {path}")
    data = load_catalog()
    assets = data["assets"]
    if asset_id in assets:
        raise CatalogError(f"Asset ID already exists: {asset_id}")
    if any(asset_path(existing_id, record) == path for existing_id, record in assets.items()):
        raise CatalogError(f"File is already registered: {path}")
    assets[asset_id] = {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
        "source": source.strip(),
    }
    data["assets"] = dict(sorted(assets.items()))
    save_catalog(data)
    print(f"Registered {asset_id}: {path}")


def verify(asset_id: str | None) -> None:
    assets = load_catalog()["assets"]
    if asset_id is not None and asset_id not in assets:
        raise CatalogError(f"Unknown asset ID: {asset_id}")
    selected = {asset_id: assets[asset_id]} if asset_id is not None else assets
    failures: list[str] = []
    for current_id, record in selected.items():
        try:
            check_asset(current_id, record)
            print(f"OK {current_id}")
        except CatalogError as error:
            failures.append(str(error))
    if failures:
        raise CatalogError("\n".join(failures))
    if not selected:
        print("Catalog is empty; no reusable assets have been registered")


def task_input_path(task_name: str) -> Path:
    relative = Path(task_name)
    tasks_root = TASKS.resolve()
    task = (TASKS / relative).resolve()
    if relative.is_absolute() or task == tasks_root or not task.is_relative_to(tasks_root):
        raise CatalogError(f"Task must be a directory under {TASKS}; received {task_name!r}")
    if relative.parts[0] == "_template" or not task.is_dir():
        raise CatalogError(f"Task directory does not exist or is the template: {task}")
    input_path = (task / "comfyui" / "input").resolve()
    if not input_path.is_relative_to(task):
        raise CatalogError(f"ComfyUI input escapes task directory: {input_path}")
    return input_path


def stage(asset_id: str, task_name: str) -> None:
    assets = load_catalog()["assets"]
    if asset_id not in assets:
        raise CatalogError(f"Unknown asset ID: {asset_id}")
    source = check_asset(asset_id, assets[asset_id])
    input_path = task_input_path(task_name)
    input_path.mkdir(parents=True, exist_ok=True)
    target = input_path / f"{asset_id}{source.suffix.lower()}"
    if target.is_symlink():
        raise CatalogError(f"ComfyUI input must not be a symbolic link: {target}")
    if target.exists():
        if not target.is_file() or digest(target) != assets[asset_id]["sha256"]:
            raise CatalogError(f"ComfyUI input already exists with different content: {target}")
    else:
        temporary = input_path / f".{target.name}.tmp"
        if temporary.exists() or temporary.is_symlink():
            raise CatalogError(f"Temporary ComfyUI input already exists: {temporary}")
        shutil.copyfile(source, temporary)
        if digest(temporary) != assets[asset_id]["sha256"]:
            raise CatalogError(f"Copy failed SHA-256 verification: {temporary}")
        temporary.replace(target)
    print(f"ComfyUI task input: {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("register", help="Add metadata for a file already in assets/originals")
    add.add_argument("asset_id")
    add.add_argument("file")
    add.add_argument("--source", required=True, help="Origin or provenance description")
    inspect = commands.add_parser("verify", help="Check registered binaries against Git-tracked hashes")
    inspect.add_argument("asset_id", nargs="?")
    use = commands.add_parser("stage", help="Copy a verified asset into one task's ComfyUI input directory")
    use.add_argument("asset_id")
    use.add_argument("--task", required=True, help="Existing task path relative to tasks/")
    arguments = parser.parse_args()
    try:
        if arguments.command == "register":
            register(arguments.asset_id, arguments.file, arguments.source)
        elif arguments.command == "verify":
            verify(arguments.asset_id)
        elif arguments.command == "stage":
            stage(arguments.asset_id, arguments.task)
    except (CatalogError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
