from dict_state import Session
from tools import JsonMode, manipulate_json, PracticeType
from json import JSONDecodeError
import sys
from os import system
from random import choice
from time import sleep


class GeneralMode:
    @staticmethod
    def submit(session: Session) -> None:
        while True:
            print(
                "enter the desired mode:\n1 - input mode\n2 - practice mode\n3 - search mode\n4 - quit"
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
                case "q" | "e" | "4":
                    sys.exit(0)
                case _:
                    print("bad mode argument choose one: 1, 2, 3 or 4")


class InputMode:
    @staticmethod
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

    @staticmethod
    def leave(session) -> None:
        json_data: dict[str, str] = manipulate_json(
            session.main_dict_path, JsonMode.read
        )
        session.main_dict |= json_data
        manipulate_json(
            session.main_dict_path, JsonMode.write, session.main_dict
        )
        session.main_dict.clear()
        system("cls")
        session.mode = GeneralMode


class PracticeMode:
    @staticmethod
    def submit(session: Session) -> None:
        data: tuple[tuple[str, str], ...] = (
            tuple(
                manipulate_json(session.main_dict_path, JsonMode.read).items()
            )
            if session.practice_type == PracticeType.normal
            else tuple(session.local_dict.items())
        )
        while True:
            chosen_word: tuple[str, str] = choice(data)
            print(f"{chosen_word[1]} - ", end="")
            match input():
                case word if word == chosen_word[0]:
                    session.correct_count += 1
                    print("good job")
                    sleep(1)
                case "1":
                    PracticeMode.leave(session)
                    break
                case _:
                    session.incorrect_count += 1
                    print(
                        f"the word was {chosen_word[0]}. If you want to leave, type 1"
                    )
                    sleep(3)

            system("cls")

    @staticmethod
    def leave(session: Session) -> None:
        system("cls")
        print(
            f"you got {(session.correct_count / (session.correct_count + session.incorrect_count)) * 100:.1f}%"
        )
        session.local_dict.clear()
        if session.practice_type == PracticeType.local:
            manipulate_json(session.local_dict_path, JsonMode.write)

        session.practice_type = PracticeType.normal
        session.mode = GeneralMode


class SearchMode:
    @staticmethod
    def submit(session: Session) -> None:
        data: dict[str, str] = manipulate_json(
            session.main_dict_path, JsonMode.read
        )
        while True:
            desired_word: str = input(
                "type the desired word, 1 to proceed to the main menu, or 2 to start practising: "
            )
            if desired_word == "1":
                SearchMode.leave()
                break

            if desired_word == "2":
                session.practice_type = PracticeType.local
                session.mode = PracticeMode
                break

            if desired_word in data.keys():
                session.local_dict[desired_word] = data[desired_word]
                print(f"selected word: {desired_word}")
            else:
                print(
                    f"the prompt {desired_word} was not found in the main dictionary"
                )

    @staticmethod
    def leave(session: Session) -> None:
        system("cls")
        session.local_dict.clear()
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
