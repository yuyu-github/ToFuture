from enum import Enum
from tkinter import *
from tkinter import ttk
from tkinter import font
from typing import Callable

from tftr_data import TftrData

class ContentType(Enum): 
  START = 1
  CONTENT = 2
  PROJECT_SETTINGS = 3

def update(type: ContentType, tftr_data: TftrData, root: Tk, commands: dict[str, Callable]):
  match type:
    case ContentType.START:
      ttk.Style().configure('big.TButton', font=('System', 20))
      ttk.Button(root, text='新規作成', width=30, padding=[15], style='big.TButton', command=commands['create_new']).pack(anchor='center', expand=0.4)
    case ContentType.CONTENT:
      pass
    case ContentType.PROJECT_SETTINGS:
      pass

def update_content(tftr_data: TftrData):
  pass
