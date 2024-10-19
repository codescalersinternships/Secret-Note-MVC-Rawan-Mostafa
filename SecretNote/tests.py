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
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def signup(self,username,password1,password2):
        self.driver.get('http://127.0.0.1:8000/accounts/signup')

        username_field=self.driver.find_element(By.ID,"id_username")
        username_field.send_keys(username)

        password1_field=self.driver.find_element(By.ID,"id_password1")
        password1_field.send_keys(password1)

        password2_field=self.driver.find_element(By.ID,"id_password2")
        password2_field.send_keys(password2)


        button=self.driver.find_element(By.CLASS_NAME,"submit-btn")
        button.click()

    def login(self,username,password):
        self.driver.get('http://127.0.0.1:8000/accounts/login')

        username_field=self.driver.find_element(By.ID,"id_username")
        username_field.send_keys(username)

        password_field=self.driver.find_element(By.ID,"id_password")
        password_field.send_keys(password)


        button=self.driver.find_element(By.CLASS_NAME,"submit-btn")
        button.click()

    def test_correct_signup(self):
        self.signup(self.username,self.password,self.password)
        assert "/login" in self.driver.current_url
        assert is_element_present_by_id(self.driver,"login-title") is True
        self.driver.close()

    def test_incorrect_signup(self):
        self.signup(self.username,self.password,"another_password")
        assert "/login" not in self.driver.current_url
        assert is_element_present_by_id(self.driver,"error") is True
        self.driver.close()

    def test_correct_login(self):
        self.signup(self.username,self.password,self.password)
        self.login(self.username,self.password)
        assert "/notes" in self.driver.current_url
        assert is_element_present_by_id(self.driver,"create-note-btn") is True

        self.driver.close()

    def test_incorrect_username_login(self):
        self.signup(self.username,self.password,self.password)
        self.login("another_username",self.password)

        assert "/notes" not in self.driver.current_url
        assert "/login" in self.driver.current_url
        assert is_element_present_by_id(self.driver,"create-note-btn") is False
        self.driver.close()

    def test_incorrect_password_login(self):
        self.signup(self.username,self.password,self.password)
        self.login(self.username,"another_password")

        assert "/notes" not in self.driver.current_url
        assert "/login" in self.driver.current_url
        assert is_element_present_by_id(self.driver,"create-note-btn") is False
        self.driver.close()


