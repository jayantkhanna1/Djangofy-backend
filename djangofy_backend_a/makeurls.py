import os

class CreateUrls:
    def __init__(self,project_name,apps):
        self.project_name = project_name
        self.apps = apps

    def makeUrls(self):
        # Editing urls.py file in project
        try:
            print(os.getcwd())
            file = open("sandbox/"+self.project_name + "/" + self.project_name + "/urls.py","r")
            url_data = file.read()
            file.close()
            url_data = url_data.replace("from django.urls import path","from django.urls import path,include")
            url_data = url_data.split("urlpatterns = [")[0]
            url_data += "urlpatterns = [\n"
            for app in self.apps:
                app = app.replace("'","")
                url_data += "    path('"+app+"/',include('"+app+".urls')),\n"
            url_data += "   path('admin/', admin.site.urls),\n"
            url_data += "]\n"
            file = open("sandbox/"+self.project_name + "/" + self.project_name + "/urls.py","w")
            file.write(url_data)
            file.close()
            

            # Editing urls.py file in all apps
            for app in self.apps:
                app = app.replace("'","")
                file = open("sandbox/"+self.project_name + "/" + app + "/urls.py","w")
                file.write("from django.urls import path\n")
                file.write("from . import views\n")
                file.write("\n")
                file.write("urlpatterns = [\n")
                file.write("]\n")
                file.close()

            return True
        except Exception as e:
            print(e)
            return False
            


            