'''
请求进入 Django 之后的处理流程

1. HTTP Server 接收浏览器发送的 “请求报文”
2. WSGI 将 “请求报文” 封装成 HttpReqeust 对象
   -------------------------------------------------------> process_request
3. Django 进行 URL 匹配，找到对应的 view 函数
   -------------------------------------------------------> process_view
4. view 函数进行处理:
    1. 获取参数
    2. 调用数据库、缓存
    3. 调用其他程序逻辑
       ---------------------------------------------------> process_template
    4. 进行模板渲染
    5. 将运算结果封装成一个 HttpResponse 对象
    ------------------------------------------------------> process_exception
   -------------------------------------------------------> process_response
5. WSGI 将 HttpResponse 对象封装成 “响应报文”
6. HTTP Server 将 “响应报文” 发送给浏览器
7. HTTP Server 关闭与浏览器的网络连接

关于 WSGI:

    HTTP Server (Socket 服务器，控制网络连接，接收、发送数据)
    | ^
    V |
    WSGI
    | ^
    V |
    Web App (Django / Flask / Tornado)
'''
import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from libs.http import render_json
from common import stat

err_log = logging.getLogger('err')

class AuthMiddleware(MiddlewareMixin):
    '''登陆检查中间件'''
    white_list = (
        '/api/user/get_vcode',
        '/api/user/submit_vcode',
    )

    def process_request(self, request):
        # 检查当前请求的路径是否在 白名单 中
        if request.path in self.white_list:
            return

        uid = request.session.get('uid')
        if not uid:
            return render_json(stat.LoginRequired.code)
        else:
            request.uid = uid


class LogicErrMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, stat.LogicErr):
            err_log.error(f'Code: {exception.code}  Data: {exception.data}')
            return render_json(exception.data, exception.code)
