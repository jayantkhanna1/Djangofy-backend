from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from .makesettings import CreateSettings
from .makeurls import CreateUrls
from .makeviews import CreateViews
from .makemodels import CreateModels
from .makeserializers import CreateSerializers
from .makeadmin import CreateAdmin
from .makerequirements import CreateRequirements
import shutil
from django.http import HttpResponse


def createAllFiles(project_name,apps,rest_framework):
    try:
        os.system("cd sandbox && django-admin startproject "+project_name)
        
        # create a .env file in project directory
        env_file = open("sandbox/"+project_name+"/.env","w")
        env_file.close()
        
        # Now adding gitignore for .env
        gitignore_file = open("sandbox/"+project_name+"/.gitignore","w")
        gitignore_file.write("*.env")
        gitignore_file.close()

        # Creating apps
        for app in apps:
            os.system("cd sandbox/"+project_name+" && python manage.py startapp "+app)

        # Creating static and templates folder
        os.system("cd sandbox/"+project_name+" && mkdir static")
        os.system("cd sandbox/"+project_name+" && mkdir templates")
        os.system("cd sandbox/"+project_name+" && mkdir media")

        # Creating a requirements.txt file
        req_file = open("sandbox/"+project_name+"/requirements.txt","w")
        req_file.close()

        # Creating a serializers.py file in apps if rest_framework is true
        if rest_framework:
            for app in apps:
                serializers_file = open("sandbox/"+project_name+"/"+app+"/serializers.py","w")
                serializers_file.close()
        # Creating a urls.py file in apps
        for app in apps:
            urls_file = open("sandbox/"+project_name+"/"+app+"/urls.py","w")
            urls_file.close()

        return True
    except Exception as e:
        print(e)
        return False  

def startSandbox(data):
    # Getting data
    project_name = data['project_name']
    apps = data['apps']
    database = data['database']
    rest_framework = data['rest_framework']
    template_based = data['template_based']
    models = []
    if "models" in data:
        models = data['models']
    pip_packages = data['pip_packages']
    pagination = False
    if rest_framework:
        pagination = data['pagination']
        if pagination:
            page_size = data['page_size']
        else:
            page_size = 0
    
    # Creating all required files
    ret = createAllFiles(project_name,apps,rest_framework)
    if not ret:
        return False
    
    # Editing settings.py file
    settings = CreateSettings(project_name,apps,database,rest_framework,template_based,models,pip_packages,pagination,page_size)
    ret = settings.makeSettings()

    # Editing urls.py file in project and apps
    urls = CreateUrls(project_name,apps)
    ret = urls.makeUrls()
    if not ret:
        return False
    
    # Adding data to views.py file in apps
    views = CreateViews(project_name,apps,models,rest_framework,pagination)
    ret = views.makeViews()
    if not ret:
        return False

    # Adding data to models.py file in apps
    models_ob = CreateModels(project_name,apps,models)
    ret = models_ob.makeModels()
    if not ret:
        return False
    
    # Adding data to serializers.py file in apps
    if rest_framework:
        serializers = CreateSerializers(project_name,apps,models)
        ret = serializers.makeSerializers()
        if not ret:
            return False
        
    # Adding data to admin.py file
    admin = CreateAdmin(project_name,apps,models)
    ret = admin.makeAdmin()
    if not ret:
        return False
    
    # Making requirements
    req = CreateRequirements(project_name,pip_packages,rest_framework,template_based,database)
    ret = req.makeRequirements()
    if not ret:
        return False
    
    return True

# Create your views here.
@api_view(['POST'])
def getZip(request):
    # Check if all data is present or not
    if not "project_name" in request.data:
        return Response({"data":"project_name not present"},status.HTTP_400_BAD_REQUEST)
    if not "apps" in request.data:
        return Response({"data":"apps not present"},status.HTTP_400_BAD_REQUEST)
    if not "database" in request.data:
        return Response({"data":"database not present"},status.HTTP_400_BAD_REQUEST)
    if not "rest_framework" in request.data:
        return Response({"data":"rest_framework not present"},status.HTTP_400_BAD_REQUEST)
    if not "template_based" in request.data:
        return Response({"data":"template_based not present"},status.HTTP_400_BAD_REQUEST)
    if not "pip_packages" in request.data:
        return Response({"data":"pip_packages not present"},status.HTTP_400_BAD_REQUEST)
    if request.data['rest_framework']:
        if not "pagination" in request.data:
            return Response({"data":"pagination not present"},status.HTTP_400_BAD_REQUEST)
        if request.data['pagination']:
            if not "page_size" in request.data:
                return Response({"data":"page_size not present"},status.HTTP_400_BAD_REQUEST)
            
    ret = startSandbox(request.data)
    if ret:
        # make a zip of project then remove that project from sandbox and send that zip file
        output_filename = "zipsandbox/"+request.data['project_name']
        dir_name = "sandbox/"+request.data['project_name']
        shutil.make_archive(output_filename, 'zip', dir_name)
        # shutil.rmtree(dir_name)
        output_filename = output_filename+".zip"
        zip_file = open(output_filename, 'rb')
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=name.zip'
        #return response
        return Response({"data":"Yes"},status.HTTP_200_OK)
    else:
        return Response({"data":"No"},status.HTTP_400_BAD_REQUEST)


'''

sample data : 
{
    "project_name":"djangofy_backend_p",
    "apps":["djangofy_backend_a"],
    "database":"sqlite3",
    "rest_framework":True,
    "template_based":True,
    "models":[
        {
            "app_name":"djangofy_backend_a",
            "models" : [
                {
                    "model_name":"Zip",
                    "fields":[
                        {
                            "field_name":"zip_code",
                            "field_type":"models.CharField(max_length=100)",
                        }
                    ]
                }
            ]
        }
    ],
    "pip_packages":[
        "djangorestframework"
    ]
}
'''