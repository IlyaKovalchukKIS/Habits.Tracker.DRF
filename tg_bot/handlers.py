import requests
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

import tg_bot.keyboards as kb
from tg_bot.services import habit_create_api, get_pleasant_habit_list, habit_delete_api, habit_retrieve_api, \
    habit_update_api, habit_published_api

router = Router()
url = 'http://127.0.0.1:8000/'
user_data = {}
habit_data = []


class HabitFields(StatesGroup):
    user = State()
    place = State()
    time = State()
    action = State()
    pleasant_habit = State()
    related_habit = State()
    frequency = State()
    award = State()
    time_to_complete = State()
    is_published = State()
    user_data = State()

    field_update = State()


@router.message(CommandStart())
async def registration_user(message: Message, state: FSMContext):
    data_user = {}
    data_from_tg = message.chat

    data_user['email'] = f"{data_from_tg.username}@habit.kis"
    data_user['chat_id_tg'] = message.chat.id
    data_user['password'] = 34531241

    check_user = requests.post(url=url + "users/token/", data=data_user)

    if str(check_user.status_code).startswith('4'):
        print('if')
        # password = [str(random.randint(0, 9)) for _ in range(10)]
        # data_user['password'] = password
        registration = requests.post(url=url + 'users/user/', data=data_user)
        token_user = requests.post(url=url + "users/token/", data=data_user)
        data_user['token'] = token_user.json().get('access')

        user_data['token'] = data_user['token']
        user_data['email'] = data_user['email']
        user_data['password'] = data_user['password']

        await state.update_data(user_data=data_user)
        await message.answer(text='Вы зарегистрированы')

    else:
        print('else')
        user_list = requests.get(url=url + 'users/user/')
        print(user_list.json())
        user_list = user_list.json()
        for user in user_list:
            if data_user['email'] == user['email'] or message.chat.id == user['chat_id_tg']:
                token_user = requests.post(url=url + "users/token/", data=data_user)
                data_user['token'] = token_user.json().get('access')

                user_data['token'] = data_user['token']
                user_data['email'] = data_user['email']
                user_data['password'] = data_user['password']

                await state.update_data(user_data=data_user)
                await message.answer('Токен пользователя обновлен')


@router.message(Command('habit_create'))
async def create_habit(message: Message, state: FSMContext):
    await state.set_state(HabitFields.place)
    await message.answer('Введите МЕСТО где вы будете выполнять привычку:', reply_markup=ReplyKeyboardRemove())


