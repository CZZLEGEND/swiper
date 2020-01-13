from common import stat
from libs.http import render_json
from social import logics


def rcmd_users(request):
    '''推荐用户'''
    users = logics.rcmd(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''右滑：喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def superlike(request):
    '''上滑：超级喜欢'''
    sid = int(request.POST.get('sid'))



def dislike(request):
    '''左滑：不喜欢'''
    sid = int(request.POST.get('sid'))
