import textwrap
textwrap.indent

class CreateSettings:
    def __init__(self,project_name,apps,database,rest_framework,template_based,models,pip_packages,pagination,page_size):
        self.project_name = project_name
        self.apps = apps
        self.database = database
        self.rest_framework = rest_framework
        self.template_based = template_based
        self.models = models
        self.pip_packages = pip_packages
        self.pagination = pagination
        self.page_size = page_size
    
    def checkDatabase(self):
            if self.database == "sqlite3":
                return 1
            elif self.database == "postgresql":
                return 2
            elif self.database == "mysql":
                return 3
            elif self.database == "mongodb":
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
                env_file = open("sandbox/"+self.project_name+"/.env","w")
                env_file.write("DB_NAME='' \nDB_USER='' \nDB_PASSWORD='' \nDB_HOST='' \nDB_PORT=''")

            elif val == 3:
                pass
            elif val == 4:
                pass


        if self.rest_framework and self.pagination:
            rest_framework_string = "\nREST_FRAMEWORK = {\n    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',\n    'PAGE_SIZE': "+str(self.page_size)+"\n}"
            settings_data = settings_data + rest_framework_string

        # Replace all data in settings.py
        settings_file = open("sandbox/"+self.project_name+"/"+self.project_name+"/settings.py","w")
        settings_file.write(settings_data)
        settings_file.close()

        return True