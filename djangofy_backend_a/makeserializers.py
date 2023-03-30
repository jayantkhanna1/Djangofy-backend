class CreateSerializers:
    def __init__(self,project_name,apps,models) -> None:
        self.project_name = project_name
        self.apps = apps
        self.models = models

    def makeSerializers(self):
        try:
            for app in self.apps:
                app = app.replace("'","")
                serializers_file = open("sandbox/"+self.project_name+"/"+app+"/serializers.py","w")
                serializers_file.write("from rest_framework import serializers \n")
                serializers_file.write("from .models import * \n")
                for model in self.models:
                    if model["app_name"] == app:
                        models = model["models"]
                        for y in models:
                            serializers_file.write("class "+y["model_name"]+"Serializer(serializers.ModelSerializer): \n")
                            serializers_file.write("    class Meta: \n")
                            serializers_file.write("        model = "+y["model_name"]+" \n")
                            serializers_file.write("        fields = '__all__' \n")
                serializers_file.close()
            return True
        except Exception as e:
            print(e)
            return False
                                       