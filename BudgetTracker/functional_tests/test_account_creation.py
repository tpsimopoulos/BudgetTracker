from .base import FunctionalTest
from selenium.webdriver.common.by import By
from uuid import uuid4


class CreateAccountTest(FunctionalTest):
          
    def test_non_user_invited_to_create_account(self):
        self.selenium.get(f'{self.live_server_url}') 
        self.text_container = self.selenium.find_element_by_class_name("create_account_link_container")
        self.link_container = self.selenium.find_element_by_css_selector("a[class=sign_up_link]")
        self.assertIn("Don\'t have an account?", self.text_container.text)
        self.assertEqual("Sign Up", self.link_container.text)

    def test_non_user_taken_to_account_creation_on_sign_up_click(self):
        self.selenium.get(f'{self.live_server_url}') 
        self.text_container = self.selenium.find_element_by_class_name("create_account_link_container")
        self.link_container = self.selenium.find_element_by_css_selector("a[class=sign_up_link]")
        self.link_container.click()
        create_account_page_heading = self.selenium.find_element(By.ID, "create_account_page_heading")
        self.assertEqual("Create an Account", create_account_page_heading.text)

    def test_non_user_can_create_account(self):
        super().create_account_and_return_test_user_credentials()

    def test_error_thrown_when_user_types_in_username_that_already_exists_when_creating_account(self):
        username, password = super().create_account_and_return_test_user_credentials()
        self.selenium.get(f'{self.live_server_url}/members/logout_user') 
        test_password = str( uuid4() )
        self.send_keys_and_click_submit_for_create_account_func_test(username, test_password, test_password)
        error_message = self.selenium.find_element_by_class_name("username_error_field")
        self.assertTrue(error_message.is_displayed())

    def test_username_errors_removed_on_keypress(self):
        self.test_error_thrown_when_user_types_in_username_that_already_exists_when_creating_account()
        username_input_field = self.selenium.find_element(By.ID, "id_username")
        username_input_field.send_keys("i")
        error_message = self.selenium.find_element_by_class_name("username_error_field")
        self.assertFalse(error_message.is_displayed())

    def test_error_thrown_when_user_types_in_diferent_passwords_when_creating_account(self):
        self.selenium.get(f'{self.live_server_url}') 
        test_username = "testUser"
        diff_password1 = "non_matching_pass976"
        diff_password2 = "non_matching_pass453"
        self.send_keys_and_click_submit_for_create_account_func_test(test_username, diff_password1, diff_password2)
        error_message = self.selenium.find_element_by_class_name("password_error_field")
        self.assertTrue(error_message.is_displayed())

    def test_password_errors_removed_on_keypress(self):
        self.test_error_thrown_when_user_types_in_diferent_passwords_when_creating_account()
        password_input_field = self.selenium.find_element(By.ID, "id_password1")
        password_input_field.send_keys("i")
        error_message = self.selenium.find_element_by_class_name("password_error_field")
        self.assertFalse(error_message.is_displayed())

        