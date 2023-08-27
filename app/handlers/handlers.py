from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from ..database.database import db
from app.database import crud
from ..redis import workout_user
from app.handlers import callbacks
from app.bot import bot

dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    """Обработка команды start"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = ['План тренировки', 'Упражнения', 'Мои тренировки']
    keyboard.add(*buttons)
    await message.answer("Hello!", reply_markup=keyboard)


@dp.message_handler(Text(equals='Мои тренировки'))
async def workout_plan_menu(message: types.Message):
    """Обработка кнопки 'Мои тренировки'
    Выводит список категорий тренировочных планов пользователя"""
    plans = workout_user.get_workout_plan_types_in_user_plans(message.from_user.id)

    print(plans)
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    if plans:
        for plan_id in plans:
            plan = crud.get_workout_plan_type_by_id(db, plan_id)
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


@dp.message_handler(Text(equals='План тренировки'))
async def workout_plan_menu(message: types.Message):
    """Обработка кнопки 'План тренировки'
    Выводит список категорий тренировочных планов"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    workout_types = crud.get_all_workout_plans_types(db)
    print(workout_types)
    w_plans = workout_user.get_workout_plan_types_in_user_plans(message.from_user.id)

    for workout_type in workout_types:
        button = types.InlineKeyboardButton(text=f'{workout_type}',
                                            callback_data=callbacks.callback_all_workout_types.new(
                                                types=f'{workout_type.id}'))
        if workout_type.id in w_plans:
            button_delete = types.InlineKeyboardButton(text='✖️    Удалить',
                                                       callback_data=callbacks.callback_del_workout_types.new(
                                                           wt=workout_type.id))
            keyboard.add(button, button_delete)
        else:
            button_add = types.InlineKeyboardButton(text='➕   Добавить',
                                                    callback_data=callbacks.callback_add_workout_types.new(
                                                        wt=workout_type.id))
            keyboard.add(button, button_add)
    await message.answer('Выберите тип тренировки', reply_markup=keyboard)


