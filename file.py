from datetime import datetime
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
  
  tftr_data = TftrData()
  
  f = open(path, 'rb')
  data = f.read()
  f.close()
  
  i = 0
  data_len = len(data)
  while i < data_len:
    type = data[i]
    match type:
      case 0:
        tftr_data.creation_date = datetime.fromtimestamp(int.from_bytes(data[i+1:i+9], 'big'))
        i += 9
      case 1:
        tftr_data.last_update = datetime.fromtimestamp(int.from_bytes(data[i+1:i+9], 'big'))
        i += 9
      case 2:
        tftr_data.viewable_date = datetime.fromtimestamp(int.from_bytes(data[i+1:i+9], 'big'))
        i += 9
      case 3:
        tftr_data.edit_deadline = datetime.fromtimestamp(int.from_bytes(data[i+1:i+9], 'big'))
        i += 9
      case 4:
        size = int.from_bytes(data[i+1:i+9], 'big')
        i += 9
        tftr_data.content = data[i:i+size].decode('utf-8')
        i += size
      case 5:
        file_count = int.from_bytes(data[i+1:i+3], 'big')
        i += 3

        files: dict[str, bytes] = {}
        for i in range(file_count):
          file_name_len = data[i:i+2]
          i += 2
          file_data_len = data[i:i+8]
          i += 8
          file_name = data[i:i+file_name_len].decode('utf-8')
          i += file_name_len
          file_data = data[i:i+file_data_len]
          i += file_data_len
          files[file_name] = file_data
        
        tftr_data.files = files
      case _:
        return None
  
  return tftr_data
