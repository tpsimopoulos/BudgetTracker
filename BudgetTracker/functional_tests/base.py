from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from uuid import uuid4
from selenium.webdriver.common.by import By
import time

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        cls.selenium = webdriver.Firefox(firefox_options=opts)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.selenium.quit()
    
    def wait(fn):
        '''
        Decorator that waits a max of 10 seconds for function 
        to return non-exception/non-error else throws exception/error.
        '''
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e 
                    time.sleep(0.5)
        return modified_fn

    def create_account_and_return_test_user_credentials(self):
        self.selenium.get(f'{self.live_server_url}/members/create_account') 
        test_username = "testUser"
        test_password = str( uuid4() )
        username_input_field = self.selenium.find_element_by_css_selector("input[name=username]")
        username_input_field.send_keys(test_username)
        password_input_field = self.selenium.find_element_by_css_selector("input[name=password1]")
        password_input_field.send_keys(test_password)
        password_confirmation = self.selenium.find_element_by_css_selector("input[name=password2]")
        password_confirmation.send_keys(test_password)
        submit_button = self.selenium.find_element_by_css_selector("input[value=Submit]")
        submit_button.click()
        start_budget_invitation_heading = self.selenium.find_element(By.ID, "start_budget_invitation_heading")
        self.assertIn("Start your budget today.", start_budget_invitation_heading.text)
        navbar_username = self.selenium.find_element_by_class_name("navbar_username")
        self.assertEqual(test_username, navbar_username.text)
        return test_username, test_password
    
    def send_keys_and_click_submit_for_login_func_test(self, username, password):
        username_input_field = self.selenium.find_element_by_css_selector("input[name=username]")
        username_input_field.send_keys(username)
        password_input_field = self.selenium.find_element_by_css_selector("input[name=password]")
        password_input_field.send_keys(password)
        submit_button = self.selenium.find_element_by_css_selector("input[value=Submit]")
        submit_button.click()

    def send_keys_and_click_submit_for_reset_password_func_test(self, username, password1, password2):
        forgot_password_link = self.selenium.find_element(By.ID, "forgot_password_link")
        forgot_password_link.click()
        username_input_field = self.selenium.find_element_by_css_selector("input[name=username]")
        username_input_field.send_keys(username)
        password_input_field = self.selenium.find_element_by_css_selector("input[name=password]")
        password_input_field.send_keys(password1)
        password_confirmation_input_field = self.selenium.find_element_by_css_selector("input[name=password_confirmation]")
        password_confirmation_input_field.send_keys(password2)
        reset_button = self.selenium.find_element_by_css_selector("input[value=Reset]")
        reset_button.click()

    def send_keys_and_click_submit_for_create_account_func_test(self, username, password1, password2):
        self.link_container = self.selenium.find_element_by_css_selector("a[class=sign_up_link]")
        self.link_container.click()
        username_input_field = self.selenium.find_element_by_css_selector("input[name=username]")
        username_input_field.send_keys(username)
        password_input_field = self.selenium.find_element_by_css_selector("input[name=password1]")
        password_input_field.send_keys(password1)
        password_confirmation_input_field = self.selenium.find_element_by_css_selector("input[name=password2]")
        password_confirmation_input_field.send_keys(password2)
        submit_button = self.selenium.find_element_by_css_selector("input[value=Submit]")
        submit_button.click()

    def create_starter_budget_with_food_category(self):
        self.create_account_and_return_test_user_credentials()
        submit_button = self.selenium.find_element_by_css_selector("input[value=Begin]")
        submit_button.click()
        add_category_input_field = self.selenium.find_element_by_css_selector("input[id='0']")
        add_category_input_field.send_keys("Food")
        continue_button = self.selenium.find_element_by_css_selector("input[value=Continue]")
        continue_button.click()
        allowance_input_field = self.selenium.find_element_by_css_selector("input[name=Food]")
        allowance = "25"
        allowance_input_field.send_keys("25")
        submit_button = self.selenium.find_element_by_css_selector("input[value=Submit]")
        submit_button.click()
        remaining_allowance_heading = self.selenium.find_element(By.ID, "remaining_allowance_heading")
        self.assertEqual("Total remaining allowance.", remaining_allowance_heading.text)
        remaining_allowance_amount = self.selenium.find_element(By.ID, "remaining_allowance_amount")
        self.assertEqual(f'${allowance}.00', remaining_allowance_amount.text)