# just for review and history of my improvement!
# this code is unoptimized and inexpert!


import json
import random
import tkinter as tk
from tkinter import *

words = {}

with open('local_words.json', 'w') as js_file:
    json.dump(None, js_file)

try:
    with open('dict.json', 'r') as js_file:
        availability = json.load(js_file)
except json.decoder.JSONDecodeError:
    with open('dict.json', 'w') as js_file:
        json.dump(None, js_file)

#interface
win = tk.Tk()
win.title('Sava dictionary')
win.geometry('900x600')
win.configure(bg = '#1b1b1b')
win.iconbitmap('4033369.ico')
win.resizable(False, False)
version = tk.Label(win, text = '1.2.1', bg = '#1b1b1b', fg = '#7C6E7F', font = ('Courier', 14))
version.place(height = 30, width = 60, x = 830, y = 570)
def disable_button(x):
     x.configure(state = 'disabled')

def enable_button(x):
    x.configure(state = 'normal')

def input_regime():
    key = tk.Entry(win, bg = '#7F7D9C', font = ('Cascadia code', 11), fg = '#322D31')
    value = tk.Entry(win, bg = '#7F7D9C', font = ('Cascadia code', 11), fg = '#322D31')
    key.place(height = 40, width = 180, x = 360, y = 290)
    value.place(height = 40, width = 180, x = 360, y = 350)
    pointer1 = tk.Label(win, text = 'Input the word here', font = ('Calibre', 11), 
                              bg = '#1b1b1b', fg = '#848482')
    pointer2 = tk.Label(win, text = 'Input the translation here', font = ('Calibre', 11), 
                              bg = '#1b1b1b', fg = '#848482')
    pointer1.place(height = 40, width = 160, x = 195, y = 290)
    pointer2.place(height = 40, width = 190, x = 165, y = 350)
    consent = tk.Button(win, text = 'Consent adding', command = continuation, bg = '#504A4B', 
                        font = ('Consolas', 11), fg = '#E7DECC')
    consent.place(height = 30, width = 150, x = 200, y = 450)
    global inp, search, train
    disable_button(inp)
    disable_button(train)
    disable_button(search)
    def going_back():
        nonlocal back_button, key, value, submit, consent, pointer1, pointer2
        global inp, search, train
        back_button.destroy()
        enable_button(inp)
        enable_button(train)
        enable_button(search)
        key.destroy()
        value.destroy()
        submit.destroy()
        consent.destroy()
        pointer1.destroy()
        pointer2.destroy()
    back_button = tk.Button(win, text = 'back', command = going_back, bg = '#504A4B', font = ('Consolas', 11),
                            fg = '#E7DECC')
    back_button.place(height = 40, width = 180, x = 360, y = 540)
    def insertion():
        global words
        words[key.get()] = value.get()
        key.delete('0', 'end')
        value.delete('0', 'end')
    submit = tk.Button(win, text = 'Submit', command = insertion, bg = '#504A4B', font = ('Consolas', 11), 
                       fg = '#E7DECC')
    submit.place(height = 30, width = 150, x = 520, y = 450)
    
def continuation():
    try:
        with open('dict.json', 'r') as json_file:
            data = json.load(json_file)
            words.update(data)
        with open('dict.json', 'w') as json_file:
            json.dump(words, json_file, indent = 4)
    except TypeError or json.JSONDecodeError:
        with open('dict.json', 'w') as json_file:
            json.dump(words, json_file, indent = 4)
    finally:
        temp_label = tk.Label(win, text = 'Saved new prompts successfully!', font = ('Calibre', 11), 
                              fg = '#0B6623', bg = '#1b1b1b')
        temp_label.place(height = 30, width = 220, x = 10, y = 10)
        temp_label.after(3000, lambda: temp_label.destroy())

