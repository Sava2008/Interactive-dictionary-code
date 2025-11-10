import tkinter as tk
from state import Session
from tools import RgbColor, WidgetOperation, manipulate_widgets


class GeneralMode:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def retract(self) -> None:
        if self.session.main_frame is not None:
            self.session.main_frame.destroy()

        self.session.main_frame = tk.Frame(
            self.session.win, bg=RgbColor.toplevel_bg
        )
        self.session.main_frame.pack(expand=True, fill="both")

    def submit(self) -> str:
        return self.session.foreign_word.get()


class InputMode(GeneralMode):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def retract(self) -> None:
        return super().retract()

    def submit(self) -> None:
        foreign_input: str = super().submit()
        match foreign_input:
            case "":
                return None
            case _:
                native_input: str = self.session.native_word.get()
                if (
                    native_input not in ("", "placeholder")
                    and self.session.main_dict is not None
                ):
                    self.session.main_dict[foreign_input] = native_input
                manipulate_widgets(
                    WidgetOperation.clear,
                    None,
                    self.session.foreign_word,
                    self.session.native_word,
                )


class PracticeMode(GeneralMode):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def retract(self) -> None:
        return super().retract()

    def submit(self) -> None: ...


class SearchMode(GeneralMode):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def retract(self) -> None:
        return super().retract()

    def submit(self) -> None: ...
