import textwrap
class CreateAsgi:
    def __init__(self,socket,project_name):
        self.socket = socket
        self.project_name = project_name

    def makeAsgi(self):
        if self.socket:
            try:
                socket_str = '''
                import os
                from channels.routing import ProtocolTypeRouter, URLRouter
                from django.core.asgi import get_asgi_application
                from channels.auth import AuthMiddlewareStack
                from channels.security.websocket import AllowedHostsOriginValidator
                from django.urls import path
                from transcription_app.consumers import TranscribeASR, RemoveUser

                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcription_project.settings')
                django_asgi_app = get_asgi_application()
                application = ProtocolTypeRouter({
                    "http": django_asgi_app,
                    "websocket": AllowedHostsOriginValidator(
                        AuthMiddlewareStack(
                            URLRouter([
                                # Add paths here
                            ])
                        )
                    ),
                })

                '''
                file = open("sandbox/"+self.project_name+"/"+self.project_name+"/asgi.py","w")
                file.write(textwrap.dedent(socket_str))
            except:
                return False
        return True