@dp.callback_query_handler(callbacks.callback_all_workout_types.filter())
async def workout_plan_types(call: types.CallbackQuery, callback_data: dict):
    """Выводит тренировочные планы в категории"""
    workout_plan_id = callback_data['types']
    w_plans = crud.get_workout_plans_by_type(db, workout_plan_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    check_mark = workout_user.get_workout_plans_with_mark(call.from_user.id)
    print(check_mark)

    for workout_plan in w_plans:
        if workout_plan.id in check_mark:
            button = types.InlineKeyboardButton(text=f'{workout_plan}',
                                                callback_data=callbacks.callback_workout_plan_by_type.new(
                                                    plan=f'{workout_plan.id}'))
            button_delete_mark = types.InlineKeyboardButton(text='  ☑️  ',
                                                            callback_data=callbacks.callback_add_workout_plan.new(
                                                                wp=workout_plan.id))
            keyboard.add(button, button_delete_mark)
        else:
            button = types.InlineKeyboardButton(text=f'{workout_plan}',
                                                callback_data=callbacks.callback_workout_plan_by_type.new(
                                                    plan=f'{workout_plan.id}'))
            button_add_mark = types.InlineKeyboardButton(text='  🔘 ',
                                                         callback_data=callbacks.callback_add_workout_plan.new(
                                                             wp=workout_plan.id))
            keyboard.add(button, button_add_mark)

    await call.message.answer('Выберите план тренировки', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(callbacks.callback_add_workout_plan.filter())
async def add_mark_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Добавление отметки 'выполнено' на тренировочный план"""
    workout_plan_id = callback_data['wp']
    if workout_plan_id not in workout_user.get_workout_plans_with_mark(call.from_user.id):
        workout_user.add_mark_workout_plan(call.from_user.id, workout_plan_id)
        await call.answer('Отмечено')
    else:
        await call.answer('План уже отмечен')


@dp.callback_query_handler(callbacks.callback_del_workout_plan.filter())
async def del_mark_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Удаление отметки 'выполнено' на тренировочный план"""
    workout_plan_id = callback_data['wp']
    workout_user.del_mark_workout_plan(call.from_user.id, workout_plan_id)
    await call.answer('Удалено')


@dp.callback_query_handler(callbacks.callback_add_workout_types.filter())
async def add_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Добавление тренировочного плана в закладки"""
    workout_plan_id = callback_data['wt']
    if workout_plan_id not in workout_user.get_workout_plan_types_in_user_plans(call.from_user.id):
        workout_user.add_workout_plan_type_in_user_plans(call.from_user.id, workout_plan_id)
        await call.answer('Добавлено')
    else:
        await call.answer('План уже добавлен в избранное')


@dp.callback_query_handler(callbacks.callback_del_workout_types.filter())
async def delete_workout_plan(call: types.CallbackQuery, callback_data: dict):
    """Удаление тренировочного плана из закладок"""
    workout_plan_id = callback_data['wt']
    workout_user.delete_workout_plan_type_in_user_plans(call.from_user.id, workout_plan_id)
    await call.answer('Удалено')


@dp.callback_query_handler(callbacks.callback_workout_plan_by_type.filter())
async def workout_plans(call: types.CallbackQuery, callback_data: dict):
    """Выводит список упражнений в плане тренировки"""
    workout_plan_id = callback_data['plan']
    workout_plan = crud.get_workout_by_id(db, workout_plan_id)
    exercise_in_workout_plan = crud.get_exercises_by_workout_plan_id(db, workout_plan_id)
    print(exercise_in_workout_plan)
    reps = crud.get_reps_by_workout_plan_id(db, workout_plan_id)
    print(reps)
    exercises_with_mark = workout_user.get_exercises_with_mark(call.from_user.id, workout_plan_id)
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
    await call.message.answer(f'{workout_plan}', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(callbacks.callback_add_exercise.filter())
async def add_mark_exercise(call: types.CallbackQuery, callback_data: dict):
    """Добавление отметки 'выполнено' на тренировочный план"""
    workout_plan_id = callback_data['wp']
    exercise_id = callback_data['ex']
    if exercise_id not in workout_user.get_exercises_with_mark(call.from_user.id, workout_plan_id):
        workout_user.add_mark_exercise(call.from_user.id, workout_plan_id, exercise_id)
        await call.answer('Отмечено')
    else:
        await call.answer('Упражнение уже отмечено')


@dp.callback_query_handler(callbacks.callback_del_exercise.filter())
async def del_mark_exercise(call: types.CallbackQuery, callback_data: dict):
    """Удаление отметки 'выполнено' на тренировочный план"""
    workout_plan_id = callback_data['wp']
    exercise_id = callback_data['ex']
    workout_user.del_mark_exercise(call.from_user.id, workout_plan_id, exercise_id)
    await call.answer('Удалено')


@dp.message_handler(Text(equals='Упражнения'))
async def exercises_menu(message: types.Message):
    """Выводит типы мышечных групп"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    groups = crud.get_muscle_groups(db)
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
    if muscle_group:
        exercises = crud.get_exercises_by_muscle_group_name(db, muscle_group)
        for exercise in exercises:
            button = types.InlineKeyboardButton(text=f'{exercise} ',
                                                callback_data=callbacks.callback_exercise_by_muscle_groups.new(
                                                    exercise=f'{exercise}'))
            keyboard.add(button)

    await call.message.answer(f'{muscle_group}', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(callbacks.callback_exercise_by_muscle_groups.filter())
async def exercise_menu(call: types.CallbackQuery, callback_data: dict):
    # keyboard = types.InlineKeyboardMarkup(row_width=1)
    """Выводит описание упражнения"""
    exercise = callback_data['exercise']
    if exercise:
        exercise = crud.get_exercise_by_name(db, exercise)
        await call.message.answer(f'{exercise}')
        with open(f'images/{exercise.image_slug}', 'rb') as an:
            await call.message.answer_animation(an)
        await call.message.answer(f'{exercise.description}')
        await call.answer()