@router.message(HabitFields.place)
async def time_habit(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(HabitFields.time)
    await message.answer('Введите ВРЕМЯ в которое вы будете выполять привычку в формате 12:00:',
                         reply_markup=ReplyKeyboardRemove())


@router.message(HabitFields.time)
async def habit_action(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(HabitFields.action)
    await message.answer('Введите ДЕЙСТВИЕ которое будете выполнять:', reply_markup=ReplyKeyboardRemove())


@router.message(HabitFields.action)
async def frequency(message: Message, state: FSMContext):
    await state.update_data(action=message.text)
    await state.set_state(HabitFields.frequency)
    await message.answer('Выберете ПЕРИОДИЧНОСТЬ с которой будете выполнять привычку',
                         reply_markup=kb.habit_frequency())


@router.callback_query(HabitFields.frequency)
async def add_frequency(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    await callback.message.answer(text=str(data))
    await state.update_data(frequency=data[-1])
    await state.set_state(HabitFields.time_to_complete)
    await callback.message.answer('Введите ВРЕМЯ НА ВЫПОЛНЕНИЕ привычки, но не более 120 секунд:',
                                  reply_markup=ReplyKeyboardRemove())


@router.message(HabitFields.time_to_complete)
async def published_habit(message: Message, state: FSMContext):
    await state.update_data(time_to_complete=message.text)
    await state.set_state(HabitFields.is_published)
    await message.answer('Сделать привычку публичной?', reply_markup=kb.bool_choice())


@router.callback_query(F.data.startswith('is_published'))
async def save_is_published(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_published=callback.data.split('_')[-1])
    await choice_habit(callback.message, state)


async def choice_habit(message: Message, state: FSMContext):
    await message.answer('Выберете одно из действий:\n'
                         '1 - сделать привычку приятной\n'
                         '2 - добавить вознаграждение за выполенную привычку\n'
                         '3 - выбрать связанную привычку')
    await message.answer('Сделайте выбор:', reply_markup=kb.habit_choice())


# end
@router.callback_query(F.data.casefold() == 'pleasant_habit')
async def pleasant_habit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pleasant_habit=True)
    habit_data = await state.get_data()
    create = habit_create_api(habit_data=habit_data, user_token=habit_data['user_data']['token'])
    print(create)
    await callback.message.answer(f'Ваша привычка:\n'
                                  f'Я буду {str(habit_data["action"]).lower()} '
                                  f'в {str(habit_data["place"]).lower()} '
                                  f'в {habit_data["time"]}')
    await state.clear()


@router.callback_query(F.data.casefold() == 'add_award')
async def add_award(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pleasant_habit=False)
    await state.set_state(HabitFields.award)
    await callback.message.answer('Введите вознаграждение:')


# end
@router.message(HabitFields.award)
async def save_award(message: Message, state: FSMContext):
    await state.update_data(award=message.text)
    habit_data = await state.get_data()
    create = habit_create_api(habit_data=habit_data, user_token=habit_data['user_data']['token'])
    print(create)
    await message.answer(f'Ваша привычка:\n'
                         f'Я буду {str(habit_data["action"]).lower()} '
                         f'в {str(habit_data["place"]).lower()} '
                         f'в {habit_data["time"]}')
    await state.clear()


# end
@router.callback_query(F.data.casefold() == 'related_habit')
async def related_habit(callback: CallbackQuery, state: FSMContext):
    res = []
    await state.update_data(pleasant_habit=False)
    await state.update_data(award=None)
    await state.set_state(HabitFields.related_habit)
    habits = get_pleasant_habit_list(user_data)
    for habit in habits:
        if habit['pleasant_habit']:
            res.append(habit)
    await callback.message.answer('Выберете привычку:')
    for habit in res:
        await callback.message.answer(f'Ваша привычка:\n'
                                      f'Я буду {str(habit["action"]).lower()} '
                                      f'в {str(habit["place"]).lower()} '
                                      f'в {habit["time"]}',
                                      reply_markup=kb.related_habit(habit['id']))


# end
@router.callback_query(F.data.startswith("habit"))
async def save_related_habit(callback: CallbackQuery, state: FSMContext):
    habit_id = callback.data.split('_')[-1]
    await state.update_data(related_habit=habit_id)
    habit_data = await state.get_data()
    create = habit_create_api(habit_data=habit_data, user_token=habit_data['user_data']['token'])
    print(create)
    await callback.message.answer(f'Ваша привычка:\n'
                                  f'Я буду {str(habit_data["action"]).lower()} '
                                  f'в {str(habit_data["place"]).lower()} '
                                  f'в {habit_data["time"]}')
    await state.clear()


@router.message(HabitFields.award)
async def award(message: Message, state: FSMContext):
    await state.update_data(award=message.text)


@router.message(Command('habits_list'))
async def list_habit(message: Message, state: FSMContext):
    habits = get_pleasant_habit_list(user_data)
    for habit in habits:
        await message.answer(f'Ваша привычка:\n'
                             f'Я буду {str(habit["action"]).lower()} '
                             f'в {str(habit["place"]).lower()} '
                             f'в {habit["time"]}', reply_markup=kb.delete_and_update(habit['id']))


@router.callback_query(F.data.startswith("delete_habit_"))
async def delete_habit(callback: CallbackQuery, state: FSMContext):
    print('-' * 10)
    print('handler delete habit')
    habit_id = callback.data.split("_")[-1]
    print(habit_id)
    user_token = user_data['token']
    print(user_token)
    response = habit_delete_api(habit_id=habit_id, user_token=user_token)
    await callback.message.answer(response)


@router.callback_query(F.data.startswith("update_habit_"))
async def update_habit(callback: CallbackQuery, state: FSMContext):
    habit_id = callback.data.split("_")[-1]
    user_token = user_data['token']
    retrieve = habit_retrieve_api(habit_id=habit_id, user_token=user_token)
    await callback.message.answer(text='Выберете поле которое хотите изменить', reply_markup=kb.update_fields(retrieve))


@router.callback_query(F.data.startswith('update_field_'))
async def update_field(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split('_')
    habit_data.extend(field)
    await state.set_state(HabitFields.field_update)
    if field[-2] in ['time', 'place', 'action', 'award', 'time_to_complete']:
        await callback.message.answer('Введите изменение:')

        @router.message(HabitFields.field_update)
        async def habit_update_func(message: Message, state: FSMContext):
            data = message.text
            await state.update_data(field_update=data)
            data = await state.get_data()
            update = habit_update_api(habit_id=habit_data[-1],
                                      field=habit_data[-2],
                                      data=data['field_update'],
                                      user_token=user_data['token'])
            await callback.message.answer('str(update)')
            await state.clear()

    elif field[-2] == 'frequency':
        await callback.message.answer('Выберете периодичность', reply_markup=kb.habit_frequency())

        @router.callback_query(HabitFields.field_update)
        async def habit_update_func(callback: CallbackQuery, state: FSMContext):
            data = callback.data.split('_')
            await state.update_data(field_update=data[-1])
            data = await state.get_data()
            update = habit_update_api(habit_id=habit_data[-1],
                                      field=habit_data[-2],
                                      data=data['field_update'],
                                      user_token=user_data['token'])
            await callback.message.answer('str(update)')
            await state.clear()

    elif field[-2] == 'published':
        await callback.message.answer('Выберете изменение:', reply_markup=kb.bool_choice())

        @router.callback_query(HabitFields.field_update)
        async def habit_update_func(callback: CallbackQuery, state: FSMContext):
            data = callback.data.split('_')
            await state.update_data(field_update=data[-1])
            data = await state.get_data()
            update = habit_update_api(habit_id=habit_data[-1],
                                      field=habit_data[-2],
                                      data=data['field_update'],
                                      user_token=user_data['token'])
            await callback.message.answer('str(update)')
            await state.clear()


@router.message(Command('habits_published'))
async def list_habit(message: Message, state: FSMContext):
    habits = habit_published_api(user_data['token'])
    for habit in habits:
        if habit['is_published']:
            await message.answer(f'Список публичных привычек:\n'
                                 f'Я буду {str(habit["action"]).lower()} '
                                 f'в {str(habit["place"]).lower()} '
                                 f'в {habit["time"]}')
