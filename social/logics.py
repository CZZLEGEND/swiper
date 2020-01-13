import datetime

from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friend


def rcmd(uid):
    '''用户推荐接口'''
    # 获取当前用户的交友资料
    profile, _ = Profile.objects.get_or_create(id=uid)

    # 计算出生日期的范围
    today = datetime.date.today()
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    # 取出滑过的所有的用户 ID
    # select sid from swiped where uid=1;
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 根据条件匹配要推荐的用户
    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    ).exclude(id__in=sid_list)[:30]

    # 返回最终结果
    return users


def like_someone(uid, sid):
    '''右滑：喜欢某人'''
    # 添加一条滑动记录
    Swiped.swipe(uid, sid, 'like')

    # 检查是否对方是否右滑或上滑过自己
    if Swiped.has_liked(sid, uid):
        # 匹配成好友关系
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_some():
    pass
