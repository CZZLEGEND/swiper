from qiniu import Auth, put_file

from swiper import conf


def upload_to_qn(filepath, filename):
    '''将本地文件上传到七牛云'''
    # 构建鉴权对象
    qn_auth = Auth(conf.QN_ACCESSKEY, conf.QN_SECRETKEY)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(conf.QN_BUCKET, filename, 3600)

    # 要上传文件的本地路径
    put_file(token, filename, filepath)

    # 生成文件的 URL
    file_url = '%s/%s' % (conf.QN_BASE_URL, filename)
    return file_url
