from django.db import models


class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=16, verbose_name='会员名称')
    level = models.IntegerField(default=0, verbose_name='会员等级')
    duration = models.IntegerField(default=0, verbose_name='购买的时长')
    price = models.FloatField(default=0, verbose_name='会员价格')


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=16, verbose_name='权限名称')
    description = models.TextField(verbose_name='权限描述信息')


class VipPermRelation(models.Model):
    vip_level = models.IntegerField(verbose_name='会员等级')
    perm_id = models.IntegerField(verbose_name='权限ID')
