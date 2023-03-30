project_name = "djangofy_backend_p"
app = ["djangofy_backend_a"]
rest_framework = True
pagination = True
tamplate_based = True
page_size = 10
database = "postgresql"
import textwrap
textwrap.indent

def checkDatabase(database):
    if database == "sqlite3":
        return 1
    elif database == "postgresql":
        return 2
    elif database == "mysql":
        return 3
    elif database == "mongodb":
        return 3
    else:
        return -1




settings_file = open("sandbox/"+project_name+"/"+project_name+"/settings.py","r")
settings_data = settings_file.read()
settings_file.close()


# Adding import statement on top of file
settings_data = "from dotenv import load_dotenv \nload_dotenv() \nimport os" + settings_data

# Editing INSTALLED_APPS
preinstalled_apps = settings_data.split("INSTALLED_APPS = [")[1]
preinstalled_apps = preinstalled_apps.split("]")[0]
preinstalled_apps = preinstalled_apps.split(",")
for i in range(len(app)):
    app[i] = "'"+app[i]+"'"

preinstalled_apps = [app.strip() for app in preinstalled_apps]
for x in app:
    preinstalled_apps.append(x)
preinstalled_apps = [x for x in preinstalled_apps if x != '']
if rest_framework:
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
if tamplate_based:
    # add template directory here too and also make templates and media and static folder in corret place
    static_and_media_string = "\nSTATIC_URL = '/static/'\nSTATIC_ROOT = os.path.join(BASE_DIR, 'static/')" + "\nMEDIA_URL = '/media/'\nMEDIA_ROOT = os.path.join(BASE_DIR, 'media/')"
    settings_data = settings_data.replace("STATIC_URL = '/static/'",static_and_media_string)
    settings_data = settings_data.replace("STATIC_URL = 'static/'",static_and_media_string)

# For database also change
val = checkDatabase(database)
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
        env_file = open("sandbox/"+project_name+"/.env","w")
        env_file.write("DB_NAME='' \nDB_USER='' \nDB_PASSWORD='' \nDB_HOST='' \nDB_PORT=''")



if rest_framework and pagination:
    rest_framework_string = "\nREST_FRAMEWORK = {\n    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',\n    'PAGE_SIZE': "+str(page_size)+"\n}"
    settings_data = settings_data + rest_framework_string
print(settings_data)