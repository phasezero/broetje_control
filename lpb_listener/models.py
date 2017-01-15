from django.db import models

# Create your models here.
class Rawdata(models.Model):
  timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
  data = model.CharField(validators=[validate_comma_separated_integer_list])
  
  def __init__(self):
    super(Rawdata, self).__init__()

  def get_timestamp(self):
      return self.__timestamp


  def get_data(self):
      return self.__data


  def set_timestamp(self, value):
      self.__timestamp = value


  def set_data(self, value):
      self.__data = value


  def del_timestamp(self):
      del self.__timestamp


  def del_data(self):
      del self.__data

  timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")
  data = property(get_data, set_data, del_data, "data's docstring")
