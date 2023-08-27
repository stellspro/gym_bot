from redis_con import DataConn
from utils import port_redis, host_redis, psw_redis


def add_workout_plan_type_in_user_plans(user_id: int, workout_type_id: int):
    """Добавление категории тренировок в избранное"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.rpush(f'{user_id}-workout_plans', workout_type_id)
        redis_client.expire(user_id, 86400)


def delete_workout_plan_type_in_user_plans(user_id: int, workout_type_id: int):
    """Удаление категории тренировок в избранное"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.lrem(f'{user_id}-workout_plans', 1, workout_type_id)
        redis_client.expire(user_id, 86400)


def get_workout_plan_types_in_user_plans(user_id: int):
    """Выводит все категории тренировок из избранного пользователя"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        return [int(x) for x in redis_client.lrange(f'{user_id}-workout_plans', 0, -1)]


def add_mark_workout_plan(user_id: int, workout_plan_id: int):
    """Отметка 'выполнено' на тренировочный план"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.rpush(f'{user_id}-workout_plan', workout_plan_id)
        redis_client.expire(user_id, 86400)


def del_mark_workout_plan(user_id: int, workout_plan_id: int):
    """Удаление отметки 'выполнено' на тренировочный план"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.lrem(f'{user_id}-workout_plan', 1, workout_plan_id)
        redis_client.expire(user_id, 86400)


def get_workout_plans_with_mark(user_id: int):
    """Выводит все отмеченные тренировочные планы"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        return [int(x) for x in redis_client.lrange(f'{user_id}-workout_plan', 0, -1)]


def get_exercises_with_mark(user_id: int, workout_plan_id: int):
    """Выводит все отмеченные упражнения в тренировочном плане"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        return [int(x) for x in redis_client.lrange(f'{user_id}-workout_plan-{workout_plan_id}', 0, -1)]


def add_mark_exercise(user_id: int, workout_plan_id: int, exercise_id: int):
    """Отметка 'выполнено' на упражнение в тренировочном плане"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.rpush(f'{user_id}-workout_plan-{workout_plan_id}', exercise_id)
        redis_client.expire(user_id, 86400)


def del_mark_exercise(user_id: int, workout_plan_id: int, exercise_id: int):
    """Удаление отметки 'выполнено' на упражнение в тренировочном плане"""
    with DataConn(host_redis, port_redis, psw_redis) as redis_client:
        redis_client.lrem(f'{user_id}-workout_plan-{workout_plan_id}', 1, exercise_id)
        redis_client.expire(user_id, 86400)
