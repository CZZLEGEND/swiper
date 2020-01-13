from django.db import models


class Swiped(models.Model):
    '''滑动记录'''
    STYPES = (
        ('like', '右滑'),
        ('superlike', '上滑'),
        ('dislike', '左滑'),
    )
    uid = models.IntegerField(verbose_name='用户 ID')
    sid = models.IntegerField(verbose_name='被滑动用户的 ID')
    stype = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动的类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动的时间')

    class Meta:
        unique_together = ('uid', 'sid')  # uid 与 sid 联合唯一


class Friend(models.Model):
    '''好友表'''
    uid1 = models.IntegerField(verbose_name='用户 ID')
    uid2 = models.IntegerField(verbose_name='用户 ID')

    class Meta:
        unique_together = ('uid1', 'uid2')  # uid1 与 uid2 联合唯一
