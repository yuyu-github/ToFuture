from datetime import datetime, time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

from tftr_data import TftrData
from state import State
from file import load, save as save_to_file
from display import State, update
import display

state: State = State.START
tftr_data: TftrData = None
filepath: str = ''

def create_new(event = None):
  global tftr_data
  tftr_data = load()
  state = State.EDIT
  update(state, tftr_data, root)

def open_file(event = None):
  global tftr_data
  global filepath

  path = filedialog.askopenfilename(filetypes=[('ToFutureファイル', '*.tftr')])
  if path != '' and os.path.isfile(path):
    filepath = path
    tftr_data = load(filepath)

    if tftr_data == None:
      messagebox.showerror(title='エラー', message='ファイルを読み込めませんでした')
    else:
      if datetime.now() <= tftr_data.edit_deadline:
        state = State.EDIT
        update(state, tftr_data, root)
      elif datetime.now() >= tftr_data.viewable_date:
        state = State.VIEW
        update(state, tftr_data, root)
      else:
        viewable_date = tftr_data.viewable_date.strftime("%y/%m/%y %H:%M:%S")
        messagebox.showinfo(title='閲覧不可', message=f'このファイルは{viewable_date}まで閲覧できません')

def save(event = None):
  global tftr_data
  
  if filepath == '':
    save_as()
    return

  if state == State.EDIT:
    tftr_data.last_update = datetime.now()
    tftr_data.edit_deadline = datetime.combine(display.editDeadlineDateEntry.get_date(), time())
    tftr_data.viewable_date = datetime.combine(display.viewableDateEntry.get_date(), time())
    tftr_data.content = display.contentText.get("1.0", END)
  
  save_to_file(tftr_data, filepath)

def save_as(event = None):
  global filepath

  path = filedialog.asksaveasfilename(filetypes=[('ToFutureファイル', '*.tftr')])
  if path != '':
    filepath = path
    save()

root = Tk()
root.title('ToFuture')
root.geometry('1280x720')

menubar = Menu(root)

menu_file = Menu(menubar, tearoff = False)
menu_file.add_command(label='新規作成', accelerator='Ctrl+N', command=create_new)
menu_file.add_command(label='開く', accelerator='Ctrl+O', command=open_file)
menu_file.add_command(label='上書き保存', accelerator='Ctrl+S', command=save)
menu_file.add_command(label='名前をつけて保存', accelerator='Ctrl+Shift+S', command=save_as)
menu_file.bind_all('<Control-n>', create_new)
menu_file.bind_all('<Control-o>', open_file)
menu_file.bind_all('<Control-s>', save)
menu_file.bind_all('<Control-Shift-S>', save_as)

menubar.add_cascade(label='ファイル', menu=menu_file)
root.config(menu=menubar)

update(state, tftr_data, root, {'create_new': create_new, 'open_file': open_file})

root.mainloop()
