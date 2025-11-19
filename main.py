from dict_control import (
    GeneralMode,
    InputMode,
    PracticeMode,
    SearchMode,
    start,
)
import dict_state
import sys
import os


def main() -> None:
    current_dir = os.path.dirname(__file__)
    session: dict_state.Session = dict_state.Session(
        "Sava Dictionary 1.3.0",
        (1000, 600),
        os.path.join(current_dir, r"Images\Icon.ico"),
        os.path.join(current_dir, r"JSON_dicts\main_dict.json"),
        os.path.join(current_dir, r"JSON_dicts\local_dict.json"),
        os.path.join(current_dir, r"JSON_dicts\spare_dict.json"),
    )
    session.mode = GeneralMode
    start(session)
    while True:
        match session.mode:
            case m if m in (GeneralMode, InputMode, PracticeMode, SearchMode):
                m.submit(session)
            case _:
                sys.stderr.write("Unknown mode")
                sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input()
