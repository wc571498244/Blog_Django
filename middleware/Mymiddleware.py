from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
# 使用中间件来限制没有登录的用户访问
login_list = ['/user/perInfo']  # 没有登录的限制列表


class Middleware1(MiddlewareMixin):
    # 重写request方法
    def process_request(self, request):
        if request.path in login_list:
            if not request.user.is_authenticated:
                return render(request, "user/login.html", context={
                    "msg": "NotLogin"
                })
