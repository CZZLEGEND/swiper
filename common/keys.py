'''各种缓存的 Key'''

VCODE_K = 'Vcode-%s'  # 验证码的 Key, 拼接用户的手机号
FIRST_RCMD_K = 'FIRST_RCMD-%s'  # 优先推荐队列, 拼接用户的 ID
REWIND_K = 'Rewind-%s-%s'  # 记录每日反悔次数的 Key，拼接当天的日期和uid
