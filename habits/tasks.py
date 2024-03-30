import asyncio
import datetime

from aiogram import Router
from celery import shared_task

from habits.models import Habit

router = Router()


@shared_task
def habit_time():
    habits_send = []
    habits = Habit.objects.all()
    date_time = datetime.datetime.now()
    print(date_time)

    for habit in habits:
        last_send = date_time.date() - habit.last_send

        if habit.last_send is None or last_send.day == 0:
            if habit.time == date_time.time():
                habits_send.append(habit)

    async def send_message():
        await router.message(chat_id=habit.user.tg_chat_id, text='Начните выполнять привычку')

    asyncio.run(send_message())
