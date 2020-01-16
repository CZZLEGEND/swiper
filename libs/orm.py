from datetime import date, time, datetime

from django.db import models
from django.db.models import query

from libs.cache import rds
from common.keys import MODEL_K


def get(self, *args, **kwargs):
    """
    Performs the query and returns a single object matching the given
    keyword arguments.
    """
    cls_name = self.model.__name__  # 取出当前操作的 Model 类的名字
    # 检查 kwargs 中是否存在主键
    pk = kwargs.get('pk') or kwargs.get('id')
    if pk:
        # 从缓存获取数据
        key = MODEL_K % (cls_name, pk)
        model_obj = rds.get(key)
        # 检查缓存的结果
        if isinstance(model_obj, self.model):
            return model_obj

    # 缓存不存在时, 调用原 get 接口从数据库获取数据
    model_obj = self._get(*args, **kwargs)

    # 将数据写入缓存
    key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(key, model_obj)

    return model_obj


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
    Saves the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    # 调用原 save 方法，将数据保存到数据库
    self._save(force_insert, force_update, using, update_fields)

    # 将数据保存到 缓存
    key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(key, self)


def to_dict(self, *exclude):
    '''将 Model 模型转换成一个字典'''
    attr_dict = {}
    for field in self._meta.fields:
        if field.name in exclude:
            continue

        key = field.name
        value = getattr(self, key)
        if isinstance(value, (date, time, datetime)):
            value = str(value)

        attr_dict[key] = value

    return attr_dict


def patch_model():
    '''通过 Monkey Patch (猴子补丁) 的方式为 Django 的 ORM 增加统一的缓存处理'''
    # 修改 get 方法
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    # 修改 save 方法
    models.Model._save = models.Model.save
    models.Model.save = save

    # 统一为所有的 Model 增加 to_dict 方法
    models.Model.to_dict = to_dict
