from json import JSONDecodeError, dump, load
from typing import Any
from enum import StrEnum, Enum
import sys


class JsonMode(StrEnum):
    write = "w"
    read = "r"


class PracticeType(Enum):
    normal = 0
    local = 1


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
                dump(content, js_file, indent=4)
