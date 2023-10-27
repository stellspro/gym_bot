from app.buttons import workout_plan_button, exercise_button
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from app.database.database import db
from app.database import crud
from app.handlers import callbacks
from app.bot import bot
from app.redis.workout_user import UserPlans, MarkPlans, MarkExercise

dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    """Обработка команды start"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = ['Тип тренировки', 'Упражнения', 'Мои тренировки']
    keyboard.add(*buttons)
    await message.answer("Hello!", reply_markup=keyboard)


@dp.message_handler(Text(equals='Мои тренировки'))
async def workout_plan_menu(message: types.Message):
    """Обработка кнопки 'Мои тренировки'
    Выводит список категорий тренировочных планов пользователя"""
    user_plans = UserPlans()
    workout_plan_type = crud.WorkoutPlanType(db)
    plans = user_plans.get_all(message.from_user.id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    if plans:
        for plan_id in plans:
            plan = workout_plan_type.get(plan_id)
            button = types.InlineKeyboardButton(text=f'{plan.name}',
                                                callback_data=callbacks.callback_all_workout_types.new(
                                                    types=f'{plan.id}'))
            button_delete = types.InlineKeyboardButton(text='✖️    Удалить',
                                                       callback_data=callbacks.callback_del_workout_types.new(
                                                           wt=plan.id))

            keyboard.add(button, button_delete)
        await message.answer('Выберите тип тренировки', reply_markup=keyboard)
    else:
        await message.answer('У вас пока нет тренировок(')


@dp.message_handler(Text(equals='Тип тренировки'))
async def workout_plan_menu(message: types.Message):
    """Обработка кнопки 'Тип тренировки'
    Выводит список категорий тренировочных планов"""
    workout_plan_type = crud.WorkoutPlanType(db)
    workout_types = workout_plan_type.all()

    user_plans = UserPlans()
    user_plans = user_plans.get_all(message.from_user.id)
    keyboard = workout_plan_button.get_all_workout_types(workout_types, user_plans)

    await message.answer('Выберите тип тренировки', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_all_workout_types.filter())
async def workout_plan_types(call: types.CallbackQuery, callback_data: dict):
    """Выводит тренировочные планы в категории"""
    workout_plan_id = callback_data['types']
    plans = crud.WorkoutPlanType(db)
    w_plans = plans.get(workout_plan_id)

    mark_plans = MarkPlans()
    check_mark = mark_plans.get_all(call.from_user.id)
    keyboard = workout_plan_button.get_workout_plan_type_button(w_plans.workout_plans, check_mark)

    await call.message.answer('Выберите тренировочный план', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(callbacks.callback_add_workout_plan.filter())
async def add_mark_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Добавление отметки 'выполнено' на тренировочный план"""
    workout_plan_id = callback_data['wp']
    mark_plans = MarkPlans()

    if workout_plan_id not in mark_plans.get_all(call.from_user.id):
        mark_plans.add(call.from_user.id, workout_plan_id)
        await call.answer('Отмечено')
    else:
        await call.answer('План уже отмечен')

    plans = crud.WorkoutPlanType(db)
    w_plans = plans.get(workout_plan_id)
    check_mark = mark_plans.get_all(call.from_user.id)
    keyboard = workout_plan_button.get_workout_plan_type_button(w_plans.workout_plans, check_mark)

    await call.message.edit_text('Выберите тренировочный план', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_del_workout_plan.filter())
async def del_mark_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Удаление отметки 'выполнено' на тренировочный план"""
    workout_plan_id = callback_data['wp']
    mark_plans = MarkPlans()
    mark_plans.delete(call.from_user.id, workout_plan_id)
    await call.answer('Удалено')

    plans = crud.WorkoutPlanType(db)
    w_plans = plans.get(workout_plan_id)
    check_mark = mark_plans.get_all(call.from_user.id)
    keyboard = workout_plan_button.get_workout_plan_type_button(w_plans.workout_plans, check_mark)

    await call.message.edit_text('Выберите тренировочный план', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_add_workout_types.filter())
async def add_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Добавление тренировочного плана в закладки"""
    workout_plan_id = callback_data['wt']
    user_plans = UserPlans()

    if workout_plan_id not in user_plans.get_all(call.from_user.id):
        user_plans.add(call.from_user.id, workout_plan_id)
        await call.answer('Добавлено')
    else:
        await call.answer('План уже добавлен в избранное')

    workout_plan_type = crud.WorkoutPlanType(db)
    workout_types = workout_plan_type.all()

    user_plans = user_plans.get_all(call.from_user.id)
    keyboard = workout_plan_button.get_all_workout_types(workout_types, user_plans)
    await call.message.edit_text('Выберите тип тренировки', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_del_workout_types.filter())
