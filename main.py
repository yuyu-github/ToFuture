from glob import glob
import sys
from tkinter import *
from tkinter import filedialog

from tftr_data import TftrData
from file import load
from display import ContentType, update

tftr_data: TftrData = None

def create_new(event = None):
  global tftr_data
  tftr_data = load()
  update(ContentType.EDIT, tftr_data, root)

def open_file(event = None):
  pass

def save(event = None):
  pass

def save_as(event = None):
  pass

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

update(ContentType.START, tftr_data, root, {'create_new': create_new, 'open_file': open_file})

root.mainloop()
