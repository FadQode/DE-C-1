import json
from pathlib import Path


def load_raw_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)