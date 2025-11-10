from json import JSONDecodeError
from tools import manipulate_json, JsonMode


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
        self.main_dict: dict[str, str] | None = None
        self.local_dict: dict[str, str] | None = None
        self.main_dict_path: str = main_dict_path
        self.local_dict_path: str = local_dict_path
        self.spare_dict_path: str = spare_dict_path

        self.win_title: str = title
        self.win_scales: tuple[int, int] = scales
        self.icon_path: str = icon_path

        self.practice_random_word: tuple[str, str] | None = None

        self.corrent_count: int = 0
        self.incorrent_count: int = 0
        self.word_count: int = 0

    def start(self) -> None:
        manipulate_json(self.local_dict_path, JsonMode.write, None)

        try:
            self.main_dict = manipulate_json(
                self.main_dict_path, JsonMode.read
            )
            manipulate_json(
                self.spare_dict_path, JsonMode.write, self.main_dict
            )

        except (JSONDecodeError, FileNotFoundError):
            manipulate_json(self.main_dict_path, JsonMode.write, None)
