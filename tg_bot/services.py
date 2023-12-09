import requests


def habit_create_api(habit_data, user_token):
    habit_data.pop('user_data')
    url = 'http://127.0.0.1:8000/habits/create/'
    headers = {'Authorization': f'Bearer {user_token}'}
    create = requests.post(url, data=habit_data, headers=headers)
    print(create)
    return create.json()


def habit_delete_api(habit_id, user_token):
    print('-' * 10)
    print('habit_delete_api')
    print(habit_id, user_token)
    url = 'http://127.0.0.1:8000/habits/destroy/'
    headers = {'Authorization': f'Bearer {user_token}'}
    destroy = requests.delete(url=url + f"{int(habit_id)}", headers=headers)
    print(destroy)
    return 'Привычка удалена'


def habit_update_api(habit_id, field, data, user_token):
    url = 'http://127.0.0.1:8000/habits/update/'
    headers = {'Authorization': f'Bearer {user_token}'}
    data = {field: data}
    print(data, habit_id, field)
    update = requests.put(url=url + f'{habit_id}/', headers=headers, data=data)
    print(update)
    return update


def habit_retrieve_api(habit_id, user_token):
    url = 'http://127.0.0.1:8000/habits/retrieve/'
    headers = {'Authorization': f'Bearer {user_token}'}
    retrieve = requests.get(url=url + f"{int(habit_id)}", headers=headers)
    return retrieve.json()


def habit_published_api(user_token):
    url = 'http://127.0.0.1:8000/habits/list/published/'
    headers = {'Authorization': f'Bearer {user_token}'}
    published = requests.get(url=url, headers=headers)
    return published.json()

def get_pleasant_habit_list(user_data):
    url = 'http://127.0.0.1:8000/habits/list/'
    headers = {'Authorization': f'Bearer {user_data["token"]}'}
    habits_list = requests.get(url=url, headers=headers)
    habits_list = habits_list.json()
    for habit in habits_list:
        if not habit['user'] == user_data['email']:
            habits_list.pop(habit)
    return habits_list
