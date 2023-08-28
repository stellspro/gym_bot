from aiogram.utils.callback_data import CallbackData


callback_all_workout_types = CallbackData("workout_type", "types")
callback_all_muscle_groups = CallbackData("muscle_group", "group")
callback_workout_plan_by_type = CallbackData("workout_plan", "plan")
callback_exercise_by_muscle_groups = CallbackData("ex_by_mg", "exercise")
callback_exercise_by_workout_plan = CallbackData("exercise_by_workout_plan", "exercise")
callback_add_workout_types = CallbackData("add_wt", "wt")
callback_del_workout_types = CallbackData("del_wt", "wt")
callback_add_workout_plan = CallbackData("add_wp", "wp")
callback_del_workout_plan = CallbackData("del_wp", "wp")
callback_add_exercise = CallbackData("add_ex", "wp", "ex")
callback_del_exercise = CallbackData("del_ex", "wp", "ex")
