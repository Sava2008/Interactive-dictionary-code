import json
import tkinter as tk
from random import choice
from typing import Any, Generator
from traceback import extract_stack

with open('local_dict.json', 'w') as js_file:
    json.dump(None, js_file)

local_dict: dict[str, str] = {}
main_dict: dict[str, str] = {}

def initialize_main_dict() -> None:
    global main_dict

    try:
        with open('dict.json', 'r') as js_file:
            main_dict = json.load(js_file)
    except json.decoder.JSONDecodeError:
        with open('dict.json', 'w') as js_file:
            json.dump(None, js_file)

initialize_main_dict()

with open('spare_dict.json', 'w') as js_file:
    json.dump(main_dict, js_file, indent=4)

colors: dict[str, str] = {'general_bg': '#1b1b1b', 'text_color': '#EDE9F0',
                          'button_bg': '#504A4B', 'entry_bg': '#69677C',
                          'red': '#990F02', 'green': '#0B6623'}

class EntryTempLabel(tk.Entry):
    def __init__(self: tk.Entry, parent: tk.Frame, 
                 font: tuple[str, int]=('Century', 16),
                 temp_label: str='', bg: str=colors['entry_bg'], 
                 fg: str=colors['text_color'], highlightthickness: int=2, 
                 highlightcolor: str='white', 
                 highlightbackground: str='gray', *args: tuple[Any], 
                 **kwargs: dict[str, Any]) -> None:
        super().__init__(parent, font=font, bg=bg, fg='gray',
                         highlightthickness=highlightthickness, 
                         highlightcolor=highlightcolor,
                         highlightbackground=highlightbackground, *args, 
                         **kwargs)
        self.temp_label: str = temp_label
        self.default_fg: str = fg
        self.placeholder_fg: str = '#292929'

        self.parent: tk.Frame | None = parent
        
        self.set_temp_label(temp_label)
        
        self.bind('<FocusIn>', self.clear_temp_label)
        self.bind('<FocusOut>', self.set_temp_label)
        self.bind('<Key>', self.check_temp_label)

    def clear_temp_label(self, dummy: None=None) -> None:
        if self.get() == self.temp_label:
            self.delete('0', 'end')
            self.config(fg=self.default_fg)

    def set_temp_label(self, dummy: None=None) -> None:
        if not self.get():
            self.insert(0, self.temp_label)
            self.config(fg=self.placeholder_fg)

    def check_temp_label(self, dummy: None=None) -> None:
        current_text: str = self.get()
        if current_text and current_text != self.temp_label:
            self.config(fg=self.default_fg)
    
    def destroy(self) -> None:
        self.unbind('<FocusIn>')
        self.unbind('<FocusOut>')
        self.unbind('<Key>')
        super().destroy()
        self.parent = None
        for attr in list(self.__dict__):
            delattr(self, attr)


# Templates for the future widgets
main_frame: tk.Frame | None = None

retract: tk.Button | None = None
submit: tk.Button | None = None

delete_words: tk.Button | None = None

foreign_word: tk.Entry | None = None
native_word: tk.Entry | None = None

random_word_label: tk.Label | None = None


correct: int = 0
incorrect: int = 0

random_word: tuple[str] | None = None

query: tk.Entry | None = None
environment: tk.Button | None; scrollable_frame: tk.Button | None;
scroll: tk.Scrollbar | None
environment, scrollable_frame, scroll = (None,) * 3
local_practice: tk.Button | None = None
del_words: tk.Button | None = None

checkbuttons_list: list[tk.Checkbutton] = []
bool_vars_list: list[tk.BooleanVar] = []

count: int = len(main_dict)
indent_widget: tk.Label | None = None

def fullscreen() -> bool:
    return main_win.attributes('-fullscreen')


def discard_words(caller: str='main_button_widgets') -> None:
    if caller == 'main_button_widgets':
        with open('dict.json', 'w') as js_file:
            json.dump(None, js_file)
    else:
        global main_dict, bool_vars_list, checkbuttons_list
        with open('dict.json', 'r') as js_file:
            main_dict = json.load(js_file)

        checkbuttons_list = [checkbutton for checkbutton, 
                             var in zip(checkbuttons_list, 
                                        bool_vars_list) if not var.get()]
        bool_vars_list = [var for var in bool_vars_list if not var.get()]

        checkbuttons_texts: Generator[str] = [cb.cget('text') for cb in 
                                              checkbuttons_list]
        checked: Generator[str] = \
            [c for c, b in zip(checkbuttons_texts, bool_vars_list) if not b.get()]
        main_dict = {key: value for key, value in main_dict.items() 
                        if key in checkbuttons_texts or key in
                        checked}

        with open('dict.json', 'w') as js_file:
            json.dump(main_dict, js_file, indent=4)

        submit_query()
        

