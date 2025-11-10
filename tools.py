from json import dump, load
from typing import Any
from enum import StrEnum


class JsonMode(StrEnum):
    write = "w"
    read = "r"


class RgbColor(StrEnum):
    toplevel_bg = "#1b1b1b"
    text = "#EDE9F0"
    button_bg = "#504A4B"
    entry_bg = "#69677C"
    red = "#990F02"
    green = "#0B6623"


def manipulate_json(
    path: str, mode: JsonMode, content: Any | None = None
) -> Any | None:
    with open(path, mode) as js_file:
        match mode:
            case mode.read:
                return load(js_file)
            case mode.write:
                dump(content, js_file)
