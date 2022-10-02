from email import message_from_string
import subprocess
from datetime import datetime, time
from io import BufferedWriter
import tempfile
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from tkinter import simpledialog

from tftr_data import TftrData
from state import State
from file import load, save as save_to_file
from display import State, update
import display

state: State = State.START
tftr_data: TftrData = None
filepath: str = ''
opened_attachments: dict[str, str] = {}

saved = False
def set_saved(value):
  global saved

  if saved != value:
    saved = value

def add_attachment(event = None):
  path = filedialog.askopenfilename(filetypes=[('すべてのファイル', '*.*')])
  if path != '':
    filename = os.path.basename(path)
    f = open(path, 'rb')
    tftr_data.attachments[filename] = f.read()
    f.close()
    display.file_listbox.insert(END, filename)

    set_saved(False)

def delete_attachment(event = None):
  select: str = display.file_listbox.curselection()
  if len(select) > 0:
    if messagebox.askyesno(title='確認', message='ファイルを削除しますか？'):
      tftr_data.attachments.pop(display.file_listbox.get(select[0]))
      display.file_listbox.delete(ACTIVE)

      set_saved(False)

def rename_attachment(event = None):
  select: str = display.file_listbox.curselection()
  if len(select) > 0:
    old_name = display.file_listbox.get(select[0])
    new_name = simpledialog.askstring('名前の変更', '新しい名前を入力してください', initialvalue=old_name)
    if new_name != None and new_name != '':
      tftr_data.attachments[new_name] = tftr_data.attachments.pop(old_name)
      display.file_listbox.insert(select[0], new_name)
      display.file_listbox.delete(select[0] + 1)
      display.file_listbox.select_set(select[0])
      
      set_saved(False)
      
def save_attachment(event = None):
  select: str = display.file_listbox.curselection()
  if len(select) > 0:
    filename = display.file_listbox.get(select[0])
    path = filedialog.asksaveasfilename(initialfile=filename)
    if path != '':
      f = open(path, 'wb')
      f.write(tftr_data.attachments[filename])
      f.close()

def open_attachment(event = None):
  select: str = display.file_listbox.curselection()
  if len(select) > 0:
    fullname = display.file_listbox.get(select[0])
    (name, extentsion) = os.path.splitext(fullname)
    temp_file_name = tempfile.NamedTemporaryFile(prefix=name + '_', suffix=extentsion).name
    f = open(temp_file_name, 'wb')
    f.write(tftr_data.attachments[fullname])
    opened_attachments[fullname] = temp_file_name
    f.close()
    subprocess.Popen(['start', f.name], shell=True)
    
def confirm_save():
  if state == State.START or saved: return True
  
  name = os.path.basename(filepath) if filepath != '' else '新規ファイル'
  answer = messagebox.askyesnocancel(title='確認', message=f"'{name}'は保存されていません。保存しますか？")
  if answer:
    if not save():
      answer = None
  if answer == None:
    return False
  return True

def create_new(event = None):
  global state
  global tftr_data

  if not confirm_save(): return

  tftr_data = load()
  state = State.EDIT
  update(state, tftr_data, root, filepath=filepath, \
    commands={'set_saved': set_saved, 'add_attachment': add_attachment, 'delete_attachment': delete_attachment, 'rename_attachment': rename_attachment, 'save_attachment': save_attachment, 'open_attachment': open_attachment})

  set_saved(False)

def open_file(event = None):
  global state
  global tftr_data
  global filepath

  if not confirm_save(): return
  
  path = filedialog.askopenfilename(filetypes=[('ToFutureファイル', '*.tftr')])
  if path != '' and os.path.isfile(path):
    filepath = path
    tftr_data = load(filepath)

    if tftr_data == None:
      messagebox.showerror(title='エラー', message='ファイルを読み込めませんでした')
    else:
      if datetime.now() <= tftr_data.edit_deadline:
        state = State.EDIT
        update(state, tftr_data, root, filepath=filepath, \
          commands={'set_saved': set_saved, 'add_attachment': add_attachment, 'delete_attachment': delete_attachment, 'rename_attachment': rename_attachment, 'save_attachment': save_attachment, 'open_attachment': open_attachment})
        set_saved(True)
      elif datetime.now() >= tftr_data.viewable_date:
        state = State.VIEW
        update(state, tftr_data, root, filepath=filepath, commands={'save_attachment': save_attachment, 'open_attachment': open_attachment})
        set_saved(True)
      else:
        viewable_date = tftr_data.viewable_date.strftime("%Y/%m/%y %H:%M")
        messagebox.showinfo(title='閲覧不可', message=f'このファイルは{viewable_date}まで閲覧できません')

def save(event = None):
  global tftr_data
  
  if filepath == '':
    return save_as()

  if state == State.EDIT:
    tftr_data.last_update = datetime.now()
    tftr_data.edit_deadline = datetime.combine(display.edit_deadline_date_entry.get_date(), time())
    tftr_data.viewable_date = datetime.combine(display.viewable_date_entry.get_date(), time())
    tftr_data.content = display.content_text.get("1.0", END)
    
    for name, path in opened_attachments.items():
      f = open(path, 'rb')
      tftr_data.attachments[name] = f.read()
      f.close()
  
  result = save_to_file(tftr_data, filepath)
  set_saved(result)
  return result

def save_as(event = None):
  global filepath

  path = filedialog.asksaveasfilename(filetypes=[('ToFutureファイル', '*.tftr')])
  if path != '':
    filepath = path
    return save()
  return False

root = Tk()
root.geometry('1280x720')

def on_close_window():
  if confirm_save():
    root.destroy()
root.protocol('WM_DELETE_WINDOW', on_close_window)

menubar = Menu(root)

menu_file = Menu(menubar, tearoff = False)
menu_file.add_command(label='新規作成', accelerator='Ctrl+N', command=create_new)
menu_file.add_command(label='開く', accelerator='Ctrl+O', command=open_file)
menu_file.add_command(label='上書き保存', accelerator='Ctrl+S', command=save)
menu_file.add_command(label='名前をつけて保存', accelerator='Ctrl+Shift+S', command=save_as)
root.bind_all('<Control-n>', create_new)
root.bind_all('<Control-o>', open_file)
root.bind_all('<Control-s>', save)
root.bind_all('<Control-Shift-S>', save_as)

menubar.add_cascade(label='ファイル', menu=menu_file)
root.config(menu=menubar)

update(state, tftr_data, root, commands={'create_new': create_new, 'open_file': open_file})

root.mainloop()
