from django.db import models

def get_directory_path(instance, filename):
    return f"/aigateway/{filename}"
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=60)
    created = models.CharField(max_length=60)
    last_updated = models.CharField(max_length=60)

class Directory(models.Model):
    name = models.CharField(max_length=20)

class AiModel(models.Model):
    name = models.CharField(max_length=60)
    typemodel = models.CharField(max_length=30)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    #config = models.CharField(max_length=200)
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE)

class DataSet(models.Model):
    name = models.CharField(max_length=60)
    directory = models.CharField(max_length=200)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)


class File (models.Model):
    name = models.CharField(max_length=20)
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=get_directory_path,
        blank=True,
    )