from calendar import calendar
from enum import Enum
from operator import truediv
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from typing import Callable
from tkcalendar import DateEntry

from tftr_data import TftrData

class ContentType(Enum): 
  START = 1
  EDIT = 2
  VIEW = 3
  
class Format(Enum):
  TEXT = 1
  MARKDOWN = 2
  
dataText: scrolledtext.ScrolledText
viewableDateEntry: DateEntry
editDeadlineDateEntry: DateEntry

def update(type: ContentType, tftr_data: TftrData, root: Tk, commands: dict[str, Callable] = {}):
  global dataText
  global viewableDateEntry
  global editDeadlineDateEntry

  for widget in root.winfo_children():
    if widget.widgetName != 'menu':
      widget.destroy()
  
  match type:
    case ContentType.START:
      frame = ttk.Frame(root).pack(padx=50, fill=BOTH)
      ttk.Style().configure('big.TButton', font=('Yu Gothic UI', 15))
      ttk.Button(frame, text='新規作成', width=20, padding=[10], style='big.TButton', command=commands['create_new']).place(anchor=CENTER, relx=0.5, rely=0.5, x=-170)
      ttk.Button(frame, text='ファイルを開く', width=20, padding=[10], style='big.TButton', command=commands['open_file']).place(anchor=CENTER, relx=0.5, rely=0.5, x=170)
    case ContentType.EDIT:
      dataText = scrolledtext.ScrolledText(root, font=('Yu Gothic', 12))
      dataText.grid(column=0, row=0, padx=10, pady=10, sticky=NSEW)
      settingsFrame = ttk.Frame(root)
      settingsFrame.grid(column=1, row=0, padx=10, pady=15, sticky=NSEW)
      root.rowconfigure(0, weight=1)
      root.columnconfigure(0, weight=2)
      root.columnconfigure(1, weight=1, minsize=250)
      
      Label(settingsFrame, text='閲覧可能日').grid(column=0, row=0, sticky=W)
      viewableDateEntry = DateEntry(settingsFrame, showweeknumbers=False)
      viewableDateEntry.grid(column=1, row=0, padx=10, pady=2, sticky=EW) 
      Label(settingsFrame, text='編集期限').grid(column=0, row=1, sticky=W)
      editDeadlineDateEntry = DateEntry(settingsFrame, showweeknumbers=False)
      editDeadlineDateEntry.grid(column=1, row=1, padx=10, pady=2, sticky=EW)
      settingsFrame.columnconfigure(1, weight=1)
    case ContentType.VIEW:
      dataText = scrolledtext.ScrolledText(root, font=('Yu Gothic', 12))
      dataText.grid(column=0, row=0, padx=10, pady=10, sticky=NSEW)
      replyFrame = ttk.Frame(root)
      replyFrame.grid(column=1, row=0, padx=10, pady=15, sticky=NSEW)
      root.rowconfigure(0, weight=1)
      root.columnconfigure(0, weight=4)
      root.columnconfigure(1, weight=3, minsize=350)

def update_content(tftr_data: TftrData):
  pass
