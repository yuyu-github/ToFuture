from glob import glob
import sys
from tkinter import *

from tftr_data import TftrData
from file import load
from display import ContentType, update, update_content

tftr_data: TftrData = None

def create_new(event = None):
  global tftr_data
  tftr_data = load()
  update(ContentType.EDIT, tftr_data, root)

def file_open(event = None):
  pass

def save(event = None):
  pass

def save_as(event = None):
  pass

def project_settings(event = None):
  pass

root = Tk()
root.title('ToFuture')
root.geometry('1280x720')

menubar = Menu(root)

menu_file = Menu(menubar, tearoff = False)
menu_file.add_command(label='新規作成', accelerator='Ctrl+N', command=create_new)
menu_file.add_command(label='開く', accelerator='Ctrl+O', command=file_open)
menu_file.add_command(label='上書き保存', accelerator='Ctrl+S', command=save)
menu_file.add_command(label='名前をつけて保存', accelerator='Ctrl+Shift+S', command=save_as)
menu_file.bind_all('<Control-n>', create_new)
menu_file.bind_all('<Control-o>', file_open)
menu_file.bind_all('<Control-s>', save)
menu_file.bind_all('<Control-Shift-S>', save_as)

menu_edit = Menu(menubar, tearoff=False)
menu_edit.add_command(label='ファイル設定', accelerator='Ctrl+P', command=project_settings)
menu_edit.bind_all('<Control-p>', project_settings)

menubar.add_cascade(label='ファイル', menu=menu_file)
menubar.add_cascade(label='編集', menu=menu_edit)
root.config(menu=menubar)

update(ContentType.START, tftr_data, root, {'create_new': create_new})

root.mainloop()
