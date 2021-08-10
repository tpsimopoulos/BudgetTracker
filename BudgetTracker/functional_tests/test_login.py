from .base import FunctionalTest
from selenium.webdriver.common.by import By

class LoginTest(FunctionalTest):

    def test_user_redirected_to_login_if_not_logged_in(self):
        self.selenium.get(f'{self.live_server_url}') 
        self.selenium.find_element(By.ID, "login_page_heading")

    