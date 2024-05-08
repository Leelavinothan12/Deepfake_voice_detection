# deepfake/models.py

from django.db import models

class myfileupload(models.Model):
    myfile = models.FileField()