def main_button_widgets() -> None:
    add_vocab: tk.Button = tk.Button(main_frame, text='Add new prompts',
                                     bg=colors['button_bg'], 
                                     fg=colors['text_color'],
                                     font=('Century', 14), command=input_mode)
    add_vocab.grid(row=1, column=2, pady=40, sticky='we')

    main_practice: tk.Button = tk.Button(main_frame,
                                         text='Practice random prompts',
                                         bg=colors['button_bg'], 
                                         fg=colors['text_color'],
                                         font=('Century', 14), command=practice_mode)
    main_practice.grid(row=2, column=2, pady=40, sticky='we')

    search: tk.Button = tk.Button(main_frame, text='Search prompts',
                                  bg=colors['button_bg'], 
                                  fg=colors['text_color'],
                                  font=('Century', 14), command=search_mode)
    search.grid(row=3, column=2, pady=40, sticky='we')

    word_count: tk.Label = tk.Label(main_frame, text=f'{len(main_dict)} words known',
                                    bg=colors['general_bg'],
                                    fg=colors['text_color'],
                                    font=('Century', 12),
                                    relief='groove')
    word_count.grid(row=1, column=1, sticky='nw', padx=80, pady=20)

    delete_words: tk.Button = tk.Button(main_frame, text='Remove all the words',
                                      bg=colors['button_bg'],
                                      fg=colors['text_color'],
                                      font=('Century', 14),
                                      command=discard_words)
    delete_words.grid(row=1, column=3, sticky='ne', padx=80, pady=20)


def reset_main_screen() -> None:
    global main_frame

    if main_frame is not None:
        main_frame.destroy()

    main_frame = tk.Frame(main_win, bg=colors['general_bg'])
    main_frame.pack(expand=True)


def initialize_foreign_entry() -> None:
    global foreign_word

    foreign_word = EntryTempLabel(parent=main_frame, 
                                  temp_label='Foreign word or phrase')
    
    caller: str = extract_stack()[-2].name
    if caller == 'input_mode':
        foreign_word.grid(row=1, column=2, pady=20, sticky='nswe')
    elif caller == 'practice_mode':
        foreign_word.grid(row=2, column=2, pady=20, sticky='nswe')
    

def submit_input() -> None:
    vocab_piece: str = foreign_word.get()
    if vocab_piece.lower().strip().startswith(('der ', 'die ', 'das ')):
        listed_vocab: list[str] = vocab_piece.split()
        vocab_piece: str = ' '.join([word.lower().capitalize() 
                                    if idx % 2 == 1 else word.lower()
                                    for idx, word in enumerate(listed_vocab)])
    translation_piece: str = native_word.get()
    foreign_word.delete(first='0', last='end')
    native_word.delete(first='0', last='end')
    foreign_word.set_temp_label()
    native_word.set_temp_label()
            
    if vocab_piece == 'Foreign word or phrase' or \
            translation_piece == 'Native word or phrase':
        pass
    else:
        main_dict[vocab_piece] = translation_piece

    foreign_word.focus()

def submit_practice(caller: str='global') -> None:
    global correct, incorrect, random_word_label, random_word

    answer: str = foreign_word.get()
    foreign_word.delete('0', 'end')
    foreign_word.focus()
    apraisals: tuple[str, ...] = ('Your answer is correct', 
                            'Well done (for now)', 
                            'You\'re a true linguist!',
                            'Not half bad!', 
                            'How\'re you even doing this?', 
                            'Hmmm... Looks like it\'s alright', 
                            'No way you got this one right', 
                            'Didn\'t get you this time')
    disapprovals: tuple[str, ...] = ('Someone is not studying enough. ' 
                                     f'{random_word[0]}',
                                     'I\'m stronger than you, human! ' 
                                     f'The answer was {random_word[0]}',
                                     f'Gotcha! The words is {random_word[0]}',
                                     'I\'ll subjucate huma-... '
                                     'I mean, the correct '
                                     f'answer is {random_word[0]}, dude...',
                                     f'Maybe next time. {random_word[0]}')
    if answer == random_word[0]:
        correct += 1
        apraisal = tk.Label(main_frame, text=choice(apraisals), 
                            bg=colors['general_bg'], fg=colors['green'], 
                            font=('Century', 14))
        apraisal.grid(row=8, column=2, sticky='we')
        apraisal.after(500, lambda: apraisal.config(bg='#9C9C9C'))
    else:
        incorrect += 1
        disapproval = tk.Label(main_frame, 
                             text=choice(disapprovals),
                             bg=colors['general_bg'], fg=colors['red'], 
                             font=('Century', 14))
        disapproval.grid(row=8, column=2, sticky='we')
        disapproval.after(500, lambda: disapproval.config(bg='#9C9C9C'))

    if caller == 'global':
        random_word = choice(tuple(main_dict.items()))

    else:
        random_word = choice(tuple(local_dict.items()))

    if random_word_label is not None:
        random_word_label.destroy()
     
    random_word_label = tk.Label(main_frame, text=random_word[1], bg='#313131', 
                             fg=colors['text_color'], font=('Century', 16), 
                             borderwidth=2, relief='ridge', 
                             width=55)
    random_word_label.grid(row=1, column=2, pady=20, sticky='we')


