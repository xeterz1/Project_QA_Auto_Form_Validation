import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

URL = os.environ.get("FORM_URL", "http://localhost:8000/")

@pytest.fixture
def driver():
    d = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield d
    d.quit()

def fill_form(d, name, email, age, message):
    d.find_element(By.ID, "name").send_keys(name)
    d.find_element(By.ID, "email").send_keys(email)
    d.find_element(By.ID, "age").send_keys(str(age))
    d.find_element(By.ID, "message").send_keys(message)

def test_valid_submit_shows_success_banner(driver):
    driver.get(URL)
    fill_form(driver, "Akram", "akram@example.com", 26, "Hello!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    banner = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "formMessage"))
    ).text.lower()
    assert "submitted successfully" in banner

def test_invalid_email_server_rejects_even_if_html5_allows(driver):
    # 'akram@domain' typically passes HTML5, but fails our Python regex (no TLD)
    driver.get(URL)
    fill_form(driver, "Akram", "akram@domain", 26, "Hi")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    text = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "formMessage"))
    ).text.lower()
    assert "invalid email" in text

def test_age_above_max_is_rejected_by_server(driver):
    # HTML has min=1 but no max; backend enforces <= 120
    driver.get(URL)
    fill_form(driver, "Akram", "akram@example.com", 121, "Hi")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    text = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "formMessage"))
    ).text.lower()
    assert "invalid age" in text

def test_invalid_email_html5_is_blocked(driver):
    # This one should be blocked by browser (no POST), so no new message shown
    driver.get(URL)
    fill_form(driver, "Akram", "akram_at_example.com", 26, "Hi")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    valid = driver.execute_script("return document.querySelector('#smartForm').checkValidity();")
    assert valid is False
    # Banner should not say success
    assert "successfully" not in driver.find_element(By.ID, "formMessage").text.lower()
