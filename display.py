import os
import re
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.font import Font
from turtle import back, width
from typing import Callable
from tkcalendar import DateEntry

from state import State
from tftr_data import TftrData
  
content_text: scrolledtext.ScrolledText
viewable_date_entry: DateEntry
edit_deadline_date_entry: DateEntry
file_listbox: Listbox

def update(type: State, tftr_data: TftrData, root: Tk, *, commands: dict[str, Callable] = {}):
  global content_text
  global viewable_date_entry
  global edit_deadline_date_entry
  global file_listbox
  
  for widget in root.winfo_children():
    if widget.widgetName == 'menu':
      menu_file = widget.winfo_children()[widget.index('ファイル') - 1]
      
      menu_file.entryconfig(menu_file.index('上書き保存'), state='normal')
      menu_file.entryconfig(menu_file.index('名前をつけて保存'), state='normal')
      
      match type:
        case State.START:
          menu_file.entryconfig(menu_file.index('上書き保存'), state='disabled')
          menu_file.entryconfig(menu_file.index('名前をつけて保存'), state='disabled')
    else:
      widget.destroy()
  
  match type:
    case State.START:
      root.title('ToFuture')
      
      frame = ttk.Frame(root).pack(padx=50, fill=BOTH)
      ttk.Style().configure('big.TButton', font=('Yu Gothic UI', 15))
      ttk.Button(frame, text='新規作成', width=20, padding=[10], style='big.TButton', command=commands['create_new']).place(anchor=CENTER, relx=0.5, rely=0.5, x=-170)
      ttk.Button(frame, text='ファイルを開く', width=20, padding=[10], style='big.TButton', command=commands['open_file']).place(anchor=CENTER, relx=0.5, rely=0.5, x=170)
    case State.EDIT:
      def on_key_press(event: Event):
        if not (event.keysym.startswith('Control') or event.keysym.startswith('Shift') or event.keysym.startswith('Alt') or event.keysym.startswith('Win') or event.state > 1) or \
          (event.state == 4 and re.match(r'^[xvXV]$', event.keysym)):
          commands['set_saved'](False)
      
      content_text = scrolledtext.ScrolledText(root, font=('Yu Gothic', 12))
      content_text.insert('1.0', tftr_data.content)
      content_text.grid(column=0, row=0, rowspan=3, padx=10, pady=10, sticky=NSEW)
      content_text.bind('<KeyPress>', on_key_press)
      settings_frame = Frame(root)
      settings_frame.grid(column=1, row=0, padx=(0, 10), pady=(15, 10), sticky=NSEW)
      file_control_frame = Frame(root)
      file_control_frame.grid(column=1, row=1, padx=(0, 10), pady=5, sticky=NSEW)
      file_list_frame = Frame(root)
      file_list_frame.grid(column=1, row=2, padx=(0, 10), pady=(0, 20), sticky=NSEW)
      root.rowconfigure(2, weight=1)
      root.columnconfigure(0, weight=2)
      root.columnconfigure(1, weight=1, minsize=250)
      
      Label(settings_frame, text='閲覧可能日').grid(column=0, row=0, sticky=W)
      viewable_date_entry = DateEntry(settings_frame, showweeknumbers=False, year=tftr_data.viewable_date.year, month=tftr_data.viewable_date.month, day=tftr_data.viewable_date.day)
      viewable_date_entry.grid(column=1, row=0, padx=10, pady=2, sticky=EW) 
      viewable_date_entry.bind('<KeyPress>', on_key_press)
      viewable_date_entry.bind('<<DateEntrySelected>>', on_key_press)
      Label(settings_frame, text='編集期限').grid(column=0, row=1, sticky=W)
      edit_deadline_date_entry = DateEntry(settings_frame, showweeknumbers=False, year=tftr_data.edit_deadline.year, month=tftr_data.edit_deadline.month, day=tftr_data.edit_deadline.day)
      edit_deadline_date_entry.grid(column=1, row=1, padx=10, pady=2, sticky=EW)
      edit_deadline_date_entry.bind('<KeyPress>', on_key_press)
      edit_deadline_date_entry.bind('<<DateEntrySelected>>', on_key_press)
      settings_frame.columnconfigure(1, weight=1)
      
      add_file_button = ttk.Button(file_control_frame, text='ファイルを追加', command=commands['add_attachment'])
      add_file_button.grid(column=0, row=0, sticky=EW)
      delete_file_button = ttk.Button(file_control_frame, text='ファイルを削除', command=commands['delete_attachment'])
      delete_file_button.grid(column=1, row=0, sticky=EW)
      rename_file_button = ttk.Button(file_control_frame, text='名前を変更', command=commands['rename_attachment'])
      rename_file_button.grid(column=2, row=0, sticky=EW)
      open_file_button = ttk.Button(file_control_frame, text='ファイルを開く', command=commands['open_attachment'])
      open_file_button.grid(column=0, row=1, sticky=EW)
      save_file_button = ttk.Button(file_control_frame, text='ファイルを保存', command=commands['save_attachment'])
      save_file_button.grid(column=1, row=1, sticky=EW)
      file_control_frame.columnconfigure(0, weight=1)
      file_control_frame.columnconfigure(1, weight=1)
      file_control_frame.columnconfigure(2, weight=1)
      
      file_listbox = Listbox(file_list_frame, font=('Yu Gothic UI', 15), listvariable=StringVar(value=tuple(tftr_data.attachments.keys())), activestyle=NONE, selectbackground='skyblue', selectforeground='black', highlightthickness=0)
      file_listbox.grid(column=0, row=0, sticky=NSEW)
      file_list_scrollbar = ttk.Scrollbar(file_list_frame, orient=VERTICAL, command=file_listbox.yview)
      file_list_scrollbar.grid(column=1, row=0, sticky=NS)
      file_listbox.config(yscrollcommand=file_list_scrollbar.set)
      file_listbox.bind_all('<MouseWheel>', lambda self: file_listbox.yview_scroll((self.delta < 0) - (self.delta > 0), 'units'))
      file_list_frame.rowconfigure(0, weight=1)
      file_list_frame.columnconfigure(0, weight=1)
    case State.VIEW:      
      content_text = scrolledtext.ScrolledText(root, font=('Yu Gothic', 12))
      content_text.insert('1.0', tftr_data.content)
      content_text.config(state='disabled')
      content_text.grid(column=0, row=0, rowspan=3, padx=10, pady=10, sticky=NSEW)
      reply_frame = ttk.Frame(root)
      reply_frame.grid(column=1, row=0, padx=10, pady=15, sticky=NSEW)
      file_control_frame = Frame(root)
      file_control_frame.grid(column=1, row=1, padx=(0, 10), pady=5, sticky=NSEW)
      file_list_frame = Frame(root)
      file_list_frame.grid(column=1, row=2, padx=(0, 10), pady=(0, 20), sticky=NSEW)
      root.rowconfigure(2, weight=1)
      root.columnconfigure(0, weight=4)
      root.columnconfigure(1, weight=3, minsize=350)
      
      open_file_button = ttk.Button(file_control_frame, text='ファイルを開く', command=commands['open_attachment'])
      open_file_button.grid(column=0, row=1, sticky=EW)
      save_file_button = ttk.Button(file_control_frame, text='ファイルを保存', command=commands['save_attachment'])
      save_file_button.grid(column=1, row=1, sticky=EW)
      file_control_frame.columnconfigure(0, weight=1)
      file_control_frame.columnconfigure(1, weight=1)
      
      file_listbox = Listbox(file_list_frame, font=('Yu Gothic UI', 15), listvariable=StringVar(value=tuple(tftr_data.attachments.keys())), activestyle=NONE, selectbackground='skyblue', selectforeground='black', highlightthickness=0)
      file_listbox.grid(column=0, row=0, sticky=NSEW)
      file_list_scrollbar = ttk.Scrollbar(file_list_frame, orient=VERTICAL, command=file_listbox.yview)
      file_list_scrollbar.grid(column=1, row=0, sticky=NS)
      file_listbox.config(yscrollcommand=file_list_scrollbar.set)
      file_listbox.bind_all('<MouseWheel>', lambda self: file_listbox.yview_scroll((self.delta < 0) - (self.delta > 0), 'units'))
      file_list_frame.rowconfigure(0, weight=1)
      file_list_frame.columnconfigure(0, weight=1)