async def delete_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Удаление тренировочного плана из закладок"""
    workout_plan_id = callback_data['wt']
    user_plans = UserPlans()
    user_plans.delete(call.from_user.id, workout_plan_id)
    await call.answer('Удалено')

    workout_plan_type = crud.WorkoutPlanType(db)
    workout_types = workout_plan_type.all()

    user_plans = user_plans.get_all(call.from_user.id)
    keyboard = workout_plan_button.get_all_workout_types(workout_types, user_plans)
    await call.message.edit_text('Выберите тип тренировки', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_workout_plan_by_type.filter())
async def workout_plans(call: types.CallbackQuery, callback_data: dict):
    """Выводит список упражнений в плане тренировки"""
    workout_plan_id = callback_data['plan']
    plan = crud.WorkoutPlan(db)
    workout_plan = plan.get(workout_plan_id)

    exercise_in_workout_plan = workout_plan.exercises
    reps = crud.Reps(db)
    reps = reps.get(workout_plan_id)
    mark_exercise = MarkExercise()
    exercises_with_mark = mark_exercise.get_all(call.from_user.id, workout_plan_id)

    keyboard = exercise_button.get_exercises_by_workout_plan_type(
                workout_plan,
                exercise_in_workout_plan,
                exercises_with_mark,
                reps
    )

    await call.message.answer(f'{workout_plan}', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(callbacks.callback_add_exercise.filter())
async def add_mark_exercise(call: types.CallbackQuery, callback_data: dict):
    """Добавление отметки 'выполнено' на упражнение в тренировочном плане"""
    workout_plan_id = callback_data['wp']
    exercise_id = callback_data['ex']
    mark_exercise = MarkExercise()
    if exercise_id not in mark_exercise.get_all(call.from_user.id, workout_plan_id):
        mark_exercise.add(
            user_id=call.from_user.id,
            entity=exercise_id,
            plan=workout_plan_id
        )
        await call.answer('Отмечено')
    else:
        await call.answer('Упражнение уже отмечено')

    plan = crud.WorkoutPlan(db)
    workout_plan = plan.get(workout_plan_id)

    exercise_in_workout_plan = workout_plan.exercises
    reps = crud.Reps(db)
    w_reps = reps.get(workout_plan_id)
    mark_exercise = MarkExercise()
    exercises_with_mark = mark_exercise.get_all(call.from_user.id, workout_plan_id)

    keyboard = exercise_button.get_exercises_by_workout_plan_type(
        workout_plan,
        exercise_in_workout_plan,
        exercises_with_mark,
        w_reps
    )
    await call.message.edit_text(f'{workout_plan}', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_del_exercise.filter())
async def del_mark_exercise(call: types.CallbackQuery, callback_data: dict):
    """Удаление отметки 'выполнено' на тренировочный план"""
    workout_plan_id = callback_data['wp']
    exercise_id = callback_data['ex']
    mark_exercise = MarkExercise()
    mark_exercise.delete(call.from_user.id, exercise_id, workout_plan_id)
    await call.answer('Удалено')

    plan = crud.WorkoutPlan(db)
    workout_plan = plan.get(workout_plan_id)

    exercise_in_workout_plan = workout_plan.exercises
    reps = crud.Reps(db)
    w_reps = reps.get(workout_plan_id)
    mark_exercise = MarkExercise()
    exercises_with_mark = mark_exercise.get_all(call.from_user.id, workout_plan_id)

    keyboard = exercise_button.get_exercises_by_workout_plan_type(
        workout_plan,
        exercise_in_workout_plan,
        exercises_with_mark,
        w_reps
    )
    await call.message.edit_text(f'{workout_plan}', reply_markup=keyboard)


@dp.message_handler(Text(equals='Упражнения'))
async def exercises_menu(message: types.Message):
    """Выводит типы мышечных групп"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    muscle_group = crud.MuscleGroup(db)
    groups = muscle_group.all()
    for muscle in groups:
        button = types.InlineKeyboardButton(text=f'{muscle}',
                                            callback_data=callbacks.callback_all_muscle_groups.new(group=f'{muscle}'))
        keyboard.add(button)

    await message.answer(f'Выберите мышечную группу:', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_all_muscle_groups.filter())
async def muscle_group_menu(call: types.CallbackQuery, callback_data: dict):
    """Выводит упражнения на каждую мышечную группу"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    muscle_group = callback_data['group']
    muscle_group_exercises = crud.MuscleGroup(db)
    exercise = muscle_group_exercises.get_by_name(muscle_group)
    if muscle_group:
        exercises = exercise.exercises
        for exercise in exercises:
            button = types.InlineKeyboardButton(text=f'{exercise} ',
                                                callback_data=callbacks.callback_exercise_by_muscle_groups.new(
                                                    exercise=f'{exercise}'))
            keyboard.add(button)

    await call.message.answer(f'{muscle_group}', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(callbacks.callback_exercise_by_muscle_groups.filter())
async def exercise_menu(call: types.CallbackQuery, callback_data: dict):
    """Выводит описание упражнения"""
    call_exercise = callback_data['exercise']
    exercise = crud.Exercise(db)

    if call_exercise:
        exercise = exercise.get_by_name(call_exercise)
        await call.message.answer(f'{exercise}')
        with open(f'app/images/{exercise.image_slug}', 'rb') as an:
            await call.message.answer_animation(an)
        await call.message.answer(f'{exercise.description}')
        await call.answer()

