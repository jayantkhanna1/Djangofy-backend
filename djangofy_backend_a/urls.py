from . import views
from django.urls import path

urlpatterns = [
    path('getZip',views.getZip,name='getZip'),
    path('userSignup',views.user_signup,name='userSignup'),
    path('userVerify',views.user_verify,name='userverify'),
    path('userLogin',views.user_login,name='userLogin'),
    path('forgotPassword',views.forgot_password,name='forgotPassword'),
    path('resetPassword',views.reset_password,name='resetPassword'),
]
