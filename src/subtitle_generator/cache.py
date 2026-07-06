import json
from dataclasses import asdict
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


def save_json(path: Path, items: list) -> None:
    path.write_text(json.dumps([asdict(item) for item in items], indent=2))


def load_json(path: Path, cls: type[T]) -> list[T]:
    data = json.loads(path.read_text())
    return [cls(**item) for item in data]
