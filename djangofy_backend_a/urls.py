from . import views
from django.urls import path

urlpatterns = [
    path('getZip',views.getZip,name='getZip'),
    path('userSignup',views.user_signup,name='userSignup'),
    path('userVerify',views.user_verify,name='userverify'),
    path('userLogin',views.user_login,name='userLogin'),
    path('forgotPassword',views.forgot_password,name='forgotPassword'),
    path('resetPassword',views.reset_password,name='resetPassword'),
    path('githubLogin',views.github_login,name='githubLogin'),
    path('githubConfirm',views.github_confirm,name='githubConfirm'),
    path('githubCallback',views.github_callback,name='githubCallback'),

    # mail server
    path('sendMail',views.mail_server,name = "sendMail")
]
