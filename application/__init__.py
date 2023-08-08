import pymysql
from django_redis import get_redis_connection

redis_connect = get_redis_connection()
pymysql.version_info=(1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()
