from dict_state import Session
from tools import (
    JsonMode,
    manipulate_json,
)
from json import JSONDecodeError


class GeneralMode:
    def submit(session: Session) -> None:
        while True:
            print(
                "enter the desired mode:\n1 - input mode\n2 - practice mode\n3 - search mode"
            )
            match input():
                case "i" | "1":
                    session.mode = InputMode
                    break
                case "p" | "2":
                    session.mode = PracticeMode
                    break
                case "s" | "3":
                    session.mode = SearchMode
                    break
                case _:
                    print("bad mode argument choose one: 1, 2 or 3")


class InputMode:
    def submit(session: Session) -> None:
        while True:
            print("enter the FOREIGN word, or 1 to leave:")
            foreign_prompt: str = input()
            if foreign_prompt == "1":
                InputMode.leave(session)
                break

            print("enter the NATIVE word, or 1 to leave:")
            native_prompt: str = input()
            if native_prompt == "1":
                InputMode.leave(session)
                break

            session.main_dict[foreign_prompt] = native_prompt

    def leave(session) -> None:
        json_data: dict[str, str] = manipulate_json(
            session.main_dict_path, JsonMode.read, session.main_dict
        )
        session.main_dict |= json_data
        manipulate_json(
            session.main_dict_path, JsonMode.write, session.main_dict
        )
        session.main_dict.clear()
        session.mode = GeneralMode


class PracticeMode:
    def submit(session: Session) -> None: ...
    def leave(session: Session) -> None:
        session.mode = GeneralMode


class SearchMode:
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def submit(session: Session) -> None: ...
    def leave(session: Session) -> None:
        session.mode = GeneralMode


def start(session: Session) -> None:
    manipulate_json(session.local_dict_path, JsonMode.write, None)

    try:
        session.main_dict = manipulate_json(
            session.main_dict_path, JsonMode.read
        )
        manipulate_json(
            session.spare_dict_path, JsonMode.write, session.main_dict
        )

    except (JSONDecodeError, FileNotFoundError):
        manipulate_json(session.main_dict_path, JsonMode.write, None)