def submit_query() -> None:
    global local_practice, environment, scrollable_frame, scroll, del_words

    for lst in (bool_vars_list, checkbuttons_list):
        if len(lst) > 0:
            lst.clear()

    for widget in {scroll, scrollable_frame, environment, 
                   del_words, local_practice}:
        if widget is not None:
            widget.destroy()
        
    environment = tk.Canvas(main_frame, bg=colors['general_bg'])
    scrollable_frame = tk.Frame(environment, bg=colors['general_bg'])
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    scroll = tk.Scrollbar(main_frame, orient='vertical',
                          command=environment.yview)
    scroll.grid(row=1, column=1, rowspan=7, sticky='nse', padx=20)
    environment.create_window((0, 0), window=scrollable_frame, 
                               anchor='nw')
    scrollable_frame.bind('<Configure>', lambda e: 
                          environment.config(scrollregion=\
                                             environment.bbox('all'), 
                                             height=e.height))
    environment.config(yscrollcommand=scroll.set)
    environment.grid(row=1, column=1, sticky='nsew', rowspan=7, padx=20)
    environment.bind_all('<MouseWheel>', lambda event: 
                         environment.yview_scroll\
                         (int(-1 * (event.delta / 120)), 'units'))
    local_practice = tk.Button(main_frame, text='Practice', 
                                bg=colors['button_bg'], 
                                font=('Century', 18),
                                fg=colors['text_color'], 
                                command=lambda: practice_mode(scope='local'))
    local_practice.grid(row=2, column=2, padx=20, pady=20, 
                        sticky='nswe')
        
    words: list[tk.Checkbutton] = []
    scrollable_frame.update_idletasks()
    scrollable_frame.grid_propagate(False)
    environment.config(state='disabled')
    query_result: str = query.get().lower()
    filtered_dict: list[str] = [key for key, value
                                in main_dict.items() if 
                                query_result in {'enter your query', ''} or
                                key.lower().startswith(query_result) or
                                key[4:].lower().startswith(query_result) or
                                value.lower().startswith(query_result)]
                                # key[4:] is specifically for German. It removes 
                                # the articles, ensuring that both 'der Hund' and 'Hund' work
    for key in filtered_dict:
        check_var: tk.BooleanVar = tk.BooleanVar()
        queried_word = tk.Checkbutton(scrollable_frame, text=str(key),
                                      bg=colors['general_bg'], 
                                      fg=colors['text_color'],
                                      variable=check_var,
                                      selectcolor='#FF0BC2',
                                      activebackground='#533553',
                                      activeforeground='white')
        words.append(queried_word)
        bool_vars_list.append(check_var)
        checkbuttons_list.append(queried_word)

    for checkbutton in words:
        checkbutton.grid(sticky='w')
    scrollable_frame.grid_propagate(True)
    environment.config(state='normal')
    scrollable_frame.update_idletasks()

    del_words = tk.Button(main_frame, text='Remove', 
                          bg=colors['button_bg'], 
                          fg=colors['text_color'], 
                          font=('Century', 14),
                          command=lambda: 
                          discard_words(caller='local_practice'))
    del_words.grid()


def initialize_submit_button(caller: str) -> None:
    global submit, query, indent_widget

    indent_widget = tk.Label(main_frame, text=' ', bg=colors['general_bg'], 
                     font=('Century', 18))
    submit = tk.Button(main_frame, text='Submit word', 
                        bg=colors['button_bg'], fg=colors['text_color'], 
                        font=('Century', 18))

    if caller == 'input_mode':
        indent_widget.grid(row=3, column=3, pady=70)
        submit.config(command=submit_input)
        submit.grid(row=6, column=2, pady=20, sticky='nswe')

    elif caller == 'practice_mode':
        if len(local_dict) > 0:
            submit.config(command=lambda: submit_practice(caller='local'))
        else:
            submit.config(command=submit_practice)
        submit.grid(row=6, column=2, pady=60, sticky='we')

    elif caller == 'search_mode':
        query = EntryTempLabel(parent=main_frame, 
                               temp_label='Enter your query')
        query.grid(row=1, column=2)
        indent_widget.grid(row=3, column=3, pady=70)
        submit.config(command=submit_query)
        submit.grid(row=6, column=2, pady=20, sticky='nswe')


