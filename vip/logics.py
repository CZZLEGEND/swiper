def need_permission(perm_name):
    '''检查用户是否具有某种权限'''
    def deco(view_func):
        def wrapper(request, *args, **kwargs):
            # 先检查过期时间
            # 再检查是否具有权限
            pass
        return wrapper
    return deco
