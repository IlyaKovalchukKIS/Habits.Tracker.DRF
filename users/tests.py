from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationMixin(APITestCase):
    def setUp(self):
        self.data = {
            "email": 'test_mail@dot.com',
            'password': 'test_password'
        }
        self.user = self.client.post(
            '/users/user/', data=self.data
        )
        self.user_token = self.client.post(
            '/users/token/', data=self.data
        )


class UserTestCase(UserRegistrationMixin, APITestCase):
    def test_create_user(self):
        """ Тестирование регистрации пользователя """

        self.assertEqual(
            self.user.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_token_user(self):
        """ Получение токена пользователем """

        self.assertEqual(
            self.user_token.status_code,
            status.HTTP_200_OK
        )

    def test_user_update(self):
        """ Изменение данных пользователя """

        response = self.client.put(
            f"/users/user/{self.user.json()["id"]}/",
            data={"password": 'test_update_password',
                  "email": 'test_mail@dot.com'},
            headers={"Authorization": f"Bearer {self.user_token.json()['access']}"}
        )
        self.assertEqual(
            response.json()['password'], 'test_update_password'
        )

    def test_user_delete(self):
        """ Удаления пользователя """

        user_id = self.user.json()["id"]
        access_token = self.user_token.json()['access']

        response = self.client.delete(
            f'/users/user/{user_id}/', headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
