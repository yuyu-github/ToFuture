from tftr_data import TftrData

def load(path: str = ''):
  if path == '':
    return TftrData()
