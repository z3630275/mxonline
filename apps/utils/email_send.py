# _*_ coding:utf-8 _*_
__author__ = '111'
__date__ = '2017/12/25 0:52'

from users.models import EmailVerifyRecord


def send_register_email(email,type=0):
    email_record = EmailVerifyRecord()
    random_str = ''

def generate_random_str(randomlength=8):
    str=""
    chars =""