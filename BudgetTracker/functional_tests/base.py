from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

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
