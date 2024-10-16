from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
class TestSignup(TestCase):
    def test_signup_correctly(self):
        data = {
            'username': 'test_user',
            'password1': 'strong_password',
            'password2': 'strong_password',
        }
        response = self.client.post('/accounts/signup/', data=data, follow=True)
        self.assertRedirects(response, '/accounts/login/')
        user = get_user_model().objects.get(username=data['username'])
        self.assertIsNotNone(user)

    def test_signup_incorrectly(self):
        data = {
            'username': 'test_user',
            'password1': 'strong_passworc',
            'password2': 'strong_password',
        }
        response = self.client.post('/accounts/signup/', data=data, follow=True)
        self.assertNotContains(response, 'login')
        try:
            user = get_user_model().objects.get(username=data['username'])
            self.fail("Testcase should have failed due to incorrect password confirmation")  
        except get_user_model().DoesNotExist as e:
            self.assertEqual(str(e), "User matching query does not exist.")

class TestLogin(TestCase):
    def test_login_correctly(self):
        user = get_user_model().objects.create_user(username='test_user', password='strong_password')
        data = {
            'username': 'test_user',
            'password': 'strong_password'
        }
        response = self.client.post('/accounts/login/', data=data,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertRedirects(response, '/notes/')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_incorrectly(self):
        user = get_user_model().objects.create_user(username='test_user', password='strong_password')
        data = {
            'username': 'test_user',
            'password': 'strong_passwors'
        }
        response = self.client.post('/accounts/login/', data=data,follow=True)
        self.assertNotContains(response, 'notes')
        self.assertFalse(response.context['user'].is_authenticated)

