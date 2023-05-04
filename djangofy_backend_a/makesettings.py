import textwrap
textwrap.indent

class CreateSettings:
    def __init__(self,project_name,apps,database,rest_framework,template_based,pip_packages,pagination,page_size,email_backend,mobile_backend,static_backend):
        self.project_name = project_name
        self.apps = []
        i=1
        for app in apps:
            self.apps.append(app["app_name_"+str(i)])
            i+=1
        self.database = database
        self.rest_framework = rest_framework
        self.template_based = template_based
        self.pip_packages = pip_packages
        self.pagination = pagination
        self.page_size = page_size
        self.email_backend = email_backend
        self.mobile_backend = mobile_backend
        self.static_backend = static_backend
    
    def checkDatabase(self):
            if self.database.lower() == "sqlite3":
                return 1
            elif self.database.lower() == "postgresql":
                return 2
            elif self.database.lower() == "mysql":
                return 3
            elif self.database.lower() == "mongodb":
                return 4
            else:
                return -1

    def makeSettings(self):
        settings_file = open("sandbox/"+self.project_name+"/"+self.project_name+"/settings.py","r")
        settings_data = settings_file.read()
        settings_file.close()


        # Adding import statement on top of file
        settings_data = "from dotenv import load_dotenv \nload_dotenv() \nimport os\n" + settings_data

        # Editing INSTALLED_APPS
        preinstalled_apps = settings_data.split("INSTALLED_APPS = [")[1]
        preinstalled_apps = preinstalled_apps.split("]")[0]
        preinstalled_apps = preinstalled_apps.split(",")
        for i in range(len(self.apps)):
            self.apps[i] = "'"+self.apps[i]+"'"

        preinstalled_apps = [app.strip() for app in preinstalled_apps]
        for x in self.apps:
            preinstalled_apps.append(x)
        preinstalled_apps = [x for x in preinstalled_apps if x != '']
        if self.rest_framework:
            preinstalled_apps.append("'rest_framework'")
            preinstalled_apps.append("'django_filters'")
        preinstalled_apps.append("'corsheaders'")
        installed_Apps = "INSTALLED_APPS = [\n" + ",\n".join(preinstalled_apps) + "\n]"
        settings_data = settings_data.replace(settings_data.split("INSTALLED_APPS = [")[1].split("]")[0],installed_Apps.split("INSTALLED_APPS = [")[1].split("]")[0])

        # Editing MIDDLEWARE and adding whitenoise middleware
        preinstalled_middleware = settings_data.split("MIDDLEWARE = [")[1]
        preinstalled_middleware = preinstalled_middleware.split("]")[0]
        preinstalled_middleware = preinstalled_middleware.split(",")
        preinstalled_middleware = [app.strip() for app in preinstalled_middleware]
        preinstalled_middleware.append("'whitenoise.middleware.WhiteNoiseMiddleware'")
        preinstalled_middleware = [x for x in preinstalled_middleware if x != '']
        installed_middleware = "MIDDLEWARE = [\n" + ",\n".join(preinstalled_middleware) + "\n]"
        settings_data = settings_data.replace(settings_data.split("MIDDLEWARE = [")[1].split("]")[0],installed_middleware.split("MIDDLEWARE = [")[1].split("]")[0])

        # For static and media
        if self.template_based:
            if self.static_backend == "aws":
                aws_str = '''
                
                    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID'),
                    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY'),
                    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME'),
                    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME'),

                    # Use S3 for static and media files
                    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
                    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

                    # Set S3 bucket URL for static files
                    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

                    # Set static and media URLs
                    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, 'static')
                    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, 'media')
                '''
                settings_data = settings_data.replace("STATIC_URL = '/static/'",textwrap.dedent(aws_str))
                settings_data = settings_data.replace("STATIC_URL = 'static/'",textwrap.dedent(aws_str))

                # Add this data to .env file
                env_file = open("sandbox/"+self.project_name+"/.env","a")
                env_file.write("AWS_ACCESS_KEY_ID='' \nAWS_SECRET_ACCESS_KEY='' \nAWS_STORAGE_BUCKET_NAME='' \nAWS_S3_REGION_NAME=''")

            else:
                settings_data = settings_data.replace("'DIRS': [],","'DIRS': [os.path.join(BASE_DIR, 'templates')],")
                static_and_media_string = "\nSTATIC_URL = '/static/'\nSTATIC_ROOT = os.path.join(BASE_DIR, 'static/')" + "\nMEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media/')"
                settings_data = settings_data.replace("STATIC_URL = '/static/'",static_and_media_string)
                settings_data = settings_data.replace("STATIC_URL = 'static/'",static_and_media_string)
            

        # For database also change
        val = self.checkDatabase()

        if val != -1:
            if val == 1:
                pass
            elif val == 2:
                # Remove database from settings_data
                settings_data = settings_data.replace(settings_data.split("DATABASES = {")[1].split("}")[0],"")
                settings_data = settings_data.replace("DATABASES = {}\n}","")

                database_str = '''
                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.postgresql',
                        'NAME': os.getenv('DB_NAME'),
                        'USER': os.getenv('DB_USER'),
                        'PASSWORD': os.getenv('DB_PASSWORD'),
                        'HOST': os.getenv('DB_HOST'),
                        'PORT': int(os.getenv('DB_PORT')),
                    }
                }
                '''
                # Remove extra indent
                database_str = textwrap.dedent(database_str)
                settings_data = settings_data + database_str
                # Add this data to .env file
                env_file = open("sandbox/"+self.project_name+"/.env","a")
                env_file.write("DB_NAME='' \nDB_USER='' \nDB_PASSWORD='' \nDB_HOST='' \nDB_PORT=''\n")

            elif val == 3:
                # Remove database from settings_data
                settings_data = settings_data.replace(settings_data.split("DATABASES = {")[1].split("}")[0],"")
                settings_data = settings_data.replace("DATABASES = {}\n}","")

                database_str = '''
                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.mysql',
                        'NAME': os.getenv('DB_NAME'),
                        'USER': os.getenv('DB_USER'),
                        'PASSWORD': os.getenv('DB_PASSWORD'),
                        'HOST': os.getenv('DB_HOST'),
                        'PORT': int(os.getenv('DB_PORT')),
                    }
                }
                '''
                # Remove extra indent
                database_str = textwrap.dedent(database_str)
                settings_data = settings_data + database_str
                # Add this data to .env file
                env_file = open("sandbox/"+self.project_name+"/.env","a")
                env_file.write("DB_NAME='' \nDB_USER='' \nDB_PASSWORD='' \nDB_HOST='' \nDB_PORT=''\n")

            elif val == 4:
                # Remove database from settings_data
                settings_data = settings_data.replace(settings_data.split("DATABASES = {")[1].split("}")[0],"")
                settings_data = settings_data.replace("DATABASES = {}\n}","")

                database_str = '''
                DATABASES = {
                    'default': {
                        'ENGINE': 'djongo',
                        'NAME': os.getenv('DB_NAME'),
                        'ENFORCE_SCHEMA': False,
                        'CLIENT': {
                            'host': os.getenv('DB_HOST'),
                            'port': int(os.getenv('DB_PORT')),
                            'username': os.getenv('DB_USER'),
                            'password': os.getenv('DB_PASSWORD'),
                            'authSource': os.getenv('DB_NAME'),
                            'authMechanism': 'SCRAM-SHA-256'
                        }
                    }
                }
                '''

                # Remove extra indent
                database_str = textwrap.dedent(database_str)
                settings_data = settings_data + database_str
                
                # Add this data to .env file
                env_file = open("sandbox/"+self.project_name+"/.env","a")
                env_file.write("DB_NAME='' \nDB_USER='' \nDB_PASSWORD='' \nDB_HOST='' \nDB_PORT=''\n")


        if self.rest_framework and self.pagination:
            rest_framework_string = "\nREST_FRAMEWORK = {\n    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',\n    'PAGE_SIZE': "+str(self.page_size)+"\n}"
            settings_data = settings_data + rest_framework_string

        if self.email_backend is not None:
            '''
            
                EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
                EMAIL_HOST = 'smtp.gmail.com'
                EMAIL_PORT = 587
                EMAIL_USE_TLS = True
                EMAIL_HOST_USER = 'your_gmail_address@gmail.com'
                EMAIL_HOST_PASSWORD = 'your_gmail_app_password'
            '''
            email_str = '''

                EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
                EMAIL_HOST = 'smtp.gmail.com'
                EMAIL_PORT = os.getenv('EMAIL_PORT')
                EMAIL_USE_TLS = True
                EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
                EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
            '''

            # Add this data to .env file
            env_file = open("sandbox/"+self.project_name+"/.env","a")
            env_file.write("EMAIL_PORT='' \nEMAIL_HOST_USER='' \nEMAIL_HOST_PASSWORD=''\n")

            # Remove extra indent
            email_str = textwrap.dedent(email_str)
            settings_data = settings_data + email_str
        
        if self.mobile_backend is not None:
            mobile_str = '''
            
                TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
                TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
                TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
            '''

            # Add this data to .env file
            env_file = open("sandbox/"+self.project_name+"/.env","a")
            env_file.write("TWILIO_ACCOUNT_SID='' \nTWILIO_AUTH_TOKEN='' \nTWILIO_PHONE_NUMBER=''\n")

            # Remove extra indent
            mobile_str = textwrap.dedent(mobile_str)
            settings_data = settings_data + mobile_str
            
        # Replace all data in settings.py
        settings_file = open("sandbox/"+self.project_name+"/"+self.project_name+"/settings.py","w")
        settings_file.write(settings_data)
        settings_file.close()

        return True