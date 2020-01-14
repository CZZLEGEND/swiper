from django.db import models
from django.db.utils import IntegrityError

from common import stat


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

    @classmethod
    def swipe(cls, uid, sid, stype):
        '''执行一次滑动'''
        try:
            return cls.objects.create(uid=uid, sid=sid, stype='like')
        except IntegrityError:
            # 不允许重复滑动某人
            raise stat.RepeatSwipeErr

    @classmethod
    def has_liked(cls, uid, sid):
        '''检查是否喜欢 (右滑或者上滑) 过某人'''
        return cls.objects.filter(uid=uid, sid=sid, stype__in=['like', 'superlike']).exists()


class Friend(models.Model):
    '''好友表'''
    uid1 = models.IntegerField(verbose_name='用户 ID')
    uid2 = models.IntegerField(verbose_name='用户 ID')

    class Meta:
        unique_together = ('uid1', 'uid2')  # uid1 与 uid2 联合唯一

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''添加好友关系'''
        # 调整 uid1 和 uid2 的顺序，小的值放前面
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        try:
            return cls.objects.create(uid1=uid1, uid2=uid2)
        except IntegrityError:
            raise stat.AreadyFriends

    @classmethod
    def break_off(cls, uid1, uid2):
        '''绝交'''
        # 调整 uid1 和 uid2 的顺序，小的值放前面
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()
