from django.test import TestCase


class AccountCreationTest(TestCase):

    def test_create_account_template_used_if_user_clicks_sign_up_at_index(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'authenticate/login.html')

    