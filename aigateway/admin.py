from django.contrib import admin

# Register your models here.
from .models import Project, Directory, AiModel, DataSet, File

# Register your models here.
admin.site.register(Project)
admin.site.register(Directory)
admin.site.register(AiModel)
admin.site.register(DataSet)
admin.site.register(File)