from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

def is_element_present_by_id(driver, id):
    try: driver.find_element(By.ID, id)
    except NoSuchElementException as e: return False
    return True

def is_element_present_by_classname(driver, classname):
    try: driver.find_element(By.CLASS_NAME, classname)
    except NoSuchElementException as e: return False
    return True


class EndToEndTests(LiveServerTestCase):

    def setUp(self):
        self.username = f"testinguser_{''.join(random.choices(string.ascii_lowercase,k=8))}"
        self.password = "strong_password"
    

    def test_correct_signup(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get('http://127.0.0.1:8000/accounts/signup')

        username=driver.find_element(By.ID,"id_username")
        username.send_keys(self.username)

        password1=driver.find_element(By.ID,"id_password1")
        password1.send_keys(self.password)

        password2=driver.find_element(By.ID,"id_password2")
        password2.send_keys(self.password)


        button=driver.find_element(By.CLASS_NAME,"submit-btn")
        button.click()

        assert "/login" in driver.current_url
        assert is_element_present_by_id(driver,"login-title") is True

        driver.close()

    def test_incorrect_signup(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get('http://127.0.0.1:8000/accounts/signup')

        username=driver.find_element(By.ID,"id_username")
        username.send_keys(self.username)

        password1=driver.find_element(By.ID,"id_password1")
        password1.send_keys(self.password)

        password2=driver.find_element(By.ID,"id_password2")
        password2.send_keys("another_password")


        button=driver.find_element(By.CLASS_NAME,"submit-btn")
        button.click()

        assert "/login" not in driver.current_url
        assert is_element_present_by_id(driver,"error") is True

        driver.close()

        
        



