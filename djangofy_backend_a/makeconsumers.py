import textwrap
class CreateConsumers:
    def __init__(self,socket,apps,project_name):
        self.socket = socket
        self.project_name = project_name
        self.apps = []
        i=1
        for app in apps:
            self.apps.append(app["app_name_"+str(i)])
            i+=1

    def makeConsumers(self):
        if self.socket:
            try:
                for app in self.apps:
                    app = app.replace("'","")
                    file = open("sandbox/"+self.project_name+"/"+str(app)+"/consumers.py","w")
                    consumers_txt = '''
from channels.generic.websocket import AsyncWebsocketConsumer
class TranscribeASR(AsyncWebsocketConsumer):
    async def connect(self):
        print("Incoming connection request")
        await self.accept()

    async def disconnect(self, close_code):
        pass
        
    async def receive(self, text_data):
        pass
'''
                    file.write(consumers_txt)
                    file.close()
            except:
                return False
        return True
