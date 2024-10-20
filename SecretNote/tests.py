from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from django.conf import settings
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
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

def is_element_present_by_css(driver, css):
    try: driver.find_element(By.CSS_SELECTOR, css)
    except NoSuchElementException as e: return False
    return True


class EndToEndTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True  
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        self.username = f"testinguser_{''.join(random.choices(string.ascii_lowercase,k=8))}"
        self.password = "strong_password"

    def signup(self,username,password1,password2):
        self.driver.get(f"{self.live_server_url}/accounts/signup")

        username_field=self.driver.find_element(By.ID,"id_username")
        username_field.send_keys(username)

        password1_field=self.driver.find_element(By.ID,"id_password1")
        password1_field.send_keys(password1)

        password2_field=self.driver.find_element(By.ID,"id_password2")
        password2_field.send_keys(password2)


        button=self.driver.find_element(By.CLASS_NAME,"submit-btn")
        button.click()

    def login(self,username,password):
        self.driver.get(f"{self.live_server_url}/accounts/login")

        username_field=self.driver.find_element(By.ID,"id_username")
        username_field.send_keys(username)

        password_field=self.driver.find_element(By.ID,"id_password")
        password_field.send_keys(password)


        button=self.driver.find_element(By.CLASS_NAME,"submit-btn")
        button.click()

    def create_note(self,title,content,date,views):
        create_note_button=self.driver.find_element(By.ID,"create-note-btn")
        create_note_button.click()

        title_field=self.driver.find_element(By.ID,"title")
        title_field.send_keys(title)

        title_field=self.driver.find_element(By.ID,"content")
        title_field.send_keys(content)

        expiration_field=self.driver.find_element(By.ID,"expiration")
        expiration_field.send_keys(date)

        max_views_field=self.driver.find_element(By.ID,"max_views")
        max_views_field.send_keys(views)

        create_button=self.driver.find_element(By.ID,"create-btn")
        create_button.click()

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

    def test_correct_create_note(self):
        self.signup(self.username,self.password,self.password)
        self.login(self.username,self.password)

        assert is_element_present_by_id(self.driver,"no-notes") is True

        self.create_note("test-title","test-content","12/10/2024",2)
        
        assert "create" not in self.driver.current_url
        assert is_element_present_by_id(self.driver,"no_notes") is False

        latest_note_title=self.driver.find_elements(By.CLASS_NAME,"title")
        assert latest_note_title[len(latest_note_title)-1].text == "test-title"

    def test_empty_fields_create_note(self):
        self.signup(self.username,self.password,self.password)
        self.login(self.username,self.password)

        assert is_element_present_by_id(self.driver,"no-notes") is True

        self.create_note("","test-content","12/10/2024",2)
        
        assert "/notes/create" in self.driver.current_url
        assert is_element_present_by_classname(self.driver,"errorlist")

    def test_past_date_create_note(self):
        self.signup(self.username,self.password,self.password)
        self.login(self.username,self.password)

        assert is_element_present_by_id(self.driver,"no-notes") is True

        self.create_note("test-title","test-content","12/10/2023",2)
        
        assert "/notes/create" in self.driver.current_url
        assert is_element_present_by_classname(self.driver,"errorlist")


    def test_delete_on_max_views(self):
        self.signup(self.username,self.password,self.password)
        self.login(self.username,self.password)

        assert is_element_present_by_id(self.driver,"no-notes") is True

        self.create_note("test-title","test-content","12/10/2024",3)

        latest_note_button=self.driver.find_elements(By.ID,"view-btn")
        latest_note_button[len(latest_note_button)-1].click()
        views=self.driver.find_element(By.ID,"views")
        assert views.text == "Views: 1"
        self.driver.back()
        latest_note_button[len(latest_note_button)-1].click()
        views=self.driver.find_element(By.ID,"views")
        assert views.text == "Views: 2"
        self.driver.back()
        latest_note_button[len(latest_note_button)-1].click()
        views=self.driver.find_element(By.ID,"views")
        assert views.text == "Views: 3"
        self.driver.back()
        latest_note_button[len(latest_note_button)-1].click()
        assert self.driver.find_element(By.CSS_SELECTOR,"body") .text == "This note has either expired or reached its maximum views and got deleted"