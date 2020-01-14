import pickle

from redis import Redis as _Redis

from swiper.conf import REDIS


class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        '''
        Set the value at key ``name`` to pickled ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.
        '''
        pickled_value = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        return super().set(name, pickled_value, ex, px, nx, xx)

    def get(self, name, default=None):
        '''Return the value at key ``name``, or ``default`` if the key doesn't exist'''
        pickled_value = super().get(name)
        if pickled_value is None:
            return default
        else:
            try:
                value = pickle.loads(pickled_value)
            except pickle.UnpicklingError:
                return pickled_value
            else:
                return value


rds = Redis(**REDIS)
