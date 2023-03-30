class CreateAdmin:
    def __init__(self,project_name,apps,models):
        self.project_name = project_name
        self.apps = apps
        self.models = models
    
    def makeAdmin(self):
        try:
            for app in self.apps:
                app = app.replace("'","")
                admin_file = open("sandbox/"+self.project_name+"/"+app+"/admin.py","w")
                admin_file.write("from django.contrib import admin \n")
                admin_file.write("from .models import * \n\n")
                for model in self.models:
                    if model["app_name"] == app:
                        models = model["models"]
                        for y in models:
                            admin_file.write("admin.site.register("+y["model_name"]+") \n")
                admin_file.close()
            return True
        except Exception as e:
            print(e)
            return False