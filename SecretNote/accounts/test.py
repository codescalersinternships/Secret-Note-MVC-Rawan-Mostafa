from django.test import TestCase
from django.contrib.auth import get_user_model

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
        self.assertTrue(user.is_active)

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
