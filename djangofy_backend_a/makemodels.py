class CreateModels:
    def __init__(self,project_name,apps):
        self.apps = apps
        self.project_name = project_name
    
    def makeModels(self):
        try:
            i=1
            for x in self.apps:
                file = open("sandbox/"+self.project_name + "/" + x["app_name_"+str(i)] + "/models.py","w")
                file.write("from django.db import models \n")
                for model in x["modals"]:
                    file.write("class "+model["name"]+"(models.Model):\n")
                    for field in model["fields"]:
                        file.write("    "+field["name"]+" = "+field["type"]+"\n")
                file.close()
                
                i+=1
            return True
        except Exception as e:
            print(e)
            return False
    