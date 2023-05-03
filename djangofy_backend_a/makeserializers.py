class CreateSerializers:
    def __init__(self,project_name,apps) -> None:
        self.project_name = project_name
        self.apps = apps

    def makeSerializers(self):
        # try:
        #     for app in self.apps:
        #         app = app.replace("'","")
        #         serializers_file = open("sandbox/"+self.project_name+"/"+app+"/serializers.py","w")
        #         serializers_file.write("from rest_framework import serializers \n")
        #         serializers_file.write("from .models import * \n")
        #         for model in self.models:
        #             if model["app_name"] == app:
        #                 models = model["models"]
        #                 for y in models:
        #                     serializers_file.write("class "+y["name"]+"Serializer(serializers.ModelSerializer): \n")
        #                     serializers_file.write("    class Meta: \n")
        #                     serializers_file.write("        model = "+y["name"]+" \n")
        #                     serializers_file.write("        fields = '__all__' \n")
        #         serializers_file.close()
        #     return True
        # except Exception as e:
        #     print(e)
        #     return False
    
        try:
            i=1
            for x in self.apps:
                file = open("sandbox/"+self.project_name + "/" + x["app_name_"+str(i)] + "/serializers.py","w")
                file.write("from rest_framework import serializers \n")
                for model in x["modals"]:
                    file.write("from .models import "+model["name"]+"\n")
                file.write("\n")
                for model in x["modals"]:
                    file.write("class "+model["name"]+"Serializer(serializers.ModelSerializer): \n")
                    file.write("    class Meta: \n")
                    file.write("        model = "+model["name"]+" \n")
                    file.write("        fields = '__all__' \n")
                file.close()
                
                i+=1
            return True
        except Exception as e:
            print(e)
            return False
                                       