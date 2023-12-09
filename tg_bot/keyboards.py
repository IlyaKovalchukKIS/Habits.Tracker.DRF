from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def habit_choice():
    command_key = InlineKeyboardBuilder()
    command_key.add(
        InlineKeyboardButton(text='1', callback_data='pleasant_habit'),
        InlineKeyboardButton(text='2', callback_data='add_award'),
        InlineKeyboardButton(text='3', callback_data='related_habit')
    )
    return command_key.adjust(3).as_markup()


def habit_frequency():
    command_key = InlineKeyboardBuilder()
    command_key.add(
        InlineKeyboardButton(text='1 раз в день', callback_data='frequency_1'),
        InlineKeyboardButton(text='1 раз в 2 дня', callback_data='frequency_2'),
        InlineKeyboardButton(text='1 раз в 3 дня', callback_data='frequency_3'),
        InlineKeyboardButton(text='1 раз в 4 дня', callback_data='frequency_4'),
        InlineKeyboardButton(text='1 раз в 5 дней', callback_data='frequency_5'),
        InlineKeyboardButton(text='1 раз в 6 дней', callback_data='frequency_6'),
        InlineKeyboardButton(text='1 раз в 7 дней', callback_data='frequency_7')
    )

    return command_key.adjust(1).as_markup()


def related_habit(id_habit):
    command_key = InlineKeyboardBuilder()
    command_key.add(
        InlineKeyboardButton(text='Связать', callback_data=f'habit_{id_habit}'),
    )
    return command_key.adjust(1).as_markup()


def bool_choice():
    command_key = InlineKeyboardBuilder()
    command_key.add(
        InlineKeyboardButton(text='Да', callback_data=f'is_published_True'),
        InlineKeyboardButton(text='Нет', callback_data=f'is_published_False'),
    )
    return command_key.adjust(2).as_markup()


def delete_and_update(id_habit):
    command_key = InlineKeyboardBuilder()
    command_key.add(
        InlineKeyboardButton(text='Изменить', callback_data=f'update_habit_{id_habit}'),
        InlineKeyboardButton(text='Удалить', callback_data=f'delete_habit_{id_habit}'),
    )
    return command_key.adjust(2).as_markup()


def update_fields(habit_data: dict):
    command_key = InlineKeyboardBuilder()
    for key, value in habit_data.items():
        command_key.add(
            InlineKeyboardButton(text=f"{key} - {value}", callback_data=f'update_field_{key}_{habit_data["id"]}'),
        )
    return command_key.adjust(1).as_markup()


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='test2@test.sky')],
        [KeyboardButton(text='123qwerty')]
    ],
    resize_keyboard=True
)

main_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Показать все свои привычки')],
        [KeyboardButton(text='Создать привычку')],
        [KeyboardButton(text='Показать привычки пользователей')]
    ]
)


def yes_no():
    command_key = InlineKeyboardBuilder()
    command_key.add(
        InlineKeyboardButton(text='да', callback_data='++'),
        InlineKeyboardButton(text='нет', callback_data='--')
    )
    return command_key.adjust(1).as_markup()

# yes_or_no = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='Да', callback_data='++'),
#             KeyboardButton(text='Нет', callback_data='--')
#         ]
#     ], resize_keyboard=True
# )
