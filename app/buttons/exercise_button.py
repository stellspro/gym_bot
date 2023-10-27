from app.handlers import callbacks
from aiogram import types


def get_exercises_by_workout_plan_type(workout_plan, exercise_in_workout_plan, exercises_with_mark, reps):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for count, exercise in enumerate(exercise_in_workout_plan):
        if exercise.id in exercises_with_mark:
            button = types.InlineKeyboardButton(text=f'{exercise} - {reps[count].reps}',
                                                callback_data=callbacks.callback_exercise_by_muscle_groups.new(
                                                    exercise=f'{exercise}'))
            button_delete_mark = types.InlineKeyboardButton(text='  ☑️  ',
                                                            callback_data=callbacks.callback_del_exercise.new(
                                                                wp=workout_plan.id,
                                                                ex=exercise.id))
            keyboard.add(button, button_delete_mark)
        else:
            button = types.InlineKeyboardButton(text=f'{exercise} - {reps[count].reps}',
                                                callback_data=callbacks.callback_exercise_by_muscle_groups.new(
                                                    exercise=f'{exercise}'))
            button_add_mark = types.InlineKeyboardButton(text='  🔘  ',
                                                         callback_data=callbacks.callback_add_exercise.new(
                                                             wp=workout_plan.id,
                                                             ex=exercise.id))
            keyboard.add(button, button_add_mark)

    return keyboard
