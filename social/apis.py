from common import stat
from libs.http import render_json
from social import logics
from social.models import Friend
from user.models import User
from vip.logics import need_permission


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


@need_permission('superlike')
def superlike(request):
    '''上滑：超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''左滑：不喜欢'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    return render_json()


@need_permission('rewind')
def rewind(request):
    '''反悔'''
    logics.rewind_last_swipe(request.uid)
    return render_json()


@need_permission('who_liked_me')
def show_who_liked_me(request):
    '''查看都有谁喜欢过我的人'''
    users = logics.who_liked_me(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def friend_list(request):
    '''获取自己的好友列表'''
    friend_id_list = Friend.get_my_friends_id(request.uid)
    friends = User.objects.filter(id__in=friend_id_list)
    result = [user.to_dict() for user in friends]
    return render_json(result)


def hot_rank(request):
    '''全服人气热度排行榜'''
    rank_data = logics.get_top_n(50)
    return render_json(rank_data)
