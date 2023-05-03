class CreateAdmin:
    def __init__(self,project_name,apps):
        self.project_name = project_name
        self.apps = apps
        # for app in apps:
        #     self.apps.append(app["app_name"])
        # self.models = []
        # for app in apps:
        #     temp_model = {
        #         "app_name":app["app_name"],
        #         "models":app["modals"]
        #     }
        #     self.models.append(temp_model)
    
    def makeAdmin(self):
        try:
            i=1
            for x in self.apps:
                file = open("sandbox/"+self.project_name + "/" + x["app_name_"+str(i)] + "/admin.py","w")
                file.write("from django.contrib import admin \n")
                for model in x["modals"]:
                    file.write("from .models import "+model["name"]+"\n")
                file.write("\n")
                for model in x["modals"]:
                    file.write("admin.site.register("+model["name"]+")\n")
                file.close()                
                i+=1
            return True
        except Exception as e:
            print(e)
            return False