from django.http import JsonResponse

from user import logics
from common import stat


def get_vcode(request):
    '''用户获取验证码'''
    phonenum = request.GET.get('phonenum')
    success = logics.send_sms(phonenum)
    if success:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.SMS_ERR, 'data': None})


def submit_vcode(request):
    return JsonResponse({})


def get_profile(request):
    return JsonResponse({})


def set_profile(request):
    return JsonResponse({})


def upload_avatar(request):
    return JsonResponse({})
