from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from uuid import uuid4

class CreateAccountTest(FunctionalTest):
          
    def test_non_user_invited_to_create_account(self):
        self.selenium.get(f'{self.live_server_url}') 
        self.text_container = self.selenium.find_element_by_class_name("create_account_link_container")
        self.link_container = self.selenium.find_element_by_css_selector("a[class=sign_up_link]")
        self.assertIn("Don\'t have an account?", self.text_container.text)
        self.assertIn("Sign Up", self.link_container.text)

    def test_non_user_taken_to_account_creation_on_sign_up_click(self):
        self.selenium.get(f'{self.live_server_url}') 
        self.text_container = self.selenium.find_element_by_class_name("create_account_link_container")
        self.link_container = self.selenium.find_element_by_css_selector("a[class=sign_up_link]")
        self.link_container.click()
        create_account_page_heading = self.selenium.find_element(By.ID, "create_account_page_heading").text
        self.assertIn("Create an Account", create_account_page_heading)

    def test_non_user_can_create_account(self):
        self.selenium.get(f'{self.live_server_url}/members/create_account') 
        username = self.selenium.find_element_by_css_selector("input[name=username]")
        test_username = "testUser"
        username.send_keys(test_username)
        password = self.selenium.find_element_by_css_selector("input[name=password1]")
        test_password = str( uuid4() )
        password.send_keys(test_password)
        password_confirmation = self.selenium.find_element_by_css_selector("input[name=password2]")
        password_confirmation.send_keys(test_password)
        submit_button = self.selenium.find_element_by_css_selector("input[value=Submit]")
        submit_button.click()
        start_budget_invitation_heading = self.selenium.find_element(By.ID, "start_budget_invitation_heading").text
        self.assertIn("Start your budget today.", start_budget_invitation_heading)
        navbar_username = self.selenium.find_element_by_class_name("navbar_username").text
        self.assertEqual(test_username, navbar_username)