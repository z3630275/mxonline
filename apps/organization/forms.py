# _*_ coding:utf-8 _*_
__author__ = '111'
__date__ = '2018/1/6 13:17'

import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        regex = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(regex)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