#practice regime
def practice():
    with open('dict.json', 'r') as json_file:
        data = json.load(json_file)

        if data == None:
            temp_label = tk.Label(win, text = 'No prompts yet', font = ('Calibre', 11), 
                                  fg = '#990F02', bg = '#1b1b1b')
            temp_label.place(height = 40, width = 100, x = 0, y = 0)
            temp_label.after(1000, lambda: temp_label.destroy())
        
        else:
            temp_label = tk.Label(win, text = f'{len(data)} words known. Congats!', font = ('Calibre', 12), bg = '#1b1b1b', 
                              fg = '#848482', relief = 'groove')
            temp_label.place(height = 30, width = 220, x = 10, y = 10)
            correct, incorrect = 0, 0
            global inp, search, train
            disable_button(inp)
            disable_button(train)
            disable_button(search)
            def stop_loop():
                nonlocal temp_label, back_button, german, submit, english
                temp_label.destroy()
                back_button.destroy()
                german.destroy()
                submit.destroy()
                english.destroy()
                precision()
                global inp, search, train
                enable_button(inp)
                enable_button(train)
                enable_button(search)
            back_button = tk.Button(win, text = 'back', command = stop_loop, bg = '#504A4B', font = ('Consolas', 11), 
                                    fg = '#E7DECC')
            back_button.place(height = 40, width = 180, x = 360, y = 540)
            german = tk.Entry(win, bg = '#7F7D9C', font = ('Cascadia code', 11), fg = '#322D31')
            german.place(height = 40, width = 240, x = 470, y = 400)
            var = None
            key, value = random.choice(list(data.items()))
            english = tk.Label(win, text = value, bg = '#564C4D', font = ('Calibre', 11))
            english.place(height = 40, width = 240, x = 190, y = 400)

            def submission():
                nonlocal key, value, var, english, german, correct, incorrect
                english.destroy()
                var = german.get()
                if var == key:
                    correct += 1
                    appraisal = tk.Label(win, text = 'Good job!', bg = '#1b1b1b', font = ('Calibre', 18), fg = '#0B6623')
                    appraisal.place(height = 30, width = 120, x = 390, y = 320)
                    win.after(1000, lambda: appraisal.destroy())
                    german.delete('0', 'end')
                else:
                    incorrect += 1
                    disapproval = tk.Label(win, text = f'No! The correct word was "{key}"!',
                    bg = '#1b1b1b', font = ('Calibre', 18), fg = '#990F02')
                    disapproval.place(height = 50, width = 600, x = 150, y = 320)
                    win.after(5000, lambda: disapproval.destroy())
                    german.delete('0', 'end')
                key, value = random.choice(list(data.items()))
                english = tk.Label(win, text = value, bg = '#564C4D', font = ('Calibre', 11))
                english.place(height = 40, width = 240, x = 190, y = 400)
            
            submit = tk.Button(win, text = 'Submit your guess', command = submission, bg = '#504A4B', font = ('Consolas', 11), 
                            fg = '#E7DECC')
            submit.place(height = 30, width = 150, x = 375, y = 460)
    def precision():
        try:
            temp_label = tk.Label(win, text = f'correct answers: {correct}, incorrect answers: {incorrect}, \n\
            your precision: {round((correct / (correct + incorrect)) * 100, 1)}%', font = ('Calibre', 11), fg = '#848482', 
            bg = '#1b1b1b')
            temp_label.place(height = 80, width = 340, x = 280, y = 400)
            temp_label.after(5000, lambda : temp_label.destroy())
        except ZeroDivisionError:
            pass
