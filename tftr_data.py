from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta

class TftrData:
  creation_date: datetime
  last_update: datetime
  viewable_date: datetime
  edit_deadline: datetime
  content: str
  files: dict[str, bytearray]
  
  def __init__(self, creation_date = datetime.now(), last_update = datetime.now(),
               openable_update = datetime.combine(date.today(), time()) + relativedelta(years=1),
               editable_date = datetime.combine(date.today(), time()) + timedelta(weeks=1),
               content = '', files = {}):
    self.creation_date = creation_date
    self.last_update = last_update
    self.viewable_date = openable_update
    self.edit_deadline = editable_date
    self.content = content
    self.files = files