def initialize_back_button() -> None:
    global retract

    caller: str = extract_stack()[-2].name
    retract = tk.Button(main_frame, text='Main menu', bg=colors['button_bg'],
                        fg=colors['text_color'], font=('Century', 18),
                        takefocus=False, 
                        command=lambda: retract_button_func(caller=caller))
    
    if caller == 'input_mode':
        retract.grid(row=7, column=2, pady=20, sticky='nswe')

    elif caller == 'practice_mode':
        retract.grid(row=7, column=2, pady=20, sticky='nswe')

    elif caller == 'search_mode':
        retract.grid(row=7, column=2, pady=20, sticky='nswe')


def input_mode() -> None:
    '''Main function for adding new words into 
    the dictionary. Main dictionary is dict.json'''
    global native_word, retract

    initialize_main_dict()
    reset_main_screen()
    initialize_foreign_entry()
    native_word = EntryTempLabel(parent=main_frame, 
                                 temp_label='Native word or phrase')
    native_word.grid(row=2, column=2, pady=20, sticky='we')
    initialize_submit_button(caller='input_mode')
    initialize_back_button()


def practice_mode(scope: str='global') -> None:
    '''Main function for practicing random vocabulary.
    Deserializes data from dict.json, picks random items 
    and puzzles the user to type the paired foreign 
    vocabulary correctly'''
    global indent_widget, random_word, random_word_label
    reset_main_screen()
    initialize_main_dict()
    if len(main_dict) > 0:
        if scope == 'global':
            random_word = choice(tuple(main_dict.items()))
        elif scope == 'local':
            for cb, var in zip(checkbuttons_list, bool_vars_list):
                if var.get():
                    text: str = cb.cget('text')
                    local_dict[text] = main_dict[text]
            if len(local_dict) > 0:
                random_word = choice(tuple(local_dict.items()))
                checkbuttons_list.clear()
                bool_vars_list.clear()

        try:
            if len(local_dict) > 0:
                reset_main_screen()
            random_word_label = tk.Label(main_frame, text=random_word[1], 
                                                    bg='#313131', 
                                                    fg=colors['text_color'], font=('Century', 16), 
                                                    borderwidth=2, relief='ridge', width=55)
            random_word_label.grid(row=1, column=2, pady=20, sticky='we')
        except (IndexError, TypeError):
            indent_widget = tk.Label(main_frame,
                                     text='Select something!',
                                     bg=colors['general_bg'], fg=colors['red'],
                                     font=('Century', 14))
            indent_widget.grid(row=3, column=2)
            indent_widget.after(1000, lambda: indent_widget.destroy())
        else:
            initialize_foreign_entry()
            initialize_submit_button(caller='practice_mode')
            initialize_back_button()

    else:
        if indent_widget is not None:
            indent_widget.destroy()
        indent_widget = tk.Label(main_frame, text='No prompts yet', fg=colors['red'],
                         bg=colors['general_bg'])
        indent_widget.grid(row=4, column=2)
        main_frame.after(1000, lambda: indent_widget.destroy())


def search_mode() -> None:
    '''Main function which handles searching through 
    the dict.json dictionary. It provides the user 
    with local practice_mode and targeted deletion'''
    initialize_main_dict()
    if main_dict is not None:
        reset_main_screen()
        initialize_submit_button(caller='search_mode')
        initialize_back_button()
    else:
        global indent_widget
        if indent_widget is not None:
            indent_widget.destroy()
        indent_widget = tk.Label(main_frame, text='No prompts yet', fg=colors['red'],
                         bg=colors['general_bg'])
        indent_widget.grid(row=4, column=2)
        main_frame.after(1000, lambda: indent_widget.destroy())


def retract_button_func(caller: str | None=None) -> None:
    global main_dict, count

    reset_main_screen()
    main_button_widgets()
    if caller == 'input_mode':
        with open('dict.json', 'w') as js_file:
            json.dump(main_dict, js_file, indent=4)
    elif caller == 'practice_mode':
        global indent_widget
        try:
            score: int = round((correct / (correct + incorrect)) * 100, 1)
        except ZeroDivisionError:
            score: int = 0
        indent_widget = tk.Label(main_frame, text=f'you scored {score}% accuracy', 
                         bg=colors['general_bg'], fg=colors['text_color'], 
                         font=('Century', 16))
        indent_widget.grid(row=3, column=3, sticky='we')

        if len(local_dict) > 0:
            local_dict.clear()

    with open('dict.json', 'r') as js_file:
        count = len(json.load(js_file))


# Toplevel configurations
main_win: tk.Toplevel = tk.Tk()
main_win.title('Sava dictionary 1.2.2')
main_win.geometry('1000x600')
main_win.configure(bg=colors['general_bg'])
main_win.iconbitmap('4033369.ico')
main_win.bind('<F11>', lambda m: main_win.attributes('-fullscreen', not main_win.attributes('-fullscreen')))

retract_button_func()

main_win.mainloop()