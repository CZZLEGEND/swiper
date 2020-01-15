from common import stat
from user.models import User


def need_permission(perm_name):
    '''检查用户是否具有某种权限'''
    def deco(view_func):
        def wrapper(request, *args, **kwargs):
            # 检查用户的 VIP 过期时间
            user = User.objects.get(id=request.uid)
            user.check_vip_end_time()

            # 检查用户是否具有需要的权限
            if user.vip.has_perm(perm_name):
                return view_func(request, *args, **kwargs)
            else:
                raise stat.PermRequired
        return wrapper
    return deco
