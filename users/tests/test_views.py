from django.contrib.auth import get_user
from django.test import TestCase, Client

from django.urls import reverse

from users.models import CustomUser
from family.models import *


class BaseViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', password='1234', name='test', color='#7542f5')

        self.client = Client()
        self.client.login(username='test', password='1234')

        self.family = Family.objects.create(name='Test Family')
        self.member = FamilyMember.objects.create(family=self.family, user=self.user)


class UserLogoutTest(BaseViewTest):
    def test_user_logout(self):
        self.client.force_login(self.user)
        url = reverse('users:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_non_user_logout(self):
        self.client.logout()
        url = reverse('users:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class ChangeDataTest(BaseViewTest):
    def test_changed_data(self):
        self.client.force_login(self.user)
        url = reverse('users:change_data')

        response = self.client.post(url, {'name': 'test_changed', 'color': '#b3b3b3'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'test_changed')
        self.assertEqual(self.user.color, '#b3b3b3')

    def test_non_changed_data(self):
        self.client.force_login(self.user)
        url = reverse('users:change_data')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'test')
        self.assertEqual(self.user.color, '#7542f5')

    def test_get(self):
        self.client.force_login(self.user)
        url = reverse('users:change_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile'))

    def test_logout_user(self):
        self.client.logout()
        url = reverse('users:change_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('users:login')}?next=/users/change-data/')

    def test_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('users:change_data')
        response = self.client.post(url, {'name': '', 'color': ''})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'test')
        self.assertEqual(self.user.color, '#7542f5')


class LoginTest(BaseViewTest):
    def test_login_view(self):
        self.client.logout()
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_login_view(self):
        self.client.logout()
        url = reverse('users:login')
        response = self.client.post(url, {'username': self.user.username, 'password': 1234})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_authorized_post_login_view(self):
        self.client.force_login(self.user)
        url = reverse('users:login')
        response = self.client.post(url, {'username': self.user.username, 'password': 1234})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_authorized_login_view(self):
        self.client.force_login(self.user)
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

# class CustomUserRegisterView(CreateView):
#     form_class = CustomUserRegisterForm
#     template_name = 'users/register.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         login(self.request, self.object)
#         return response

class RegisterTest(BaseViewTest):
    def test_register_view(self):
        self.client.logout()
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_authorize_register_view(self):
        self.client.force_login(self.user)
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_register_valid_post(self):
        self.client.logout()
        url = reverse('users:register')
        response = self.client.post(url, {'name':'test1', 'username':'test1',
                                          'password1':'zxcasdqwe2006', 'password2':'zxcasdqwe2006', 'color':'#b3b3b3'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.name, 'test1')
        user = CustomUser.objects.get(username='test1')
        self.assertNotEqual(user.password, 'zxcasdqwe2006')
        self.assertTrue(user.check_password('zxcasdqwe2006'))

    def test_register_password_mismatch(self):
        self.client.logout()
        url = reverse('users:register')

        response = self.client.post(url, {
            'name': 'test1',
            'username': 'test1',
            'password1': '12345678',
            'password2': 'DIFFERENT',
            'color': '#b3b3b3'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введенные пароли не совпадают.')
        self.assertFalse(CustomUser.objects.filter(username='test1').exists())

    def test_register_duplicate_username(self):
        self.client.logout()
        url = reverse('users:register')

        response = self.client.post(url, {
            'name': 'another',
            'username': 'test',  # уже есть в BaseViewTest
            'password1': 'zxcasdqwe2006',
            'password2': 'zxcasdqwe2006',
            'color': '#b3b3b3'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_register_auto_login(self):
        self.client.logout()
        url = reverse('users:register')

        self.client.post(url, {
            'name': 'test1',
            'username': 'test1',
            'password1': 'zxcasdqwe2006',
            'password2': 'zxcasdqwe2006',
            'color': '#b3b3b3'
        })

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'test1')