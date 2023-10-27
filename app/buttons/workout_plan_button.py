from typing import List
from app.handlers import callbacks
from aiogram import types


def get_all_workout_types(workout_types, user_plans):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for workout_type in workout_types:
        button = types.InlineKeyboardButton(text=f'{workout_type}',
                                            callback_data=callbacks.callback_all_workout_types.new(
                                                types=f'{workout_type.id}'))
        if workout_type.id in user_plans:
            button_delete = types.InlineKeyboardButton(text='✖️    Удалить',
                                                       callback_data=callbacks.callback_del_workout_types.new(
                                                           wt=workout_type.id))
            keyboard.add(button, button_delete)
        else:
            button_add = types.InlineKeyboardButton(text='➕   Добавить',
                                                    callback_data=callbacks.callback_add_workout_types.new(
                                                        wt=workout_type.id))
            keyboard.add(button, button_add)
    return keyboard


def get_workout_plan_type_button(plans: List, check_mark: List):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for workout_plan in plans:
        if workout_plan.id in check_mark:
            button = types.InlineKeyboardButton(text=f'{workout_plan}',
                                                callback_data=callbacks.callback_workout_plan_by_type.new(
                                                    plan=f'{workout_plan.id}'))
            button_delete_mark = types.InlineKeyboardButton(text='  ☑️  ',
                                                            callback_data=callbacks.callback_del_workout_plan.new(
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
    return keyboard
