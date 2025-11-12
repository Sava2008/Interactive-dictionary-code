from os import path

from tools import PracticeType


class Session:
    def __init__(
        self,
        title: str,
        scales: tuple[int, int],
        icon_path: str,
        main_dict_path: str,
        local_dict_path: str,
        spare_dict_path: str,
    ) -> None:
        self.mode = None
        self.practice_type: PracticeType = PracticeType.normal

        self.main_dict: dict[str, str] | None = None
        self.local_dict: dict[str, str] | None = {}
        script_dir: str = path.dirname(path.abspath(__file__))
        self.main_dict_path: str = path.join(script_dir, main_dict_path)
        self.local_dict_path: str = path.join(script_dir, local_dict_path)
        self.spare_dict_path: str = path.join(script_dir, spare_dict_path)

        self.win_title: str = title
        self.win_scales: tuple[int, int] = scales
        self.icon_path: str = icon_path

        self.practice_random_word: tuple[str, str] | None = None

        self.correct_count: int = 0
        self.incorrect_count: int = 0
        self.word_count: int = 0
