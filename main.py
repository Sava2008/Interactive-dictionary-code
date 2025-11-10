import state


def main() -> None:
    session: state.Session = state.Session(
        "Sava Dictionary 1.3.0",
        (1000, 600),
        "Images/Icon.ico",
        "JSON_dicts/main_dict.json",
        "JSON_dicts/local_dict.json",
        "JSON_dicts/spare_dict.json",
    )

    session.start()
    session.win.mainloop()


if __name__ == "__main__":
    main()
