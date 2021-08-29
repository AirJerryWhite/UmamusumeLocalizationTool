import json
import re
import tkinter
import tkinter.filedialog
import tkinter.scrolledtext
import tkinter.messagebox
import os
import os.path
from tkinter import END

root_path = os.getcwd()
print(root_path)


def filename(path: str):
    if path.find('/'):
        str_cache = path.rsplit('/')
    else:
        str_cache = path.rsplit('\\')
    str_cache = str_cache[len(str_cache) - 1]
    str_cache = str_cache.rsplit('.')[0]
    return str_cache


def unification(path:str):
    data = ''
    reg = "\"[a-zA-Z]\": \"describe\", "
    with open(path, 'r', encoding='utf-8') as fp:
        data = fp.read()
    data = re.sub(reg, "", data, 5)
    data = data.replace("{\"", "{\n    \"", 1)
    data = data.replace("\", ", "\",\n    ")
    data = data.replace("\"}", "\"\n}")
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(data)


def spawnDict(path_origin: str, path_translate: str):
    path_dict = './source_file/dict/' + filename(path_origin) + '_dict.json'
    Dict = dict.fromkeys('origin', 'translate')
    with open(path_origin, 'r', encoding='utf-8') as fp:
        original_data = json.load(fp)
    with open(path_translate, 'r', encoding='utf-8') as fp:
        translated_data = json.load(fp)
    for key in original_data.keys():
        if original_data.get(key) != translated_data.get(key):
            Dict.setdefault(original_data.get(key), translated_data.get(key))
    with open(path_dict, 'w', encoding='utf-8') as fp:
        json.dump(Dict, fp, ensure_ascii=False)
    unification(path_dict)
    print("Spawn Dict successfully!\nDict at "+path_dict)


def TranslateOrigin(path_origin: str):
    path_dict = './source_file/dict/' + filename(path_origin) + '_dict.json'
    path_all = './source_file/output/' + filename(path_origin) + '_all.json'
    path_translated = './source_file/output/' + filename(path_origin) + '.json'
    path_neededTranslated = './source_file/output/neededTranslate_' + filename(path_origin) + '.json'
    translated_all = dict.fromkeys('memory', 'describe')
    translated_data = dict.fromkeys('memory', 'describe')
    neededTranslated_data = dict.fromkeys('memory', 'describe')
    with open(path_origin, 'r', encoding='utf-8') as fp:
        original_data = json.load(fp)
    with open(path_dict, 'r', encoding='utf-8') as fp:
        dict_data = json.load(fp)
    for key in original_data.keys():
        if dict_data.get(original_data.get(key)):
            translated_data.setdefault(key, dict_data.get(original_data.get(key)))
        else:
            neededTranslated_data.setdefault(key, original_data.get(key))
    for key in original_data.keys():
        if dict_data.get(original_data.get(key)):
            translated_all.setdefault(key, dict_data.get(original_data.get(key)))
        else:
            translated_all.setdefault(key, original_data.get(key))
    with open(path_translated, 'w', encoding='utf-8') as fp:
        json.dump(translated_data, fp, ensure_ascii=False)
    unification(path_translated)
    with open(path_neededTranslated, 'w', encoding='utf-8') as fp:
        json.dump(neededTranslated_data, fp, ensure_ascii=False)
    unification(path_neededTranslated)
    with open(path_all, 'w', encoding='utf-8') as fp:
        json.dump(translated_all, fp, ensure_ascii=False)
    unification(path_all)


app = tkinter.Tk()
app.title('i18upgrade')
app['width'] = 400
app['height'] = 300

textChanged = tkinter.IntVar(value=0)

menu = tkinter.Menu(app)
submenu = tkinter.Menu(menu, tearoff=0)
photo = tkinter.PhotoImage(file='./source_file/resource/picture.png')
logo = tkinter.Label(app, compound='center', image=photo)
logo.pack()


