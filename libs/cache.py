from redis import Redis

from swiper.conf import REDIS

rds = Redis(**REDIS)
