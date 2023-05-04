class CreateRequirements:
    def __init__(self,project_name,pip_packages,rest_framework,template_based,database,email_backend,mobile_backend,static_backend):
        self.project_name = project_name
        self.pip_packages = pip_packages
        self.rest_framework = rest_framework
        self.template_based = template_based
        self.database = database
        self.email_backend = email_backend
        self.mobile_backend = mobile_backend
        self.static_backend = static_backend


    def makeRequirements(self):
        try:
            req_file = open("sandbox/"+self.project_name+"/requirements.txt","w")
            for package in self.pip_packages:
                req_file.write(package+" \n")
            
            req_file.write("asgiref\nDjango\ndjango-admin\ndjango-excel-response2\ndjango-six\nexcel-base\nisoweek\npython-dateutil\npython-dotenv\npytz-deprecation-shim\nscreen\nsix\nsqlparse\nTimeConvert\ntzdata\ntzlocal\nxlwt\ndjango-cors-headers\nsqlparse\nwhitenoise\ngunicorn\n")

            if self.rest_framework:
                req_file.write("djangorestframework \n")
                req_file.write("django-filter \n")
                req_file.write("django-restframework\n")
                req_file.write("djangorestframework-simplejwt\n")


            if self.template_based:
                req_file.write("Pillow \n")
            
            if self.database.lower() == "postgresql":
                req_file.write("psycopg2-binary \n")
                
            if self.database.lower() == "mysql":
                req_file.write("mysqlclient \n")

            if self.database.lower() == "mongodb":
                req_file.write("djongo \npymongo")
            
            if self.email_backend and self.email_backend.lower() == "sendgrid":
                req_file.write("sendgrid \n")
            
            if self.mobile_backend:
                req_file.write("twilio \n")

            if self.static_backend:
                if self.static_backend.lower() == "aws":
                    req_file.write("django-storages \nboto3 \n")
                if self.static_backend.lower() == "azure":
                    req_file.write("django-storages \nazure-storage-blob \n")
                if self.static_backend.lower() == "gcp":
                    req_file.write("django-storages \ngoogle-cloud-storage \n")
        
            req_file.close()
            return True
        
        except Exception as e:
            print(e)
            return False
        