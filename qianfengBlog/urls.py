"""qianfengBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

import xadmin
from qianfengBlog.settings import MEDIA_ROOT
from user.views import index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path("", index, name="index"),
    path('user/', include("user.urls", namespace='user')),
    path("article/", include("article.urls", namespace="article")),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 图片上传路径
    re_path(r'mdeditor/', include('mdeditor.urls')),  # markdown文件上传的路径
]
# 部署的时候收集静态文件
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
