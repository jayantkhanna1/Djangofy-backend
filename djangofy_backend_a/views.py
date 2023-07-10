from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from .models import User, UserProjects
from .serializers import UserSerializer,UserProjectsSerializer
from .makesettings import CreateSettings
from .makeurls import CreateUrls
from .makeviews import CreateViews
from .makemodels import CreateModels
from .makeserializers import CreateSerializers
from .makeadmin import CreateAdmin
from .makerequirements import CreateRequirements
from .makedocs import CreateDocs
from .makeasgi import CreateAsgi
from .makeconsumers import CreateConsumers
import shutil
from huggingface_hub import HfApi
import string
from github import Github
import requests
import os

import random
import requests
from django.core.mail import send_mail



# Helper Functions
def createAllFiles(project_name,apps,rest_app, socket):
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
            os.system("cd sandbox/"+project_name+" && django-admin startapp "+str(appname))

        # Creating static and templates folder
        os.system("cd sandbox/"+project_name+" && mkdir static")
        os.system("cd sandbox/"+project_name+" && mkdir templates")
        os.system("cd sandbox/"+project_name+" && mkdir media")

        # Creating a requirements.txt file
        req_file = open("sandbox/"+project_name+"/requirements.txt","w")
        req_file.close()

        # Creating a Readme.md file
        req_file = open("sandbox/"+project_name+"/Readme.md","w")
        req_file.close()

        # Creating a serializers.py file in apps if rest_framework is true
        i = 1
        if rest_app:
            for app in apps:
                appname = app["app_name_"+str(i)]
                i+=1
                serializers_file = open("sandbox/"+project_name+"/"+str(appname)+"/serializers.py","w")
                serializers_file.close()
        if socket:
            socket_file = open("sandbox/"+project_name+"/"+str(appname)+"/consumers.py","w")
            socket_file.close()

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

def startSandbox(data,email_backend,mobile_backend,static_backend, celery, socket):

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
    ret = createAllFiles(project_name,apps,rest_app,socket)
    if not ret:
        return False
    
    # Editing settings.py file
    settings = CreateSettings(project_name,apps,database,rest_app,template_based,pip_packages,pagination,page_size,email_backend,mobile_backend,static_backend, celery, socket)
    ret = settings.makeSettings()

    # Editing urls.py file in project and apps
    urls = CreateUrls(project_name,apps,template_based)
    ret = urls.makeUrls()
    if not ret:
        return False
    
    # Adding data to views.py file in apps
    views = CreateViews(project_name,apps,rest_app,pagination,email_backend,mobile_backend,static_backend,celery)
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
    req = CreateRequirements(project_name,pip_packages,rest_app,template_based,database,email_backend,mobile_backend,static_backend,celery)
    ret = req.makeRequirements()
    if not ret:
        return False
    
    # making asgi file for socket
    asgi = CreateAsgi(socket,project_name)
    asgi = asgi.makeAsgi()
    if not asgi:
        return False
    
    if socket:
        consumers = CreateConsumers(socket,apps,project_name)
        cons = consumers.makeConsumers()
        if not cons:
            return False
    # Making documentation
    docs = CreateDocs(project_name,apps,database,rest_app,template_based,pip_packages,pagination,page_size,email_backend,mobile_backend,static_backend, celery)
    ret = docs.makeDocs()
    if not ret:
        return False


    return True

def push_to_github(directory,github_access_token,repo_name,is_admin):
    
    # Replace these variables with your own values
    base_dir = os.getcwd()
    repo_name = "DJangofy_"+repo_name
    if is_admin:
        repo_name = repo_name
    
    access_token = github_access_token
    folder_path = directory

    # Create a Github instance using the access token
    g = Github(access_token)

    # Create a new repository with the given name
    user = g.get_user()
    try:
        repo = user.get_repo(repo_name)
        repo_name = repo_name + str(random.randint(100000,999999))
        repo = user.create_repo(repo_name)
    except:
        # If the repository doesn't exist, create it
        repo = user.create_repo(repo_name)
    print(repo.url)
    # Print a success message
    print("Repository successfully created!")

    # Set the local folder to push
    os.chdir(folder_path)
    

    # Read the contents of the folder and create a list of file paths
    file_list = []
    for root, dirs, files in os.walk("."):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_list.append(file_path)

    # Iterate over the file list and push each file to the repository
    for file_path in file_list:
        with open(file_path, 'r') as file:
            content = file.read()
        file_path = file_path[2:]  # Remove the "./" at the beginning of the file path
        file_path = file_path.replace("\\","/")
        repo.create_file(file_path, "commit message", content)

    # Delte the local folder
    os.chdir(base_dir)
    shutil.rmtree(folder_path)

    # Print a success message
    return repo_name,repo.url


