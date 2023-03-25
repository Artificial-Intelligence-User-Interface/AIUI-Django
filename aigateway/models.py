from django.db import models

# def get_directory_path(instance, filename):
#     return f"/aigateway/{instance.directory.name}/{filename}"
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=60)
    created = models.IntegerField()
    last_updated = models.IntegerField()
    dataset = models.CharField(max_length=200)

# class Directory(models.Model):
#     name = models.CharField(max_length=20)

class AiModel(models.Model):
    name = models.CharField(max_length=60)
    typemodel = models.CharField(max_length=30)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    #config = models.CharField(max_length=200)
    model = models.CharField(max_length=200)

# class DataSet(models.Model):
#     name = models.CharField(max_length=60)
#     directory = models.IntegerField()
#     project = models.ForeignKey('Project', on_delete=models.CASCADE)


# class File (models.Model):
#     name = models.CharField(max_length=20)
#     directory = models.ForeignKey('Directory', on_delete=models.CASCADE)
#     file = models.FileField(
#         upload_to=get_directory_path,
#         blank=True,
#     )
