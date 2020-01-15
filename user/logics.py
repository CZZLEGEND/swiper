import os
import random
import logging
from uuid import uuid4

import requests
from django.core.cache import cache

from swiper import conf
from common import keys
from user.models import User
from libs.qncloud import upload_to_qn
from tasks import celery_app

inf_log = logging.getLogger('inf')


def gen_rand_code(length=6):
    '''产生指定长度的随机码'''
    chars = []
    for i in range(length):
        chars.append(str(random.randint(0, 9)))
    return ''.join(chars)


def send_sms(mobile):
    '''发送短信验证码'''
    key = keys.VCODE_K % mobile

    # 检查短信发送状态，防止短时间内给用户重复发送短信
    if cache.get(key):
        return True  # 之前发送过验证码，直接返回 True

    vcode = gen_rand_code()  # 产生验证码
    inf_log.info('验证码: %s' % vcode)

    args = conf.YZX_SMS_ARGS.copy()  # 原型模式
    args["param"] = vcode
    args["mobile"] = mobile

    response = requests.post(conf.YZX_SMS_API, json=args)
    if response.status_code == 200:
        result = response.json()
        inf_log.info('短信发送状态: %s' % result.get('msg'))
        if result.get('code') == '000000':
            cache.set(key, vcode, 600)  # 给用户多预留一些时间
            return True
        else:
            return False
    return False


def save_tmp_file(tmp_file):
    '''保存临时文件'''
    tmp_filename = uuid4().hex
    tmp_filepath = '/tmp/%s' % tmp_filename
    with open(tmp_filepath, 'wb') as fp:
        for chunk in tmp_file.chunks():
            fp.write(chunk)
    return tmp_filepath, tmp_filename


@celery_app.task
def save_avatar(uid, avatar_file):
    '''保存用户形象图片'''
    filepath, filename = save_tmp_file(avatar_file)

    # 2. 上传到七牛云
    url = upload_to_qn(filepath, filename)

    # 3. 更新用户的 avatar 字段
    User.objects.filter(id=uid).update(avatar=url)

    # 4. 删除本地的临时文件
    os.remove(filepath)
