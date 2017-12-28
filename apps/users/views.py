from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .models import UserProfile
from users.forms import LoginForm, RegisterForm
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
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user_profile=UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.password = make_password(password)
            user_profile.save()

            send_register_email(username,send_type="register")

            return render(request, 'login.html')
        else:
            return render(request, 'register.html',{"register_form":register_form})


class LoginView(View):
    # 基于类登录，View可以定义中get，post方法http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    def post(self, request):
        login_form = LoginForm(request.POST)  # 登录之前实例化时以对每个字段做验证，不进数据库查询
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username,
                                password=password)  # 向数据库发起认证，密码与用户名是否正确，必须指明参数名，可直接调用自定义方法custom下authenticate方法。
            if user is not None:
                login(request, user)  # 登录，向request中写入数据 再render，随后将user和request注册到html中，user放到request中
                return render(request, 'index.html')

        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})

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
