from common import stat
from libs.http import render_json
from social import logics


def rcmd_users(request):
    '''推荐用户'''
    users = logics.rcmd(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)
