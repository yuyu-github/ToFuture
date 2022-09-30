from datetime import datetime
from functools import reduce
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from tftr_data import TftrData
from file import load
from display import ContentType, update
import display

tftr_data: TftrData = None
filepath: str = ''

def create_new(event = None):
  global tftr_data
  tftr_data = load()
  update(ContentType.EDIT, tftr_data, root)

def open_file(event = None):
  pass

def save(event = None):
  global tftr_data
  
  if filepath == '':
    save_as()
    return

  tftr_data.last_update = datetime.now()
  tftr_data.content = display.contentText.get("1.0", END)
  
  data = bytes()
  data += b'\x00' + int(tftr_data.creation_date.timestamp()).to_bytes(8, 'big')
  data += b'\x01' + int(tftr_data.last_update.timestamp()).to_bytes(8, 'big')
  data += b'\x02' + int(tftr_data.viewable_date.timestamp()).to_bytes(8, 'big')
  data += b'\x03' + int(tftr_data.edit_deadline.timestamp()).to_bytes(8, 'big')
  content_bytes = tftr_data.content.encode('utf-8')
  data += b'\x04' + len(content_bytes).to_bytes(8, 'big') + content_bytes
  data += b'\x05' + len(tftr_data.files.keys()).to_bytes(2, 'big') + \
    reduce(lambda a, b: a + b, [len(k.encode('utf-8')).to_bytes(2, 'big') + len(v).to_bytes(8, 'big') + k.encode('utf-8') + v for k, v in tftr_data.files.items()])
  
  f = open(filepath, 'wb')
  f.write(data)
  f.close()

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

update(ContentType.START, tftr_data, root, {'create_new': create_new, 'open_file': open_file})

root.mainloop()
