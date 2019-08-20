from django.urls import path, re_path

from user import views

# 应用命名空间
app_name = "user"

urlpatterns = [
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("register/", views.register, name="register"),
    path("forgetPassword/", views.forgetPassword, name="forgetPassword"),
    re_path('^ajax_val/', views.ajax_val, name='ajax_val'),  # ajax验证
    path("update_pwd/", views.update_pwd, name="update_pwd"),
    path("perInfo/", views.perInfo, name="perInfo"),  # 云存储
]
