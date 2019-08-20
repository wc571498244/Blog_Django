from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from captcha.models import CaptchaStore

from article.models import Article, Tag
from user.forms import RegisterForm, LoginForm, forgetPasswordForm
from user.models import UserProfile
from user.util import send_email, save_img, upload_to_ali


def get_index_info():
    context = {}
    # news-box里面的文章内容
    news_info = Article.objects.all().order_by("click_num")[:4]
    context['new_info'] = news_info
    # 轮播图里面的内容
    carousels = Article.objects.all().order_by("-date")[:3]
    context['carousels'] = carousels
    # 文章列表
    article_list = Article.objects.all().order_by("-date")[:10]
    context['article_list'] = article_list
    # 点击排行
    click_rank = Article.objects.all().order_by("-click_num")[:8]
    context["click_rank"] = click_rank
    # 收藏排行
    love_rank = Article.objects.all().order_by("-love_num")[:8]
    context["love_rank"] = love_rank
    # pics盒子里面的内容
    pics_list = Article.objects.all().order_by("-love_num")[:3]
    context["pics_list"] = pics_list
    # 右边边的内容
    right_list = Article.objects.all()[:2]
    context["right_list"] = right_list
    # 文章分类
    tags = Tag.objects.all()
    context["tags"] = tags
    return context


def index(request):
    context = {}
    context.update(get_index_info())
    return render(request, 'index.html', context=context)


# 登录
def user_login(request):
    context = {}
    if request.method == "GET":
        form = LoginForm()
        context['form'] = form
        return render(request, "user/login.html", context=context)
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # 方式一： 没有继承AbstractUser的用户使用这种方法
            """
            # 进行数据库查询
            user = UserProfile.objects.filter(username=username).first()
            # 判断密码是否正确
           flag = check_password(password, user.password)
           if flag:
               # 保存登录的session信息
               request.session['username'] = username
               # 跳转到主页
           """
            context.update(get_index_info())
            context["msg"] = 'loginSuccess'
            # 方式二： 继承了AbstractUser的用户 可以使用
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # 将用户对象保存到底层的request中(session)
                return render(request, "index.html", context=context)
        return render(request, "user/login.html", context={
            "form": form,
            "msg": "login_error"
        })


# 注销
def user_logout(request):
    # 方式一： 没有继承AbstractUser的用户  必须使用这种方式
    # request.session.clear() # 删除的是字典里面的内容
    # request.session.flush()  # 删除django_session + cookie + 字典（数据库中的数据也删除）

    # 方式二： 继承了AbstractUser的用户 可以使用系统自带的注销方法
    context = {}
    context.update(get_index_info())
    context["msg"] = 'logoutSuccess'
    logout(request)
    return render(request, "index.html", context=context)


# 注册
def register(request):
    # get请求显示注册表单
    if request.method == "GET":
        return render(request, "user/register.html")
    # post请求提交表单
    else:
        # 通过ModelForm表单验证
        form = RegisterForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            # 查询数据库中是否已存在相同用户名和邮箱的账户
            user = UserProfile.objects.filter(Q(username=username) | Q(email=email)).exists()
            # 如果不存在，则可以注册
            if not user:
                # 给password加密
                password = make_password(password)
                user = UserProfile.objects.create(username=username, password=password, email=email)
                if user:
                    form = LoginForm()
                    return render(request, "user/login.html", context={
                        "msg": "success",
                        'form': form
                    })
            else:
                return render(request, "user/register.html", context={
                    'msg': "用户名或邮箱已存在"
                })

        else:
            return render(request, 'user/register.html', context={
                "msg": "注册失败请重新填写",
                "form": form
            })


# 忘记密码
def forgetPassword(request):
    context = {}
    context.update(get_index_info())
    if request.method == "GET":
        form = forgetPasswordForm()
        return render(request, "user/forgetPassword.html", context={
            "form": form
        })
    else:
        form = forgetPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            if UserProfile.objects.filter(email=email).exists():
                # 验证成功之后给邮箱发送修改密码的链接
                if send_email(request, email):
                    context["msg"] = 'send_email_success'
                    return render(request, "index.html", context=context)
                else:
                    return render(request, "user/update_pwd.html", context={
                        "msg": "send_email_error"
                    })
            return render(request, "user/forgetPassword.html", context={
                "msg": "该邮箱没有注册",
                "form": form
            })
        else:
            return render(request, "user/forgetPassword.html", context={
                "form": form
            })


# 修改密码
def update_pwd(request):
    context = {}
    context.update(get_index_info())
    if request.method == "GET":
        # 获取url上面uuid   也就是user.id
        uuid = request.GET.get('uuid')
        uid = request.session.get(uuid)
        if uid:
            return render(request, "user/update_pwd.html", context={
                "uuid": uuid  # 传入到模板中 利用input[hidden]隐藏用户的uuid
            })
        else:
            context["msg"] = 'updated'
            return render(request, "index.html", context=context)
    else:
        password = request.POST['password']
        repassword = request.POST["repassword"]
        uuid = request.POST.get("uuid")  # 获取input[hidden]中的uuid
        uid = request.session.get(uuid)  # 得到uuid之后  从session中获取uuid中的值（就是user.id）
        if uid:
            if password == repassword:
                user = UserProfile.objects.filter(pk=uid).first()
                # 密码必须加密之后才能修改数据库
                password = make_password(password)
                user.password = password
                user.save()
                # 密码修改成功之后，清除session(uuid)不让其再进入此地址改密码
                request.session.clear()
                form = LoginForm()
                return render(request, "user/login.html", context={
                    "msg": "update_success",
                    "form": form
                })
            else:
                return render(request, "user/update_pwd.html", context={
                    "msg": "update_error"
                })
        else:
            context['msg'] = "updated"
            return render(request, "index.html", context=context)


# ajax刷新验证码
def ajax_val(request):
    """
        由于ajax请求提交上来的输入验证码中的数据在response变量中，hashkey在hashkey中

        验证码生成之后数据库中会生成对应的数据在(CaptchaStore)表中
            而 response 字段的值就是验证码的字符（小写）   challenge也是验证码的字符(大写)
    """
    if request.is_ajax():
        cs = CaptchaStore.objects.filter(response=request.GET['response'], hashkey=request.GET['hashkey'])
        # 如果配置成功则返回status标志为1    失败则返回0
        if cs:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}
        # 把json数据返回到前端
        return JsonResponse(json_data)
    else:
        # raise Http404
        json_data = {'status': 0}
        return JsonResponse(json_data)


# 个人中心以及修改(图片上传到云存储)
@login_required
def perInfo(request):
    userInfo = request.user  # 获取登录的用户
    if request.method == 'GET':
        return render(request, "user/perInfo.html", context={
            "userInfo": userInfo
        })
    else:
        username = request.POST['username']
        email = request.POST['email']
        icon = None
        try:
            icon = request.FILES['icon']  # 获取文件上传的文件名
        except:
            pass
        # 修改个人信息
        if username:
            userInfo.username = username
        if email:
            userInfo.email = email
        # 上传图片到阿里云, 如果成功获取到图片
        if icon:
            filename = upload_to_ali(icon)
            userInfo.yunIcon = filename
        # 保存到数据库
        userInfo.save()
        return render(request, "user/perInfo.html", context={
            "userInfo": userInfo
        })
