from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.database.database import Base, engine

workout_plan_exercise = Table('workout_plan_exercise',
                              Base.metadata,
                              Column('workout_plan_id', Integer(), ForeignKey('workout_plans.id')),
                              Column('exercise_id', Integer(), ForeignKey('exercises.id')),
                              Column('reps', String())
                              )


class MuscleGroup(Base):
    __tablename__ = 'muscle_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    exercises = relationship("Exercise")

    def __repr__(self):
        return self.name


class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    exercises = relationship('Exercise', secondary=workout_plan_exercise)
    workout_plan_type = Column(Integer, ForeignKey('workout_plan_type.id'))

    def __repr__(self):
        return self.name


class WorkoutPlanType(Base):
    __tablename__ = 'workout_plan_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    workout_plans = relationship('WorkoutPlan')

    def __repr__(self):
        return self.name


class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    image_slug = Column(String(100), nullable=False)
    muscle_group_id = Column(Integer, ForeignKey('muscle_groups.id'))

    def __repr__(self):
        return self.name


Base.metadata.create_all(engine)
