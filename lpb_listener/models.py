from django.db import models

# Create your models here.

class Stream(models.Field):

  def __init__(self):
    super(Stream, self).__init__()

  description = 'A comma seperated 2-byte bytestream'

  def __init__(self, *args, **kwargs):
    kwargs['max_length'] = 150
    super(Stream, self).__init__(*args, **kwargs)

  def deconstruct(self):
    name, path, args, kwargs = super(HandField, self).deconstruct()
    del kwargs["max_length"]
    return name, path, args, kwargs




class LPBMessage(models.Model):
  message = models.CommaSeparatedIntegerField(max_length=200)
  timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