# Main Functions
@api_view(['POST'])
def getZip(request):
    if "private_key" not in request.data:
        return Response({"data":"private_key not present. Please Log User in first"},status.HTTP_400_BAD_REQUEST)
    
    private_key = request.data['private_key']
    if not User.objects.filter(private_key=private_key).exists():
        return Response({"data":"Invalid private_key"},status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(private_key=private_key)
    if not user.otp_verified:
        return Response({"data":"User not verified"},status.HTTP_400_BAD_REQUEST)

    
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
    
    email_backend = None
    if "email" in request.data:
        email = request.data['email']
        if email:
            if "email_backend" not in request.data:
                return Response({"data":"email_backend not present"},status.HTTP_400_BAD_REQUEST)
            elif request.data["email_backend"] == None:
                return Response({"data":"email_backend not present"},status.HTTP_400_BAD_REQUEST)
            else:
                email_backend = request.data["email_backend"]
    
    mobile_backend = None
    if "mobile" in request.data:
        mobile = request.data['mobile']
        if mobile:
            if "mobile_backend" not in request.data:
                return Response({"data":"mobile_backend not present"},status.HTTP_400_BAD_REQUEST)
            elif request.data["mobile_backend"] == None:
                return Response({"data":"mobile_backend not present"},status.HTTP_400_BAD_REQUEST)
            else:
                mobile_backend = request.data["mobile_backend"]

    static_backend = None
    if "static" in request.data:
        static = request.data['static']
        if static:
            if "static_backend" not in request.data:
                return Response({"data":"static_backend not present"},status.HTTP_400_BAD_REQUEST)
            elif request.data["static_backend"] == None:
                return Response({"data":"static_backend not present"},status.HTTP_400_BAD_REQUEST)
            else:
                static_backend = request.data["static_backend"]

    celery = None
    if "celery" in request.data and request.data["celery"] :
        celery = request.data['celery']
    
    socket = None
    if "socket" in request.data and request.data["socket"]:
        socket = request.data['socket']

    ret = startSandbox(request.data,email_backend,mobile_backend,static_backend,celery,socket)
    if ret:
        # make a zip of project then remove that project from sandbox and send that zip file
        output_filename = "zipsandbox/"+request.data['project_name']
        dir_name = "sandbox/"+request.data['project_name']
        temp_dir_name = dir_name
        shutil.make_archive(output_filename, 'zip', dir_name)
        output_filename = output_filename+".zip"
        zip_file = open(output_filename, 'rb')
        zip_file.close()

        # Uploading zip to Hugging face
        api = HfApi()
        repo_id = os.environ.get("REPO_ID")
        repo_type = "dataset"
        folder_path = output_filename
        path_in_repo = output_filename
        api.upload_file(
            path_or_fileobj=folder_path,
            path_in_repo=path_in_repo,
            repo_id=repo_id,
            repo_type=repo_type,
            token = os.environ.get("HUGGINGFACE_TOKEN")
        )
        download_link= "https://huggingface.co/datasets/"+str(repo_id)+"/resolve/main/"+str(path_in_repo)         
        project_name = request.data['project_name']
        
        os.remove(output_filename)
        repo_name = None
        repo_url = None
        if user.github_token:
            repo_name,repo_url = push_to_github(temp_dir_name,user.github_token,request.data['project_name'],user.admin)

        userproject = UserProjects.objects.create(user=user,project_name=project_name,project_link=download_link,project_data=request.data,github_link=repo_url,github_repo_name=repo_name)
        userproject.save()
        userprojectserialized = UserProjectsSerializer(userproject).data
        return Response({"data":"Success","userproject":userprojectserialized},status.HTTP_200_OK)
    else:
        return Response({"data":"No"},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_signup(request):
    if "email" not in request.data or "password" not in request.data or "name" not in request.data or "type_of_user" not in request.data:
        return Response({"data":"email or password or name or type_of_user not present"},status.HTTP_400_BAD_REQUEST)

    email = request.data['email']
    password = request.data['password']
    name = request.data['name']
    type_of_user = request.data['type_of_user']

    if User.objects.filter(email=email).exists():
        return Response({"data":"User already exists"},status.HTTP_400_BAD_REQUEST)
    
    else:
        otp = str(random.randint(100000,999999))
        subject = "OTP for signup with Djangofy"
        message = "Your OTP for signup with Djangofy is "+otp + ". Please do not share this OTP with anyone."
        mail_to = [email]
        mail_from = os.environ.get("EMAIL_HOST_USER")
        send_mail(
            subject,
            message,
            mail_from,
            mail_to,
            fail_silently=False,
        )
        user = User(email=email,password=password,name=name,type_of_user=type_of_user,otp = otp, otp_verified = False)
        user.save()
        return Response({"data":"Otp generated","otp":otp},status.HTTP_200_OK)

@api_view(['POST'])
def user_verify(request):
    if "otp" not in request.data or "email" not in request.data:
        return Response({"data":"otp or email not present"},status.HTTP_400_BAD_REQUEST)
    otp = request.data['otp']
    email = request.data['email']
    if User.objects.filter(email=email,otp=otp).exists():
        user = User.objects.get(email=email,otp=otp)
        user.otp=""
        user.otp_verified = True
        user.private_key = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
        user.save()
        user_data = UserSerializer(user).data
        return Response({"data":"User verified","user":user_data},status.HTTP_200_OK)
    else:
        return Response({"data":"Invalid OTP"},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if "private_key" in request.data:
        private_key = request.data['private_key']
        if User.objects.filter(private_key=private_key).exists():
            user = User.objects.get(private_key=private_key)
            user_data = UserSerializer(user).data
            user_projects = UserProjects.objects.filter(user=user)
            user_projects = UserProjectsSerializer(user_projects,many=True).data
            return Response({"data":"User logged in","user":user_data,"user_projects":user_projects},status.HTTP_200_OK)
        else:
            return Response({"data":"Private Key does not exist"},status.HTTP_400_BAD_REQUEST)
        
    if "email" not in request.data or "password" not in request.data:
        return Response({"data":"email or password not present"},status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    password = request.data['password']
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if user.password == password:
            user_data = UserSerializer(user).data
            user_projects = UserProjects.objects.filter(user=user)
            user_projects = UserProjectsSerializer(user_projects,many=True).data
            return Response({"data":"User logged in","user":user_data,"user_projects":user_projects},status.HTTP_200_OK)
        else:
            return Response({"data":"Wrong password"},status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"data":"User does not exist"},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgot_password(request):
    if "email" not in request.data:
        return Response({"data":"email not present"},status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        otp = str(random.randint(100000,999999))
        subject = "OTP for reset password with Djangofy"
        message = "Your OTP for reset password with Djangofy is "+otp + ". Please do not share this OTP with anyone."
        mail_to = [email]
        mail_from = os.environ.get("EMAIL_HOST_USER")
        send_mail(
            subject,
            message,
            mail_from,
            mail_to,
            fail_silently=False,
        )
        user.otp = otp
        user.save()
        return Response({"data":"Otp generated","otp":otp},status.HTTP_200_OK)
    else:
        return Response({"data":"User does not exist"},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    if "otp" not in request.data or "email" not in request.data or "password" not in request.data:
        return Response({"data":"otp or email or password not present"},status.HTTP_400_BAD_REQUEST)
    otp = request.data['otp']
    email = request.data['email']
    password = request.data['password']
    if User.objects.filter(email=email,otp=otp).exists():
        user = User.objects.get(email=email,otp=otp)
        user.otp=""
        user.password = password
        user.save()
        return Response({"data":"Password reset successfully"},status.HTTP_200_OK)
    else:
        return Response({"data":"Invalid OTP"},status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    url = "https://github.com/login/oauth/authorize?client_id="+client_id+"&scope=user,email,repo"
    return Response({"data":"Github login","url":url},status.HTTP_200_OK)

@api_view(['GET'])
def github_callback(request):
    code = request.GET.get('code')
    url = os.environ.get("BASE_URL") + "githubConfirm"
    r = requests.post(url, data={'code': code})
    return Response({"data":"Github callback","code":code},status.HTTP_200_OK)

@api_view(['POST'])
def github_confirm(request):
    try:
        code = request.data["code"]
        # Set the client ID, client secret, and authorization code
        client_id = os.environ.get("GITHUB_CLIENT_ID")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
        authorization_code = code

        # Set the headers and data for the request
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': authorization_code
        }

        # Make a POST request to the GitHub API to get an access token
        response = requests.post('https://github.com/login/oauth/access_token', headers=headers, data=data)
        
        if response.status_code != 200:
            return Response({"data":"Invalid code"},status.HTTP_400_BAD_REQUEST)

        if 'access_token' not in response.json():
            return Response({"data":"Invalid code"},status.HTTP_400_BAD_REQUEST)
        
        access_token = response.json()['access_token']

        # Set the headers to include the access token
        headers = {'Authorization': f'Bearer {access_token}'}

        # Make a request to the GitHub API to get the authenticated user's information
        response = requests.get('https://api.github.com/user/emails', headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            user_info = response.json()
            try:
                email = user_info[0]['email']
            except:
                if "email" in request.data:
                    email = request.data['email']   
                else:
                    return Response({"data":"Email not present"},status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.github_token = access_token
                user.email = email
                user.otp_verified = True
                user.private_key = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
                user.save()
                user_data = UserSerializer(user).data
                user_projects = UserProjects.objects.filter(user=user)
                user_projects = UserProjectsSerializer(user_projects,many=True).data
                return Response({"data":"User logged in","user":user_data,"user_projects":user_projects},status.HTTP_200_OK)
            else:
                user = User(email=email,type_of_user="free",otp_verified = True,private_key = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15)),github_token = access_token)
                user.save()
                user_data = UserSerializer(user).data
                return Response({"data":"User logged in","user":user_data},status.HTTP_200_OK)
        else:
            print(response.status_code)
            print(response.text)
            return Response({"data":"Invalid code"},status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"data":"Some Internal Server Error Occurred","error" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR)



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
