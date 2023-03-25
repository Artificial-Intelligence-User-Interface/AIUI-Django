from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Project, AiModel
from datetime import datetime
from django.conf import settings
import os
import time
from .forms import UploadDatasetForm
from .SvmModel import trainSVM,runSVM
from .MLPClassifierModel import trainMLP, runMLP
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
        now = round(time.time() * 1000)
        project = Project(name=name, created=now, last_updated=now, dataset='')
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
        postDict = json.loads(request.body)
        name = postDict['name']
        typemodel = postDict['model_type']
        project = Project.objects.get(id=int(postDict['project_id']))
        # f=os.path.join( settings.STATIC_ROOT, 'myApp/myData.json' ) if collectstatic invoked
        aimodel = AiModel(name=name, typemodel=typemodel,project=project,model='')
        aimodel.save()
        return JsonResponse({'models':[{'model_id':aimodel.pk,'name':postDict['name'],'type_model':typemodel,'project_id':project.pk}]})
    elif request.method == 'GET':
        response = {}
        response['models'] = []
        project = Project.objects.get(id=int(request.GET['project_id']))
        for model in project.aimodel_set.all():
            modelAttr = {}
            modelAttr['name'] = model.name
            modelAttr['type_model'] = model.typemodel
            modelAttr['project_id'] = project.pk
            modelAttr['model_id'] = model.pk
            response['models'].append(modelAttr)
        return JsonResponse(response)

# def config(request):
#     if request.method == 'GET':
#         model = AiModel.objects.get(id=int(request.GET['model_id']))
#         # check to see if there is a new config or just a preset, return based on that
#         # config = os.path.join( settings.BASE_DIR, f"myApp/static/myApp/{model.typemodel}/{model.name}.json")
#         # if (os.path.exists(config)):
#         #     with open(config) as f:
#         #         config = json.load(f)
#         #     return JsonResponse(config)
#         # else:
#         #     presets = os.path.join( settings.BASE_DIR, f"myApp/static/myApp/{model.typemodel}/presets.json")
#         #     with open(presets) as f:
#         #         presets = json.load(f)
#         #     return JsonResponse(presets)
#         presets = os.path.join( settings.BASE_DIR, f"myApp/static/myApp/{model.typemodel}/presets.json")
#         with open(presets) as f:
#             presets = json.load(f)
#         return JsonResponse(presets)
#     else:
#         #open the file (create if non existant) for the model, paste the json config
#         pass
def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def dataset(request):
    if request.method == 'POST':
        
        post = UploadDatasetForm(request.POST, request.FILES)
        project = Project.objects.get(id=int(post["project_id"].value()))
        pathDir = os.path.join( settings.BASE_DIR, f"aigateway/static/aigateway/{project.name}/")
        if(not os.path.exists(pathDir)):
            os.makedirs(pathDir)
        pathDir += "dataset.arff"
        project.dataset = pathDir
        project.save()
        handle_uploaded_file(request.FILES['file'], pathDir)
        return JsonResponse({'project_id':project.pk})

def train(request):
    # needs dataset,params,aimodel
    # update location for aimodel obj to the loc of model file
    post = json.loads(request.body)
    project = Project.objects.get(id=int(post['project_id']))
    model = AiModel.objects.get(id=int(post['model_id']))
    accuracy, pathDir = None, None, None
    if model.typemodel == 'svg':
        train = trainSVM(project.dataset,model.name,project.name)
        accuracy, pathDir = train[0], train[1]
    elif model.typemodel == 'mlp':
        train = trainMLP(project.dataset,model.name,project.name)
        accuracy, pathDir = train[0], train[1]
    model.model = pathDir
    return JsonResponse({'project_id':project.pk, 'model_id':model.pk, 'accuracy': accuracy, 'precision':precision})


def output(request):
    #get the params
    #run model
    #return output
    post = json.loads(request.body)
    data = post['parameters']
    project = Project.objects.get(id=int(post['project_id']))
    model = AiModel.objects.get(id=int(post['model_id']))
    pathDir = model.model
    result = None
    if model.typemodel == 'svg':
        result = runSVM(data, pathDir)
        pass
    elif model.typemodel == 'mlp':
        result = runMLP(data, pathDir)
    return JsonResponse({'project_id':project.pk, 'model_id':model.pk, 'result': result})
