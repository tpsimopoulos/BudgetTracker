from .base import FunctionalTest
from selenium.webdriver.common.by import By
import time


class LoginTest(FunctionalTest):

    def test_user_redirected_to_login_if_not_logged_in(self):
        self.selenium.get(f'{self.live_server_url}') 
        login_page_heading = self.selenium.find_element(By.ID, "login_page_heading")
        self.assertEqual("Login", login_page_heading.text)

    def test_user_can_login(self):
        username, password = super().create_account_and_return_test_user_credentials()
        self.selenium.get(f'{self.live_server_url}/members/logout_user')
        self.send_keys_and_click_submit_for_login_func_test(username, password)
        start_budget_invitation_heading = self.selenium.find_element(By.ID, "start_budget_invitation_heading")
        self.assertIn("Start your budget today.", start_budget_invitation_heading.text)

    def test_error_thrown_if_user_login_with_correct_username_but_incorrect_password(self):
        username, password = super().create_account_and_return_test_user_credentials()
        self.selenium.get(f'{self.live_server_url}/members/logout_user') 
        self.send_keys_and_click_submit_for_login_func_test(username, "incorrect_pass329")
        error_message = self.selenium.find_element(By.ID, "error_message")
        self.assertIn("Incorrect username or password provided.", error_message.text)

    def test_error_thrown_if_user_login_with_correct_password_but_incorrect_username(self):
        username, password = super().create_account_and_return_test_user_credentials()
        self.selenium.get(f'{self.live_server_url}/members/logout_user')
        self.send_keys_and_click_submit_for_login_func_test("incorrect_username", password) 
        error_message = self.selenium.find_element(By.ID, "error_message")
        self.assertIn("Incorrect username or password provided.", error_message.text)

    def test_errors_removed_on_keypress(self):
        self.test_error_thrown_if_user_login_with_correct_password_but_incorrect_username()
        username_input_field = self.selenium.find_element_by_css_selector("#username")
        username_input_field.send_keys("i")
        error_message = self.selenium.find_element(By.ID, "error_message")
        self.assertFalse(error_message.is_displayed())



        