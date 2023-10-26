from app.redis.base import BaseRedisRepository


class UserPlans(BaseRedisRepository):
    directory = '-workout_plans'


class MarkPlans(BaseRedisRepository):
    directory = '-workout_plan_mark'


class MarkExercise(BaseRedisRepository):
    directory = '-exercise_mark-'
