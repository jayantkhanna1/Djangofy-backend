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


def createAllFiles(project_name,apps,rest_app):
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
        i=1
        for app in apps:
            appname = app["app_name_"+str(i)]
            i+=1
            os.system("cd sandbox/"+project_name+" && python manage.py startapp "+str(appname))

        # Creating static and templates folder
        os.system("cd sandbox/"+project_name+" && mkdir static")
        os.system("cd sandbox/"+project_name+" && mkdir templates")
        os.system("cd sandbox/"+project_name+" && mkdir media")

        # Creating a requirements.txt file
        req_file = open("sandbox/"+project_name+"/requirements.txt","w")
        req_file.close()

        # Creating a serializers.py file in apps if rest_framework is true
        i = 1
        if rest_app:
            for app in apps:
                appname = app["app_name_"+str(i)]
                i+=1
                serializers_file = open("sandbox/"+project_name+"/"+str(appname)+"/serializers.py","w")
                serializers_file.close()

        # Creating a urls.py file in apps
        i = 1
        for app in apps:
            appname = app["app_name_"+str(i)]
            i+=1
            urls_file = open("sandbox/"+project_name+"/"+str(appname)+"/urls.py","w")
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
    rest_app = data['rest_app']
    template_based = data['template_based']
    # pip_packages = data['pip_packages']
    if "pip_packages" in data:
        pip_packages = data['pip_packages']
    else:
        pip_packages = []
    pagination = False
    if rest_app:
        pagination = data['pagination']
        if pagination:
            page_size = data['page_size']
        else:
            page_size = 0
    
    # Creating all required files
    ret = createAllFiles(project_name,apps,rest_app)
    if not ret:
        return False
    
    # Editing settings.py file
    settings = CreateSettings(project_name,apps,database,rest_app,template_based,pip_packages,pagination,page_size)
    ret = settings.makeSettings()

    # Editing urls.py file in project and apps
    urls = CreateUrls(project_name,apps)
    ret = urls.makeUrls()
    if not ret:
        return False
    
    # Adding data to views.py file in apps
    views = CreateViews(project_name,apps,rest_app,pagination)
    ret = views.makeViews()
    if not ret:
        return False

    # Adding data to models.py file in apps
    models_ob = CreateModels(project_name,apps)
    ret = models_ob.makeModels()
    if not ret:
        return False
    
    # Adding data to serializers.py file in apps
    if rest_app:
        serializers = CreateSerializers(project_name,apps)
        ret = serializers.makeSerializers()
        if not ret:
            return False
        
    # Adding data to admin.py file
    admin = CreateAdmin(project_name,apps)
    ret = admin.makeAdmin()
    if not ret:
        return False
    
    # Making requirements
    req = CreateRequirements(project_name,pip_packages,rest_app,template_based,database)
    ret = req.makeRequirements()
    if not ret:
        return False
    
    return True

# Create your views here.
@api_view(['POST'])
def getZip(request):
    if not "project_name" in request.data:
        return Response({"data":"project_name not present"},status.HTTP_400_BAD_REQUEST)
    if not "apps" in request.data:
        return Response({"data":"apps not present"},status.HTTP_400_BAD_REQUEST)
    if not "database" in request.data:
        return Response({"data":"database not present"},status.HTTP_400_BAD_REQUEST)
    if not "rest_app" in request.data:
        return Response({"data":"rest_app not present"},status.HTTP_400_BAD_REQUEST)
    if not "template_based" in request.data:
        return Response({"data":"template_based not present"},status.HTTP_400_BAD_REQUEST)
    if request.data['rest_app']:
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
        shutil.rmtree(dir_name)
        output_filename = output_filename+".zip"
        zip_file = open(output_filename, 'rb')
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=file.zip'
        os.remove(str(output_filename))
        return response
        # return Response({"data":"Yes"},status.HTTP_200_OK)
    else:
        return Response({"data":"No"},status.HTTP_400_BAD_REQUEST)





'''
{
    "rest_app": true,
    "template_based": true,
    "project_name": "my_special_project",
    "database": "PostgreSQL",
    "apps": [
        {
            "appIndex": "1",
            "app_name_1": "App Name amazing",
            "modals": [
                {
                    "name": "Modal 1",
                    "fields": [
                        {
                            "name": "name",
                            "type": "text"
                        },
                        {
                            "name": "email",
                            "type": "email"
                        }
                    ]
                },
                {
                    "name": "new modela 1",
                    "fields": [
                        {
                            "name": "wrfrg",
                            "type": "text"
                        }
                    ]
                }
            ]
        },
        {
            "appIndex": "2",
            "app_name_2": "bvnm ",
            "modals": [
                {
                    "name": "vb",
                    "fields": [
                        {
                            "name": "vb",
                            "type": "text"
                        }
                    ]
                }
            ]
        }
    ]
}



'''


'''
  `AutoField`: `id = models.AutoField(primary_key=True)`
- `BigAutoField`: `id = models.BigAutoField(primary_key=True)`
- `BigIntegerField`: `number = models.BigIntegerField()`
- `BinaryField`: `data = models.BinaryField()`
- `BooleanField`: `is_published = models.BooleanField()`
- `CharField`: `title = models.CharField(max_length=200)`
- `DateField`: `publish_date = models.DateField()`
- `DateTimeField`: `publish_datetime = models.DateTimeField()`
- `DecimalField`: `price = models.DecimalField(max_digits=6, decimal_places=2)`
- `DurationField`: `duration = models.DurationField()`
- `EmailField`: `email = models.EmailField()`
- `FileField`: `file = models.FileField()`
- `FloatField`: `rating = models.FloatField()`
- `ForeignKey`: `author = models.ForeignKey(TABLE,on_delete=models.CASCADE)`
- `ImageField`: `image = models.ImageField()`
- `IntegerField`: `quantity = models.IntegerField()`
- `JSONField`: `data = models.JSONField()`
- `ManyToManyField`: `tags = models.ManyToManyField(TABLE)`
- `OneToOneField`: `profile = models.OneToOneField(TABLE, on_delete=models.CASCADE)` 
- `PositiveIntegerField`: `age = models.PositiveIntegerField()`
- `PositiveSmallIntegerField`: `rating = models.PositiveSmallIntegerField()`
- `SlugField`: `slug = models.SlugField()`
- `SmallIntegerField`: `rank = models.SmallIntegerField()`
- `TextField`: `description = models.TextField()`
- `TimeField`: `publish_time = models.TimeField()`

'''