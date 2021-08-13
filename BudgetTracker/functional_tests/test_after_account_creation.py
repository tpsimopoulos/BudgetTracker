from .base import FunctionalTest
from selenium.webdriver.common.by import By
from uuid import uuid4
import time

class AfterAccountCreationTest(FunctionalTest):

    def test_user_can_create_budget_after_account_creation(self):
        super().create_starter_budget_with_food_category()

    def test_user_not_allowed_to_create_budget_with_existing_category(self):
        super().create_starter_budget_with_food_category()
        self.selenium.get(f'{self.live_server_url}/edit_budget')
        add_category_input_field = self.selenium.find_element_by_css_selector("input[id='0']")
        add_category_input_field.send_keys("Food")
        continue_button = self.selenium.find_element_by_css_selector("input[value=Continue]")
        continue_button.click()
        error_message = self.selenium.find_element(By.ID, "error_message")
        self.assertIn("Food already exists in your budget", error_message.text)