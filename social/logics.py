import datetime

from common import keys
from common import stat
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
    sid_list = list(Swiped.objects.filter(uid=uid).values_list('sid', flat=True))
    sid_list += [uid]  # 防止自身被筛选出来

    # 根据条件匹配要推荐的用户
    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    ).exclude(id__in=sid_list)[:num]  # 懒加载

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


def dislike_someone(uid, sid):
    '''左滑 (不喜欢) 某人'''
    # 添加一条滑动记录
    Swiped.swipe(uid, sid, 'dislike')

    # 强制从自己优先队列删除 sid
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)


def rewind_last_swipe(uid):
    '''
    反悔最后一次的滑动

    - 每天允许反悔 3 次
    - 反悔的记录只能是五分钟之内的
    '''
    # 取出当前时间
    now = datetime.datetime.now()

    # 检查当前是否达到了 3 次
    key = keys.REWIND_K % (now.date(), uid)
    rewind_times = rds.get(key, 0)  # 取出当天的反悔次数，默认为 0 次
    if rewind_times >= 3:
        raise stat.RewindLimited  # 当天达到额定次数: 直接给用户提示

    latest_swipe = Swiped.objects.filter(uid=uid).latest('stime')  # 找到最后一次的滑动记录

    # 对比当前时间和最后一次的滑动时间，差值是否在五分钟内
    passed_time = (now - latest_swipe.stime).total_seconds()  # 计算距离上一次滑动已经过去的秒数
    if passed_time >= 300:
        raise stat.RewindTimeout  # 超过 5 分钟，直接给用户提示

    # 撤销滑动式可能受影响的其他相关数据
    # 好友关系删掉
    if latest_swipe.stype in ['like', 'superlike']:
        Friend.break_off(uid, latest_swipe.sid)

        # 优先推荐队列里的数据删掉
        if latest_swipe.stype == 'superlike':
            rds.lrem(keys.FIRST_RCMD_K % latest_swipe.sid, 1, uid)

    # 删除最后一次滑动记录
    latest_swipe.delete()

    # 全部完成后，累加反悔次数
    rds.set(key, rewind_times + 1, 86400 * 2)  # 过期时间是为了让当天的反悔次数自然消失


def who_liked_me(uid):
    '''找到喜欢过自己，并且我还没有滑过对方的人'''
    # 取出滑过的所有的用户 ID
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 右滑或者上滑过自己的用户的 UID
    uid_list = Swiped.objects.filter(sid=uid, stype__in=['like', 'superlike']) \
                             .exclude(uid__in=sid_list) \
                             .values_list('uid', flat=True)

    # 取出喜欢过自己的用户数据
    users = User.objects.filter(id__in=uid_list)
    return users
