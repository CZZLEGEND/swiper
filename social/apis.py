from django.http import JsonResponse

from common import stat
from social import logics


def rcmd_users(request):
    '''推荐用户'''
    users = logics.rcmd(request.uid)
    result = [user.to_dict() for user in users]
    return JsonResponse({'code': stat.OK, 'data': result})
