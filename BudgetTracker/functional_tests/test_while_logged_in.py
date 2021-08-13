from .base import FunctionalTest
from selenium.webdriver.common.by import By
from uuid import uuid4

class WhileLoggedInTest(FunctionalTest):

    def test_user_notified_they_already_have_account_after_clicking_create_account(self):
        username, password = super().create_account_and_return_test_user_credentials()
        create_account_button = self.selenium.find_element_by_link_text("Create Account")
        create_account_button.click()
        has_existing_account_message = self.selenium.find_element(By.ID, "has_existing_account_message")
        self.assertEqual(f'Account already exists for {username}', has_existing_account_message.text)