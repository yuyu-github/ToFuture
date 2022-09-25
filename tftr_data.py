from datetime import date, datetime

class TftrData:
  creation_date: datetime
  last_update: datetime
  viewable_date: datetime
  edit_deadline: datetime
  content: str
  files: dict[str, bytearray]
  
  def __init__(self, creation_date = datetime.now(), last_update = datetime.now(), openable_update = None, editable_date = None, content = '', files = {}):
    self.creation_date = creation_date
    self.last_update = last_update
    self.viewable_date = openable_update
    self.edit_deadline = editable_date
    self.content = content
    self.files = files
