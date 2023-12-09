# from users.models import User
#
#
# def registration_user(form):
#     user = User.objects.get(email=form.email) \
#         if User.objects.get(email=form.email) \
#         else User.objects.create(chat_id_tg=form.chat_id, email=form.email)
#     user.save()
#     return user
#

from users.models import User
from habits.models import Habit


def get_user(user) -> User.objects:
    user = User.objects.get(user) \
        if User.objects.get(user) \
        else User.objects.create_user(email=user, chat_id_tg=user.chat_id)

    return user


def get_list_habits(user_id: int) -> list[dict] or None:
    try:
        habits = Habit.objects.filter(user=user_id)
    except KeyError:
        return None
    else:
        return habits


def get_habit(user_id: int, habit_id: int) -> dict or None:
    try:
        habit = Habit.objects.get(user_id=user_id, habit_id=habit_id)
    except KeyError:
        return None
    else:
        return habit


if __name__ == '__main__':
    print(get_habit(1, 6))
    print()
    print(get_user(1))
    print()
    print(get_list_habits(1))