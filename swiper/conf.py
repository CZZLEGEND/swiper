'''程序逻辑和第三方平台的配置'''

# Redis 配置
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 6,
}


# 云之讯短信平台配置
YZX_SMS_API = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_SMS_ARGS = {
    "sid": '4ad2912058ef9ef9ea0cdd790e0f7361',
    "token": 'cc2de93f90e7356abf9580a7de00074b',
    "appid": '3a34537ffb294f0a8af45555a161e68a',
    "templateid": '527103',
    "param": None,
    "mobile": None
}


# 七牛云配置
QN_ACCESSKEY = "kEM0sRR-meB92XU43_a6xZqhiyyTuu5yreGCbFtw"
QN_SECRETKEY = "QxTKqgnOb_UVldphU261qu9IdzmjkgGHh6GQVPPy"
QN_BUCKET = 'sh1906'
QN_BASE_URL = 'http://q3oh1b1oq.bkt.clouddn.com'
