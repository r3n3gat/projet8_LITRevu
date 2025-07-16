# accounts/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='t@test.com',
            password='pw12345'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('pw12345'))
        self.assertTrue(user.is_active)

    def test_str(self):
        user = User(username='foo')
        self.assertEqual(str(user), 'foo')


class SignUpFormTest(TestCase):
    def test_signup_form_valid(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'username': 'new',
                'email': 'newuser@example.com',
                'password1': 'strongPass123',
                'password2': 'strongPass123',
            }
        )
        # Doit rediriger vers la home en cas de succès
        self.assertRedirects(response, reverse('core:home'))
        # L'utilisateur doit être créé en base
        self.assertTrue(User.objects.filter(username='new').exists())

    def test_login_form_invalid(self):
        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'nouser',
                'password': 'nopass',
            }
        )
        # On reste bien sur la page de connexion
        self.assertEqual(response.status_code, 200)
        # Vérifie la présence du message d'erreur en français
        self.assertContains(
            response,
            'Saisissez un nom d’utilisateur et un mot de passe valides',
            msg_prefix="Le message d'erreur en français doit apparaître"
        )
