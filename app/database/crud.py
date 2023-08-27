from sqlalchemy.orm import Session
from app.models import models


def get_muscle_groups_by_id(db: Session, muscle_group_id: int):
    """Возвращает мышечную группу по id"""
    return db.query(models.MuscleGroup).filter(models.MuscleGroup.id == muscle_group_id).first()


def get_reps_by_workout_plan_id(db: Session, workout_plan_id):
    """Возвращает список с id упражнений и количеством повторений по id тренировочного плана"""
    return db.query(models.workout_plan_exercise).filter_by(workout_plan_id=workout_plan_id).all()


def get_muscle_groups(db: Session):
    """Возвращает список из всех мышечных групп"""
    return db.query(models.MuscleGroup).all()


def get_workout_by_id(db: Session, workout_id: int):
    """Возвращает тренировку по id"""
    return db.query(models.WorkoutPlan).filter(models.WorkoutPlan.id == workout_id).first()


def get_exercises_by_muscle_group_id(db: Session, muscle_group_id: int):
    """Возвращает список упражнений по id мышечной группы"""
    muscle_group = db.query(models.MuscleGroup).filter(models.MuscleGroup.id == muscle_group_id).first()
    return muscle_group.exercises


def get_exercises_by_muscle_group_name(db: Session, muscle_group_name: str):
    """Возвращает список упражнений по названию мышечной группы"""
    muscle_group = db.query(models.MuscleGroup).filter(models.MuscleGroup.name == muscle_group_name).first()
    return muscle_group.exercises


def get_exercise_by_name(db: Session, exercise_name: str):
    """Возвращает упражнение по названию"""
    return db.query(models.Exercise).filter(models.Exercise.name == exercise_name).first()


def get_exercises_by_workout_plan_id(db: Session, workout_plan_id: int):
    """Возвращает список упражнений по id тренировочного плана"""
    workout_plan = db.query(models.WorkoutPlan).filter(models.WorkoutPlan.id == workout_plan_id).first()
    return workout_plan.exercises


def get_all_workout_plans_types(db: Session):
    """Возвращает все категории тренировочных планов"""
    return db.query(models.WorkoutPlanType).all()


def get_workout_plan_type_by_id(db: Session, workout_plan_type_id: int):
    """Возвращает категорию тренировочного плана по id"""
    return db.query(models.WorkoutPlanType).filter(models.WorkoutPlanType.id == workout_plan_type_id).first()


def get_workout_plans_by_type(db: Session, workout_type_id: int):
    """Возвращает все тренировочные планы по id категории"""
    workout_type = db.query(models.WorkoutPlanType).filter(models.WorkoutPlanType.id == workout_type_id).first()
    return workout_type.workout_plans
