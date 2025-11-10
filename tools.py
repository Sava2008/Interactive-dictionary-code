from json import JSONDecodeError, dump, load
from typing import Any
from enum import StrEnum
import sys


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
            case JsonMode.read:
                try:
                    data = load(js_file)
                    return data if data else {}
                except JSONDecodeError:
                    sys.stderr.write(
                        "Json file is corrupted. Try validating it"
                    )
                    sys.exit(1)

            case JsonMode.write:
                dump(content, js_file)
