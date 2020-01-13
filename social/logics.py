import datetime

from common import keys
from libs.cache import rds
from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friend


def rcmd_from_rds(uid):
    '''取出优先推荐队列的用户'''
    uid_list = rds.lrange(keys.FIRST_RCMD_K % uid, 0, 29)
    uid_list = [int(uid) for uid in uid_list]
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num):
    '''通过数据库推荐用户'''
    # 获取当前用户的交友资料
    profile, _ = Profile.objects.get_or_create(id=uid)

    # 计算出生日期的范围
    today = datetime.date.today()
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    # 取出滑过的所有的用户 ID
    # select sid from swiped where uid=1;
    sid_list = list(Swiped.objects.filter(uid=uid).values_list('sid', flat=True)) + [uid]

    # 根据条件匹配要推荐的用户
    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    ).exclude(id__in=sid_list)[:num]

    # 返回最终结果
    return users


def rcmd(uid):
    '''用户推荐接口'''
    first_users = rcmd_from_rds(uid)  # 首先取出优先推荐队列中的用户
    num = len(first_users)
    if num >= 30:
        # 如果数量满足 30 个，直接返回结果
        return first_users
    else:
        # 数量不足 30 个，从 DB 中补齐
        other_users = rcmd_from_db(uid, 30 - num)
        users = first_users | other_users  # 将两部分的结果拼接到一起
        return users


def like_someone(uid, sid):
    '''右滑：喜欢某人'''
    # 添加一条滑动记录
    Swiped.swipe(uid, sid, 'like')

    # 强制从自己优先队列删除 sid
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    # 检查是否对方是否右滑或上滑过自己
    if Swiped.has_liked(sid, uid):
        # 匹配成好友关系
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''上滑：喜欢某人'''
    # 添加一条滑动记录
    Swiped.swipe(uid, sid, 'superlike')

    # 强制从自己优先队列删除 sid
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    # 检查是否对方是否右滑或上滑过自己
    if Swiped.has_liked(sid, uid):
        # 匹配成好友关系
        Friend.make_friends(uid, sid)
        return True
    else:
        # 将自己的 UID 添加到对方的优先推荐队列
        rds.rpush(keys.FIRST_RCMD_K % sid, uid)
        return False