def fun_SpawnDict():
    window = tkinter.Tk()
    window.title('SpawnDict')
    window['width'] = 400
    window['height'] = 150
    frame = tkinter.Frame(window)
    frame['width'] = 400
    frame['height'] = 150

    yesno = tkinter.messagebox.askquestion(title='输入设置', message='是否要一次性进行多个语言文件的字典文件生成')
    if yesno == 'no':
        path_origin = ' '
        path_translate = ' '
        input_path = ' '

        def Input_origin():
            nonlocal input_path
            nonlocal path_origin
            input_path = tkinter.filedialog.askopenfilename()
            path_origin = input_path
            InputBox_origin_path.delete(0, END)
            InputBox_origin_path.insert(0, path_origin)

        def Input_translate():
            nonlocal input_path
            nonlocal path_translate
            input_path = tkinter.filedialog.askopenfilename()
            path_translate = input_path
            InputBox_translate_path.delete(0, END)
            InputBox_translate_path.insert(0, path_translate)

        fail = tkinter.Label(frame, text='参数错误', fg='red')
        Success = tkinter.Label(frame, text='生成字典文件成功', fg='red')
        origin = tkinter.Label(frame, text='原始语言文件:')
        InputBox_origin_path = tkinter.Entry(frame, text=' ', bg='white', fg='black', width=30)
        origin_browse = tkinter.Button(frame, text='浏览', command=Input_origin)
        translate = tkinter.Label(frame, text='已翻译的语言文件:')
        InputBox_translate_path = tkinter.Entry(frame, text=' ', bg='white', fg='black', width=30)
        translate_browse = tkinter.Button(frame, text='浏览', command=Input_translate)

        origin.place(x=30, y=10)
        InputBox_origin_path.place(x=110, y=10)
        origin_browse.place(x=330, y=5)
        translate.place(x=6, y=40)
        InputBox_translate_path.place(x=110, y=40)
        translate_browse.place(x=330, y=35)

        def confirm():
            if path_origin != ' ' and path_translate != ' ':
                spawnDict(path_origin, path_translate)
                Success.place(relx=0.35, rely=0.43)
            else:
                fail.place(relx=0.4, rely=0.43)

        def close():
            window.destroy()

        confirm = tkinter.Button(frame, text='确认', command=confirm)
        cancel = tkinter.Button(frame, text='取消', command=close)
        confirm.place(relx=0.35, rely=0.6)
        cancel.place(relx=0.60, rely=0.6)
    else:
        Notice = tkinter.Label(frame, text='这个功能还在开发中...', fg='red')
        Notice.place(relx=0.30, rely=0.4)

        def close():
            window.destroy()

        cancel = tkinter.Button(frame, text='取消', command=close)
        cancel.place(relx=0.45, rely=0.6)
    frame.pack()
    window.mainloop()


submenu.add_command(label='生成字典文件', command=fun_SpawnDict)
submenu.add_separator()


def Close():
    app.destroy()


def fun_translate():
    window = tkinter.Tk()
    window.title('Translate')
    window['width'] = 400
    window['height'] = 110
    frame = tkinter.Frame(window)
    frame['width'] = 400
    frame['height'] = 110

    path_origin = ''
    origin = tkinter.Label(frame, text='原始语言文件:')
    InputBox_origin_path = tkinter.Entry(frame, text='', bg='white', fg='black', width=30)

    def Input_Origin():
        nonlocal path_origin
        path_origin = tkinter.filedialog.askopenfilename()
        InputBox_origin_path.delete(0, END)
        InputBox_origin_path.insert(0, path_origin)

    origin_browse = tkinter.Button(frame, text='浏览', command=Input_Origin)
    error = tkinter.Label()
    success = tkinter.Label()
    InputBox_origin_path.place(x=95, y=15)
    origin_browse.place(x=315, y=10)
    origin.place(x=15, y=15)

    def confirm():
        nonlocal error
        nonlocal success
        if os.path.isfile('./source_file/dict/' + filename(path_origin) + '_dict.json'):
            success = tkinter.Label(frame, text='导出语言文件成功\n导出目录位于.\\source_file\\ouput')
            if 'error' in dir():
                error.destroy()
            TranslateOrigin(path_origin)
            success.place(x=110, y=35)
        else:
            if 'success' in dir():
                success.destroy()
            error = tkinter.Label(frame, text='该语言文件' + filename(path_origin) + '的字典文件不存在无法导出。')
            error.place(x=85, y=35)

    def close():
        window.destroy()

    confirm = tkinter.Button(frame, text='确认', command=confirm)
    cancel = tkinter.Button(frame, text='取消', command=close)
    confirm.place(relx=0.35, rely=0.7)
    cancel.place(relx=0.60, rely=0.7)

    frame.pack()
    window.mainloop()


submenu.add_command(label='翻译原始语言文件', command=fun_translate)
submenu.add_separator()
submenu.add_command(label='关闭', command=Close)
menu.add_cascade(label='功能', menu=submenu)
app.config(menu=menu)
app.mainloop()
