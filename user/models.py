from django.db import models


class User(models.Model):
    '''user 表的数据模型'''
    phonenum = models.CharField(max_length=16, verbose_name='手机号')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    gender = models.CharField(max_length=10, verbose_name='性别')
    birthday = models.DateField(default='1990-01-01', verbose_name='生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=20, verbose_name='常居地')
