from .redis_con import DataConn
from utils import port_redis, host_redis, psw_redis


class BaseRedisRepository:
    directory = 'Base'

    def get_all(
            self,
            user_id: int,
            plan: int = None
    ):
        with DataConn(host_redis, port_redis, psw_redis) as redis_client:
            return [int(x) for x in redis_client.lrange(f'{user_id}{self.directory}{plan if plan else ""}', 0, -1)]

    def add(
            self,
            user_id: int,
            entity: int,
            plan: int = None
    ):
        with DataConn(host_redis, port_redis, psw_redis) as redis_client:
            redis_client.rpush(f'{user_id}{self.directory}{plan if plan else ""}', entity)
            redis_client.expire(user_id, 86400)

    def delete(
            self,
            user_id: int,
            entity: int,
            plan: int = None
    ):
        with DataConn(host_redis, port_redis, psw_redis) as redis_client:
            redis_client.lrem(f'{user_id}{self.directory}{plan if plan else ""}', 1, entity)
            redis_client.expire(user_id, 86400)
