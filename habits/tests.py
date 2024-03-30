from rest_framework import status
from rest_framework.test import APITestCase
from users.tests import UserRegistrationMixin


class HabitsTestCase(UserRegistrationMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.headers = {"Authorization": f"Bearer {self.user_token.json()['access']}"}
        self.data = {
            "place": 'test place',
            'time': '11:22',
            'action': 'test action',
            'frequency': '1',
            'award': 'test award'
        }
        self.habit = self.client.post(
            '/habits/create/',
            data=self.data,
            headers=self.headers
        )

    def test_create_habit(self):
        """ Тестирование создания привычки """

        self.assertEqual(
            self.habit.status_code, status.HTTP_201_CREATED
        )

    def test_update_habit(self):
        """ Тестирование изменения привычки """
        self.data['place'] = 'test place update'
        response = self.client.put(
            f'/habits/update/{self.habit.json()["id"]}/',
            data=self.data,
            headers=self.headers
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_list_habits(self):
        """ Тестирования вывода списка привычек """

        response = self.client.get(
            '/habits/list/',
            headers=self.headers
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['count'], 1
        )

    def test_destroy_habit(self):
        """ Тестирование удаления привычки """

        response = self.client.delete(
            f'/habits/destroy/{self.habit.json()["id"]}/',
            data=self.data,
            headers=self.headers
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        response = self.client.delete(
            f'/habits/destroy/{self.habit.json()["id"]}/',
            data=self.data
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
