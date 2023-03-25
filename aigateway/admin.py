from django.contrib import admin

# Register your models here.
from .models import Project, AiModel

# Register your models here.
admin.site.register(Project)
admin.site.register(AiModel)
