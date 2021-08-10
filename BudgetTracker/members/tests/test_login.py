from django.test import TestCase


class LoginTest(TestCase):

    def test_login_template_used_if_user_not_logged_in_and_visits_index(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'authenticate/login.html')

    