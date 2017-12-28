# _*_ coding:utf-8 _*_
__author__ = '111'
__date__ = '2017/12/24 19:04'
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': '请输入正确的邮箱格式'})
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})
