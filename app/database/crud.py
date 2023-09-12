from app.models import models
from app.database.base import BaseRepository
from app.database.database import db


class MuscleGroup(BaseRepository):
    model = models.MuscleGroup


class WorkoutPlan(BaseRepository):
    model = models.WorkoutPlan


class Exercise(BaseRepository):
    model = models.Exercise

    @staticmethod
    def get_by_muscle_group_id(id):
        entity = MuscleGroup(db).get(id)
        return entity.exercises

    @staticmethod
    def get_by_muscle_group_name(name):
        entity = MuscleGroup(db).get_by_name(name)
        return entity.exercises


class WorkoutPlanType(BaseRepository):
    model = models.WorkoutPlanType


class Reps(BaseRepository):
    model = models.workout_plan_exercise

    def get(self, id: int):
        entities = self.session.query(models.workout_plan_exercise).filter_by(workout_plan_id=id).all()
        return entities

    def all(self):
        return None
