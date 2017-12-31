from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from  utils.email_send import send_register_email


# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 不能查密码，django存储密码是密文，前端传过来是明文
            if user.check_password(password):  # 明文密码加密后与user下的密码进行对比操作
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')  # 不能用实例查询
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'msg': '注册用户已存在', "register_form": register_form})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            send_register_email(username, send_type="register")

            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})


class ActiveView(View):  # 激活
    def get(self, request, active_code):
        all_codes = EmailVerifyRecord.objects.filter(code=active_code)  # filter is list
        if all_codes:
            for code in all_codes:
                email = code.email
                users = UserProfile.objects.filter(email=email)
                for user in users:
                    user.is_active = True
                    users.save()
        else:
            # return render(request, 'active_fail.html')
            return HttpResponse("<h1>链接已经失效，请输入正确的网址!!!!</h1>")
        return render(request, 'login.html')


class LoginView(View):
    # 基于类登录，View可以定义中get，post方法http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    def post(self, request):
        login_form = LoginForm(request.POST)  # 登录之前实例化时以对每个字段做验证，不进数据库查询
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username,  # 此时已调用自定义验证方法
                                password=password)  # 向数据库发起认证，密码与用户名是否正确，必须指明参数名，可直接调用自定义方法custom下authenticate方法。
            if user is not None:
                if user.is_active:
                    login(request, user)  # 登录，向request中写入数据 再render，随后将user和request注册到html中，user放到request中
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html',{'msg': '用户未激活'})  # 如返回It returned None instead 有个else条件未render
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})

        else:
            return render(request, 'login.html', {'login_form': login_form})

    def get(self, request):
        return render(request, 'login.html')


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html',{'msg':'用户名或密码错误'})
#
#     elif request.method == 'GET':
#         return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()  # 获取验证码
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, send_type='forget')
            # return render(request, 'send_success.html')
            return HttpResponse('邮件已发送成功.......')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_codes = EmailVerifyRecord.objects.filter(code=active_code)  # filter is list
        if all_codes:
            for code in all_codes:
                email = code.email
                return render(request, 'password_reset.html', {'email': email})  # 确定是哪个用户
        else:
            # return render(request, 'active_fail.html')
            return HttpResponse("<h1>链接已经失效，请输入正确的网址!!!!</h1>")
        return render(request, 'login.html')


class ModifyView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password1', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})
