class CreateDocs:
    def __init__(self, project_name,apps,database,rest_app,template_based,pip_packages,pagination,page_size,email_backend,mobile_backend,static_backend, celery):
        self.project_name = project_name
        self.pip_packages = pip_packages
        self.rest_app = rest_app
        self.template_based = template_based
        self.database = database
        self.email_backend = email_backend
        self.mobile_backend = mobile_backend
        self.static_backend = static_backend
        self.celery = celery
        self.path = "sandbox/"+self.project_name
        self.pagination = pagination
        self.apps = []
        i=1
        for app in apps:
            self.apps.append(app["app_name_"+str(i)])
            i+=1


    def makeDocs(self):
        try:
            file = open("sandbox/"+self.project_name+"/Readme.md","w")
            file.write("# Djangofy\n\n")
            data = '''
Hello and thank you for choosing Djangofy for your development needs. We're excited to help you build your web application using the power and flexibility of Django. Whether you're a seasoned developer or just starting out, Djangofy provides the tools and resources you need to create robust and scalable web applications.

Our team of experienced developers is dedicated to helping you build the application of your dreams. We offer a range of services, including custom web application development, database design and optimization, and cloud hosting solutions. With Djangofy, you can be confident that you're getting the best possible service and support.

We believe in the power of open-source software and the Django community, and we're committed to giving back. That's why we contribute to the Django project and support the growth of the community through events and sponsorships.

Thank you again for choosing Djangofy. We're excited to work with you and help you bring your vision to life.


 '''
            file.write(data)
            file.write("# Installation\n\n")
            data = '''

When you verify your Git account, any project you create will be automatically pushed to your GitHub account. From there, you can easily clone the project to your local machine by running the following command in your terminal: 

```bash
git clone https://github.com/<your username>/<Project Name>.git
```

If you haven't verified your Git account, don't worry! You can still download the project as a zip file and extract it to your local machine. This option is provided at the last step of project creation, so you can easily access and work with the files even without a Git account.

'''
            file.write(data)
            file.write("# Setup\n\n## Virtual Environment\n")
            data = '''

To ensure a clean and organized development environment, it is highly recommended to use a virtual environment when working with any project. You can create a virtual environment for your project by running the following command in your terminal:

```bash
python -m venv <name of virtual environment>
```

Once your virtual environment is created, you can activate it using the appropriate command for your operating system.

Windows:
```bash
.\<name of virtual environment>\Scripts\\activate
```

Linux/Unix:
```bash
source <name of virtual environment>/bin/activate
```

By activating your virtual environment, you can ensure that any dependencies and packages you install will be isolated from your global environment, making it easier to manage and maintain your project.

'''

            file.write(data)
            file.write("## Installing Dependencies\n\n")
            data = '''
      
To install all the necessary dependencies for your project, simply run the following command in your terminal:

```bash
pip install -r requirements.txt
```
This command will read the requirements.txt file and automatically install all the listed dependencies for you. Make sure your virtual environment is activated before running this command to ensure that the packages are installed in the correct environment. Once the installation is complete, you'll be ready to start working on your project!

'''
            file.write(data)
            file.write("## .env\n\n")
            data = '''

<b> Important Note: </b>
Please ensure that you add all the necessary sensitive information, such as database credentials and API keys, to the .env file. This file is used to store this information securely and is not pushed to GitHub by default. However, please note that we have added the .env file to the repository, but it is empty to ensure that you can fill it out with the required data.

To prevent any accidental disclosure of sensitive information, make sure to add the .env file to the .gitignore file before committing your code to the repository. This way, you can keep your data secure while still being able to utilize the benefits of version control.
'''

            file.write(data)

            file.write("# What we have done for you:\n\n")

            if self.rest_app:
                file.write("## Rest Application\n\n")
                data = '''
                
We've taken care of the setup for your Rest application so that you can focus on building out your views and logic. All the necessary files and configurations have been created for you, and you don't need to worry about importing or setting anything in settings.py.

To return a REST response from your views, simply write your view as you normally would and return a Response object with the data you want to return. The Response object is already included in the required modules and is automatically configured to work with the REST framework.

So, whether you're returning JSON data, an HTML response or any other format, just build your view and return it using the Response object, and the framework will handle the rest. With the setup work already taken care of, you can focus on building your project with confidence!

```python
def my_view(request):
    data = {
        'message': 'No worries, we got you covered!'
    }
    return Response(data,status.HTTP_200_OK)
```

'''
                file.write(data)

            if self.template_based:
                file.write("## Template Based Application\n\n")
                data = '''

Great news! We've already set up all the necessary files and configurations for you to create a simple template-based application. This means you can start building your views and logic right away without worrying about the initial setup.

All you need to do is put your HTML files in the templates folder, and your CSS, JavaScript, and images in the static folder, and you're ready to go! You don't need to worry about configuring media routes either because we've taken care of that for you.

With the setup work out of the way, you can focus on building your application and creating the perfect user experience for your users. So, go ahead and start building your application with confidence!

'''

                file.write(data)

            if self.pagination:
                file.write("## Pagination\n\n")
                data = '''

Woo hoo! Since you've selected pagination for your project, we've already taken care of setting it up for you. All you need to do is return your response, and the page will be paginated automatically.

With pagination taken care of, you can focus on creating a great user experience for your users. So, go ahead and start building your application with confidence!

'''
                file.write(data)
            
            file.write("## Project And Apps:\n\n")
            data = '''
            
All projects and apps are datauctured in a uniform manner for easy understanding and maintenance. The project folder contains a sub-folder with the same name as the project and contains the main settings, URL routing, and WSGI configuration files. Additionally, there are separate folders for each app within the project, which contain the models, views, and URL routing for each app. The migrations folder within each app handles database migrations. The root folder also contains files such as .env, .gitignore, manage.py, README.md, and requirements.txt for managing project dependencies and version control. This standardized dataucture simplifies development, maintenance, and collaboration on projects.

'''
            file.write(data)
            
            file.write("## Database\n\n")
            data = '''
            
Awesome news! We've got you covered with a pre-configured '''+self.database+''' database for your project, so no need to fret about setting it up yourself. Simply create your models and run the migrations, and you're good to go!

Before diving into your project, remember to create a database specifically for it and add the necessary credentials to your .env file.

To begin using your project, it is important to create the necessary database migrations and apply them. You can easily do this by running the following commands in your terminal:

```bash
python manage.py makemigrations
python manage.py migrate
```

These commands will create the necessary migration files and apply them to your database, setting it up for use. With this done, you can now confidently start building your project!
'''
            file.write(data)
            
            file.write("## Modals:\n\n")
            data = '''

We have some great news for you! Managing models in your project is now a breeze, thanks to our setup. All the models you entered earlier, they are automatically added to the admin panel for easy maintenance and updates. And if you've opted for Django Rest Framework, the models are also automatically serialized and added to the views.py file, so you can easily manipulate and access them.

You can now fully concentrate on developing your app's functionality without worrying about managing your models. Our setup dataeamlines everything for you, so you can get started right away with ease.
            
            '''
            file.write(data)
            
            if self.email_backend:
                file.write("## Email Integration\n\n")
                data = '''

We've got you covered with a pre-configured email integration for your project, so no need to fret about setting it up yourself. Simply add the necessary credentials to your .env file, and you're good to go!

To send a mail from your project, send_mail function from django.core.mail have already been imported for you. You can easily do this by running the following commands in your terminal:

```python
send_mail(
    'Subject here',
    'Here is the message.',
    '<sender email>',
    ['<receiver email>'],
    fail_silently=False,
) 
```

'''
                file.write(data)

            if self.mobile_backend:
                data = '''

## Mobile Integration
            
'''
                file.write(data)
                data = '''

We've got you covered with a pre-configured mobile integration for your project, so no need to fret about setting it up yourself. Simply add the necessary credentials to your .env file, and you're good to go!

To send a message from your project, Client function from from twilio.rest have already been imported for you. You can easily do this by running the following commands in your terminal:

```python
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
    body="Hello from Twilio integrated by Djangofy!",
    from_=os.getenv('TWILIO_NUMBER'),
    to='<User Mobile Number>'
)

```

'''
                file.write(data)

            if self.static_backend:
                file.write("## Cloud Storage\n\n")
                data = '''

We've got you covered with a pre-configured cloud storage for your project, so no need to fret about setting it up yourself. Simply add the necessary credentials to your .env file, and you're good to go!

                '''
                file.write(data)

                if self.static_backend.lower() == "aws":
                    data = '''

As you selected AWS S3 storage, we have already installed boto3 for you.

To upload a file from your project, upload_file function from from boto3 have already been imported for you. You can easily do this by running the following commands in your terminal:

```python
# Enter your S3 bucket name and region
bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
region_name = os.getenv('AWS_S3_REGION_NAME')

# Enter your AWS access key and secret key
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Create an S3 client
s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

# Specify the file to upload and its name on S3
local_file_path = "/path/to/local/file.txt"
s3_file_name = "uploaded-file.txt"

# Upload the file to S3
s3.upload_file(local_file_path, bucket_name, s3_file_name)
```

'''
                    file.write(data)

                elif self.static_backend.lower() == "azure":
                    data = '''

As you selected Azure storage, we have already setup azure.storage for you.

To upload a file from your project, BlobServiceClient function from from azure.storage.blob have already been imported for you. You can easily do this by running the following commands in your terminal:

```python

AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
AZURE_ENDPOINT_SUFFIX = os.getenv("AZURE_ENDPOINT_SUFFIX")

# Set the connection dataing for your Azure Storage account
connect_data = f"DefaultEndpointsProtocol=https;AccountName={AZURE_ACCOUNT_NAME};AccountKey={AZURE_ACCOUNT_KEY};EndpointSuffix={AZURE_ENDPOINT_SUFFIX}"

# Create a BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_dataing(connect_data)

# Set the name of the container and blob
container_name = "<container_name>"
blob_name = "<blob_name>"

# Create a ContainerClient object
container_client = blob_service_client.get_container_client(container_name)

# Create a BlobClient object
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# Set the path to the file you want to upload
file_path = "<file_path>"

# Upload the file to Azure Blob Storage
with open(file_path, "rb") as data:
    blob_client.upload_blob(data)
```

'''
                    file.write(data)

                elif self.static_backend.lower() == "gcp":
                    data = '''

As you selected Google Cloud storage, we have already setup google.cloud.storage for you.

To upload a file from your project, BlobServiceClient function from from google.cloud.storage have already been imported for you. You can easily do this by running the following commands in your terminal:

```python
# Set the name of your Google Cloud Storage bucket
bucket_name = os.getenv("GS_BUCKET_NAME")

# Create a client object
client = storage.Client()

# Get the bucket object
bucket = client.get_bucket(bucket_name)

# Set the name of the blob
blob_name = "<blob_name>"

# Get the blob object
blob = bucket.blob(blob_name)

# Set the path to the file you want to upload
file_path = "<file_path>"

# Upload the file to Google Cloud Storage
with open(file_path, "rb") as data:
    blob.upload_from_file(data)
```

'''
                    file.write(data)     

                else:
                    pass

            if self.celery:
                file.write("## Celery\n\n")
                data = '''

Everything has been set in celery for you. You only need to write celery functions here is a step by step guide for you

1. First run Redis on a port default is 6379. Add these to the .env file

2. Now run celery worker in a new terminal

```bash
celery -A <project name> worker -l info -P eventlet
``` 

3. Now go to tasks.py file in the project folder and write your celery function there.

```python
@shared_task
def add(x, y):
    return x + y
```

4. Now go to views.py file in the project folder and call your celery function there.

```python
add.delay(4, 4)
```

'''
                file.write(data)
            
            file.write("# What do we have to do\n\n")
            data ='''
            
To get started with a simple project, all you need to do is set the routes in urls.py and write functions in views.py. However, if you want to make your project more complex, you might want to edit other files such as models.py, serializers.py, admin.py, and more. But don't worry, we have already preconfigured these files for you, so you can get started with ease.

But if you really don't want to do anything, just shoot us an email at djangofymail@gmail.com, and we'll take care of it for you. Our team is always happy to help you get started on your any project..

At our organization, we specialize in a variety of technology stacks including React (Frontend), Nodejs (Backend), Django (Backend), Flask (Backend), Designing, Cybersecurity, and much more. We take pride in our ability to provide top-notch services to our clients and help them achieve their project goals. Whether you need assistance with a small or large project, we're always ready to lend a helping hand.

So if you're stuck with a project, or simply need some expert guidance, don't hesitate to reach out to us. Our team of experienced professionals is always here to help you succeed.

'''
            file.write(data)
            file.close()

            return True
        except Exception as e:
            print(str(e))
            return False
        


