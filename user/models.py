import datetime

from django.db import models

from vip.models import Vip


class User(models.Model):
    '''user 表的数据模型'''
    GENDERS = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('成都', '成都'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('沈阳', '沈阳'),
    )
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    gender = models.CharField(max_length=10, default='male', choices=GENDERS, verbose_name='性别')
    birthday = models.DateField(default='1990-01-01', verbose_name='生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象的URL')
    location = models.CharField(max_length=20, default='北京', choices=LOCATION, verbose_name='常居地')

    vip_id = models.IntegerField(default=1, verbose_name='用户对应的会员ID')
    vip_end = models.DateTimeField(default='2100-01-01', verbose_name='会员过期时间')

    def __str__(self):
        return str(self.id)

    @property
    def vip(self):
        '''用户对应的 VIP Model'''
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def check_vip_end_time(self):
        '''检查VIP过期时间，如果过期，自动修改为普通用户身份'''
        if self.vip_id != 1:
            if datetime.datetime.now() >= self.vip_end:
                self.vip_id = 1
                self.save()


class Profile(models.Model):
    '''个人的配置及交友资料'''
    dating_gender = models.CharField(max_length=10, default='female', choices=User.GENDERS,
                                     verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=20, default='北京', choices=User.LOCATION,
                                       verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让未匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')
