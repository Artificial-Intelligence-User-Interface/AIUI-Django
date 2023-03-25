from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Project, Directory, AiModel, DataSet, File
from datetime import datetime
from django.conf import settings
import os
# Create your views here.

def proj(request):
    # print(request)
    if request.method == 'GET':
        response = {}
        response['projects'] = []
        if request.GET.get('id', False):
            project = Project.objects.filter(id=int(request.GET['id'])).first()
            projAttr = {}
            projAttr['name'] = project.name
            projAttr['created'] = project.created
            projAttr['last_updated'] = project.last_updated
            projAttr['id'] = project.pk
            response['projects'].append(projAttr)
        else:
            projects = Project.objects.all()
            for project in projects:
                projAttr = {}
                projAttr['name'] = project.name
                projAttr['created'] = project.created
                projAttr['last_updated'] = project.last_updated
                projAttr['id'] = project.pk
                response['projects'].append(projAttr)
        return JsonResponse(response)
    elif request.method == "POST":
        name = json.loads(request.body)['name']
        # print(request.POST)
        project = Project(name=name, created=str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S')), last_updated=str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S')))
        project.save()
        return JsonResponse({'projects':[{'id':project.pk,'name':name,'created':project.created,'last_updated':project.last_updated}]})

    

def aimodel(request):
    # name = models.CharField(max_length=60)
    # typemodel = models.CharField(max_length=30)
    # project = models.ForeignKey('Project', on_delete=models.CASCADE)
    # presets = models.CharField(max_length=200)
    # config = models.CharField(max_length=200)
    # directory = models.ForeignKey('Directory', on_delete=models.CASCADE)
    if request.method == 'POST':
        name = request.POST['name']
        typemodel = request.POST['model_type']
        project = Project.objects.get(id=int(request.POST['project_id']))
        # f=os.path.join( settings.STATIC_ROOT, 'myApp/myData.json' ) if collectstatic invoked
        directory = Directory(name=request.POST['name'])
        directory.save()
        aimodel = AiModel(name=name, typemodel=typemodel,project=project,directory=directory)
        aimodel.save()
        return JsonResponse({'models':[{'id':aimodel.pk,'name':request.POST['name'],'created':project.created,'last_updated':project.last_updated}]})
    elif request.method == 'GET':
        response = {}
        response['models'] = []
        project = Project.objects.get(id=int(request.POST['project_id']))
        for model in project.aimodel_set.all():
            modelAttr = {}
            modelAttr['name'] = model.name
            modelAttr['type'] = model.type
            modelAttr['project'] = project.pk
            modelAttr['id'] = model.pk
            response['models'].append(modelAttr)
        return JsonResponse(response)
    
def modelconfig(request):
    if request.method == 'GET':
        model = AiModel.objects.get(id=int(request.GET['model_id']))
        # check to see if there is a new config or just a preset, return based on that
        config = os.path.join( settings.BASE_DIR, f"myApp/static/myApp/{model.typemodel}/{model.name}.json")
        if (os.path.exists(config)):
            with open(config) as f:
                config = json.load(f)
            return JsonResponse(config)
        else:
            presets = os.path.join( settings.BASE_DIR, f"myApp/static/myApp/{model.typemodel}/presets.json")
            with open(presets) as f:
                presets = json.load(f)
            return JsonResponse(presets)
    else:
        #open the file (create if non existant) for the model, paste the json config
        pass
    
        


