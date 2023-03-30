class CreateModels:
    def __init__(self,project_name,apps,models):
        self.project_name = project_name
        self.apps = apps
        self.models = models

    def getModel(self,app):
        for x in self.models:
            if x['app_name'] == app:
                return x['models']
        return []
    
    def makeModels(self):
        # editing models.py in all apps and creating models
        for app in self.apps:
            app = app.replace("'","")
            file = open("sandbox/"+self.project_name + "/" + app + "/models.py","w")
            file.write("from django.db import models \n")
            models = self.getModel(app)
            for x in models:
                modal_name = x['model_name']
                fields = x['fields']
                file.write("class "+modal_name+"(models.Model):\n")
                for y in fields:
                    field_name = y['field_name']
                    field_type = y['field_type']
                    file.write("    "+field_name+" = "+field_type+"\n")
            file.close()

        return True