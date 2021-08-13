from .base import FunctionalTest
from selenium.webdriver.common.by import By
import time
from uuid import uuid4


class ResetPasswordTest(FunctionalTest):

    def test_user_can_reset_password(self):
        username, password = super().create_account_and_return_test_user_credentials()
        new_password = str( uuid4() )
        self.selenium.get(f'{self.live_server_url}/members/logout_user')
        self.send_keys_and_click_submit_for_reset_password_func_test(username, new_password, new_password)
        login_page_heading = self.selenium.find_element(By.ID, "login_page_heading")
        self.assertEqual("Login", login_page_heading.text)

    def test_error_thrown_when_user_types_in_diferent_passwords_when_resetting_password(self):
        username, password = super().create_account_and_return_test_user_credentials()
        self.selenium.get(f'{self.live_server_url}/members/logout_user')
        diff_password1 = "diff_pass598"
        diff_password2 = "diff_pass895"
        self.send_keys_and_click_submit_for_reset_password_func_test(username, diff_password1, diff_password2)
        error_message = self.selenium.find_element(By.ID, "error_message")
        self.assertEqual("Passwords don't match.", error_message.text)

    def test_error_thrown_when_user_tries_to_reset_password_using_current_password(self):
        username, password = super().create_account_and_return_test_user_credentials()
        self.selenium.get(f'{self.live_server_url}/members/logout_user')
        self.send_keys_and_click_submit_for_reset_password_func_test(username, password, password)
        error_message = self.selenium.find_element(By.ID, "error_message")
        self.assertEqual("New password can't be the same as current password.", error_message.text)

    def test_errors_removed_on_keypress(self):
        self.test_error_thrown_when_user_tries_to_reset_password_using_current_password()
        username_input_field = self.selenium.find_element_by_css_selector("input[name=username]")
        username_input_field.send_keys("i")
        error_message = self.selenium.find_element(By.ID, "error_message")
        self.assertFalse(error_message.is_displayed())

    def test_user_notified_after_successful_password_reset(self):
        username, password = super().create_account_and_return_test_user_credentials()
        self.selenium.get(f'{self.live_server_url}/members/logout_user')
        self.send_keys_and_click_submit_for_reset_password_func_test(username, "new_test_pass775", "new_test_pass775")
        password_reset_message = self.selenium.find_element(By.ID, "password_reset_message")
        self.assertEqual("Your password has been successfully reset!", password_reset_message.text)