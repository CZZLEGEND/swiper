import os

from django.http import JsonResponse
from django.core.cache import cache

from user.models import User
from user.models import Profile
from user.forms import UserForm
from user.forms import ProfileForm
from user import logics
from common import stat
from libs.qncloud import upload_to_qn


def get_vcode(request):
    '''用户获取验证码'''
    phonenum = request.GET.get('phonenum')
    success = logics.send_sms(phonenum)
    if success:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.SMS_ERR, 'data': None})


def submit_vcode(request):
    '''检查短信验证码，同时进行登陆或者注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    key = 'Vcode-%s' % phonenum
    cached_vcode = cache.get(key)
    if vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)  # 获取用户
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)  # 创建新用户

        # 记录用户登陆状态
        request.session['uid'] = user.id
        return JsonResponse({'code': stat.OK, 'data': user.to_dict()})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def get_profile(request):
    '''获取用户配置'''
    profile, _ = Profile.objects.get_or_create(id=request.uid)
    return JsonResponse({'code': stat.OK, 'data': profile.to_dict()})


def set_profile(request):
    '''修改用户信息，及用户配置'''
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 验证 user 表单的数据
    if not user_form.is_valid():
        return JsonResponse({'code': stat.USER_FORM_ERR, 'data': user_form.errors})
    # 验证 profile 表单的数据
    if not profile_form.is_valid():
        return JsonResponse({'code': stat.PROFILE_FORM_ERR, 'data': profile_form.errors})

    # 修改用户数据
    # update user set nickname='xx', gender='male' where id=uid;
    User.objects.filter(id=request.uid).update(**user_form.cleaned_data)

    # 修改 profile 数据
    Profile.objects.update_or_create(id=request.uid, defaults=profile_form.cleaned_data)

    return JsonResponse({'code': stat.OK, 'data': None})


def upload_avatar(request):
    '''上传个人形象'''
    # 1. 接受用户图片，保存到本地
    avatar_file = request.FILES.get('avatar')
    filepath, filename = logics.save_tmp_file(avatar_file)

    # 2. 上传到七牛云
    url = upload_to_qn(filepath, filename)

    # 3. 更新用户的 avatar 字段
    User.objects.filter(id=request.uid).update(avatar=url)

    # 4. 删除本地的临时文件
    os.remove(filepath)

    return JsonResponse({'code': stat.OK, 'data': None})
