import pymysql
from libs.orm import patch_model

pymysql.install_as_MySQLdb()
patch_model()  # 为 orm 增加缓存处理
