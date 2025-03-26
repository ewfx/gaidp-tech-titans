import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class FrontendTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def test_page_title(self):
        self.assertIn("Tech Titans", self.driver.title)

    def test_upload_form(self):
        driver = self.driver
        upload_form = driver.find_element(By.ID, "upload-form")
        self.assertIsNotNone(upload_form)

        file_input = driver.find_element(By.NAME, "file")
        instructions_input = driver.find_element(By.NAME, "instructions")
        submit_button = driver.find_element(By.ID, "submit-button")

        self.assertIsNotNone(file_input)
        self.assertIsNotNone(instructions_input)
        self.assertIsNotNone(submit_button)

    def test_upload_functionality(self):
        driver = self.driver
        file_input = driver.find_element(By.NAME, "file")
        instructions_input = driver.find_element(By.NAME, "instructions")
        submit_button = driver.find_element(By.ID, "submit-button")

        file_input.send_keys("c:\\path\\to\\test.csv")
        instructions_input.send_keys("Example instructions")
        submit_button.click()

        # Check for success message
        success_message = driver.find_element(By.ID, "success-message")
        self.assertIn("Processing completed!", success_message.text)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