def lookup():
    with open('dict.json', 'r') as json_file:
        data = json.load(json_file)
        if data == None:
            temp_label = tk.Label(win, text = 'No prompts yet', font = ('Calibre', 11), 
                                  fg = '#990F02', bg = '#1b1b1b')
            temp_label.place(height = 40, width = 100, x = 0, y = 0)
            temp_label.after(1000, lambda: temp_label.destroy())
        else:
            query = tk.Entry(win, bg = '#7F7D9C', font = ('Cascadia code', 11), fg = '#322D31')
            query.place(height = 40, width = 240, x = 330, y = 400)
            gotten_query, result, res_env, scrollable_frame, scroll  = None, None, None, None, None
            global inp, search, train
            disable_button(inp)
            disable_button(train)
            disable_button(search)
            res, varis = [], []
            pract, actual_pract, word_delete = None, None, None
            def gets():
                nonlocal result, actual_pract, res_env, scrollable_frame, scroll, varis, res, pract, query, gotten_query, word_delete
                try:
                    word_delete.destroy()
                except AttributeError:
                    pass
                try:
                    scroll.destroy()
                except AttributeError:
                    pass
                try:
                    actual_pract.destroy()
                except AttributeError:
                    pass
                try:
                    scrollable_frame.destroy()
                except AttributeError:
                    pass
                try:
                    res_env.destroy()
                except AttributeError:
                    pass
                try:
                    pract.destroy()
                except AttributeError:
                    pass
                res_env = tk.Canvas(win, bg = '#363636', width = 300, highlightthickness = 0)
                scrollable_frame = tk.Frame(res_env, bg = '#363636')
                scroll = tk.Scrollbar(win, orient = 'vertical', command = res_env.yview)
                scrollable_frame.bind('<Configure>', lambda e: res_env.configure(scrollregion = res_env.bbox('all')))
                res_env.create_window((0, 0), window = scrollable_frame, anchor = 'nw')
                res_env.pack(anchor = 'nw', fill = 'y', expand = True)
                res_env.configure(yscrollcommand = scroll.set)
                scroll.place(x = 300, height = 600)
                for result in res:
                    try:
                        result.destroy()
                    except AttributeError:
                        pass
                gotten_query = query.get()
                for item in data: 
                    if item.startswith(gotten_query):
                        vari = tk.BooleanVar()
                        result = tk.Checkbutton(scrollable_frame, text = str(item), bg = '#363636', 
                                        font = ('Calibre', 11), fg = '#848482', variable = vari)
                        result.pack(anchor = 'nw')
                        res.append(result)
                        varis.append(vari)
                local_words = {}
                
                def del_words():
                    nonlocal item, actual_pract, data, local_words, res, vari, result, pract, query
                    with open('dict.json', 'r') as js_file:
                        data = json.load(js_file)
                        for i, vari in enumerate(varis):
                            if vari.get():
                                data.pop(res[i].cget('text'))
                                vari.set(False)
                    with open('dict.json', 'w') as js_file:
                        if len(data) > 0:
                            json.dump(data, js_file, indent = 4)
                        else:
                            json.dump(None, js_file)
                    lb = tk.Label(win, text = 'The units was deleted!', bg = '#1b1b1b', font = ('Calibre', 14), fg = '#990F02')
                    lb.place(x = 600, y = 300)
                    lb.after(1500, lambda : lb.destroy())
                    query.delete(0, END)
                    try:
                        word_delete.destroy()
                    except AttributeError:
                        pass

                def get_text():
                    nonlocal item, actual_pract, data, local_words, res, vari, result, pract, varis
                    strings = []
                    for i, vari in enumerate(varis):
                        if vari.get():
                            strings.append(res[i].cget('text'))
                    for x in strings:
                        local_words.update({x : data[x]})
                    strings.clear()
                    try:
                        with open('local_words.json', 'r') as js_file:
                                expressions = json.load(js_file)
                        try:
                            with open('local_words.json', 'r') as js_file:
                                expressions = json.load(js_file)
                                local_words.update(expressions)
                        except TypeError:
                            pass
                        with open('local_words.json', 'w')  as js_file:
                            json.dump(local_words, js_file, indent = 4)
                    except json.decoder.JSONDecodeError or json.JSONDecodeError:
                        with open('local_words.json', 'w') as js_file:
                            json.dump(local_words, js_file, indent = 4)
                    for vari in varis:
                        vari.set(0) 
                    try:
                        pract.destroy()
                    except:
                        pass

                pract = tk.Button(win, text = 'Opt', font = ('Consolas', 11), bg = '#1b1b1b', fg = '#848482', command = get_text)
                pract.place(x = 320, y = 500)
                actual_pract = tk.Button(win, text = 'Practice opted words', font = ('Consolas', 11), bg = '#1b1b1b', fg = '#848482', 
                                        command = local_practice)
                actual_pract.place(x = 600, y = 500)
                word_delete = tk.Button(win, text = 'Delete the words', font = ('Consolas', 11), bg = '#1b1b1b', fg = '#848482',
                                        command = del_words)
                word_delete.place(x = 600, y = 300)
                
            submit = tk.Button(win, text = 'submit', command = gets, bg = '#504A4B', font = ('Consolas', 11), 
                            fg = '#E7DECC')
            submit.place(height = 30, width = 150, x = 375, y = 460)
            def going_back():
                try:
                    with open('local_words.json', 'w') as js_file:
                        json.dump(None, js_file)
                except json.JSONDecodeError:
                    pass
                global inp, search, train
                nonlocal res, query, result, data, res_env, scroll, scrollable_frame, pract, actual_pract, submit, back_button, word_delete
                res.clear()
                enable_button(inp)
                enable_button(train)
                enable_button(search)
                query.destroy()
                try:
                    word_delete.destroy()
                except AttributeError:
                    pass
                try:
                    pract.destroy()
                except AttributeError:
                    pass
                try:
                    scroll.destroy()
                except AttributeError:
                    pass
                try:
                    scrollable_frame.destroy()
                except AttributeError:
                    pass
                try:
                    res_env.destroy()
                except AttributeError:
                    pass
                try:
                    actual_pract.destroy()
                except AttributeError:
                    pass
                for result in res:
                    try:
                        result.destroy()
                    except AttributeError:
                        pass
                back_button.destroy()
                submit.destroy()
            back_button = tk.Button(win, text = 'back', command = going_back, bg = '#504A4B', font = ('Consolas', 11), 
                                    fg = '#E7DECC')
            back_button.place(height = 40, width = 180, x = 360, y = 540)
        def local_practice():
            nonlocal query, actual_pract, result, data, res_env, scroll, scrollable_frame, pract, back_button, submit, word_delete
            query.destroy()
            try:
                word_delete.destroy()
            except AttributeError:
                pass
            try:
                pract.destroy()
            except AttributeError:
                pass
            try:
                scroll.destroy()
            except AttributeError:
                pass
            try:
                scrollable_frame.destroy()
            except AttributeError:
                pass
            try:
                res_env.destroy()
            except AttributeError:
                pass
            try:
                actual_pract.destroy()
            except AttributeError:
                pass
            for result in res:
                try:
                    result.destroy()
                except AttributeError:
                    pass
                back_button.destroy()
                submit.destroy()
            with open('local_words.json', 'r') as js_file:
                datum = json.load(js_file)
                temp_label = tk.Label(win, text = f'{len(datum)} words for practice. Good luck.', font = ('Calibre', 12), bg = '#1b1b1b', 
                                    fg = '#848482', relief = 'groove')
                temp_label.place(height = 30, width = 270, x = 10, y = 10)
                lb = tk.Label(win, text = 'At least 1 word must be opted. Chosen: 0', bg = '#1b1b1b', fg = '#990F02', font = ('Consolas', 12))
                correct = 0
                incorrect = 0
                def stop_loop():
                    with open('local_words.json', 'w') as js_file:
                        json.dump(None, js_file)
                    nonlocal temp_label, english, german, submit, back_button
                    temp_label.destroy()
                    back_button.destroy()
                    german.destroy()
                    submit.destroy()
                    english.destroy()
                    try:
                        temp_label = tk.Label(win, text = f'correct answers: {correct}, incorrect answers: {incorrect}, \n\
                        your precision: {round((correct / (correct + incorrect)) * 100, 1)}%', font = ('Calibre', 11), fg = '#848482', 
                                bg = '#1b1b1b')
                        temp_label.place(height = 80, width = 340, x = 280, y = 400)
                        temp_label.after(5000, lambda: temp_label.destroy())
                    except ZeroDivisionError:
                        pass
                    global inp, search, train
                    enable_button(inp)
                    enable_button(train)
                    enable_button(search)
                back_button = tk.Button(win, text = 'back', command = stop_loop, bg = '#504A4B', font = ('Consolas', 11), 
                                        fg = '#E7DECC')
                back_button.place(height = 40, width = 180, x = 360, y = 540)
                german = tk.Entry(win, bg = '#7F7D9C', font = ('Cascadia code', 11), fg = '#322D31')
                german.place(height = 40, width = 240, x = 470, y = 400)
                var = None
                key, value = random.choice(list(datum.items()))
                english = tk.Label(win, text = value, bg = '#564C4D', font = ('Calibre', 11))
                english.place(height = 40, width = 240, x = 190, y = 400)

                def submission():
                    nonlocal key, value, correct, incorrect, var, english, german
                    english.destroy()
                    var = german.get()
                    if var == key:
                        correct += 1
                        appraisal = tk.Label(win, text = 'Good job!', bg = '#1b1b1b', font = ('Calibre', 18), fg = '#0B6623')
                        appraisal.place(height = 30, width = 120, x = 390, y = 320)
                        win.after(1000, lambda: appraisal.destroy())
                        german.delete('0', 'end')
                    else:
                        incorrect += 1
                        disapproval = tk.Label(win, text = f'No! The correct word was "{key}"!',
                        bg = '#1b1b1b', font = ('Calibre', 18), fg = '#990F02')
                        disapproval.place(height = 50, width = 600, x = 150, y = 320)
                        win.after(5000, lambda: disapproval.destroy())
                        german.delete('0', 'end')
                    key, value = random.choice(list(datum.items()))
                    english = tk.Label(win, text = value, bg = '#564C4D', font = ('Calibre', 11))
                    english.place(height = 40, width = 240, x = 190, y = 400)
                
                submit = tk.Button(win, text = 'Submit your guess', command = submission, bg = '#504A4B', font = ('Consolas', 11), 
                                fg = '#E7DECC')
                submit.place(height = 30, width = 150, x = 375, y = 460)

#buttons
inp = tk.Button(win, text = 'Add new word or phrase', command = input_regime, font = ('Consolas', 11), bg = '#504A4B', 
                fg = '#E7DECC')
train = tk.Button(win, text = 'Practice', command = practice, font = ('Consolas', 11), bg = '#504A4B', 
                  fg = '#E7DECC')
search = tk.Button(win, text = 'Search the word', command = lookup, font = ('Consolas', 11), bg = '#504A4B', 
                   fg = '#E7DECC')
inp.place(height = 60, width = 180, x = 360, y = 20)
train.place(height = 60, width = 180, x = 360, y = 120)
search.place(height = 60, width = 180, x = 360, y = 220)

win.mainloop()
