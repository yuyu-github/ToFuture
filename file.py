from functools import reduce
from tftr_data import TftrData

def save(tftr_data: TftrData, path: str):
  data = bytes()
  data += b'\x00' + int(tftr_data.creation_date.timestamp()).to_bytes(8, 'big')
  data += b'\x01' + int(tftr_data.last_update.timestamp()).to_bytes(8, 'big')
  data += b'\x02' + int(tftr_data.viewable_date.timestamp()).to_bytes(8, 'big')
  data += b'\x03' + int(tftr_data.edit_deadline.timestamp()).to_bytes(8, 'big')
  content_bytes = tftr_data.content.encode('utf-8')
  data += b'\x04' + len(content_bytes).to_bytes(8, 'big') + content_bytes
  data += b'\x05' + len(tftr_data.files.keys()).to_bytes(2, 'big') + \
    reduce(lambda a, b: a + b, [len(k.encode('utf-8')).to_bytes(2, 'big') + len(v).to_bytes(8, 'big') + k.encode('utf-8') + v for k, v in tftr_data.files.items()], b'')
  
  f = open(path, 'wb')
  f.write(data)
  f.close()

def load(path: str = ''):
  if path == '':
    return TftrData()
