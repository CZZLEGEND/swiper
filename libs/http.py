import json

from django.http import HttpResponse
from django.conf import settings

from common import stat


def render_json(data=None, code=stat.OK):
    '''渲染需要的 JSON 数据'''
    result = {
        'data': data,
        'code': code
    }

    if settings.DEBUG:
        # 调试模式的格式
        json_data = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        # 生产环境的格式
        json_data = json.dumps(result, ensure_ascii=False, separators=(',', ':'))

    return HttpResponse(json_data)
