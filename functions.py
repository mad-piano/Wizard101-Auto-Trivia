import time as t
import dill
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

# The class below contains important functions used in the main.py file
class WebDriver():
    def __init__(self): 
        self.crowns_earned = 0
    def dump(self, obj):
        '''
        Dumps the data to a file.

        Parameters:
        - obj: The object to dump to the file.

        The function dumps the data to a file in the format "Total Lifetime Crowns Earned: [insert dumped data here]".
        '''
        # Dumps the data to a file in the format "Total Lifetime Crowns Earned: [insert dumped data here]"
        with open(os.path.join("text_files", "data.txt"), 'w') as f:
            f.write(f'Total Lifetime Crowns Earned: {obj}')
            dill.dump(obj, f)
    def retry_captcha(self, driver):
        """
        Retries the captcha if it fails.

        This function clicks the "take another quiz" button to retry the captcha
        if it encounters one of several exceptions, including NoSuchElementException,
        StaleElementReferenceException, and TimeoutException. It then switches to the
        captcha iframe and clicks on the buster button to solve the captcha.

        Args:
            driver (WebDriver): The Selenium webdriver instance.

        Returns:
            None

        Raises:
            None
        """
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quizFormComponent"]/div[3]/div[3]/a'))).click()
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="jPopFrame_content"]')))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]'))).click()
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="wrapperWizard101A"]/div[3]/div[2]/iframe')))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]'))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quizFormComponent"]/div[3]/div[2]/div/a'))).click()
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
    def solveCaptcha(self, driver): 
        '''
        Solves the captcha at the end of the quiz, automatically re-does the captcha if needed.

        Parameters:
        - driver: The web driver instance to use for interacting with the quiz website.

        The function first waits for the captcha i-frame to be available, then clicks the "buster" button to solve the captcha.
        If the quiz is a Kingisle quiz, the function breaks out of the loop and returns control to the caller.
        If there is an error while solving the captcha, the function refreshes the page and tries again.
        '''
        while True:
            try:
                # if the buster button is present, click it
                if driver.find_elements(By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]'): # Recaptcha
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]'))).click() # buster
                # otherwise, click the buster button in the i-frame
                else:
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="jPopFrame_content"]'))) # Recaptcha 
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="wrapperWizard101A"]/div[3]/div[2]/iframe'))) # verification captcha i-frame
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]'))).click() # buster button
                    driver.switch_to.default_content()
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quizFormComponent"]/div[3]/div[2]/div/a'))).click() # take another quiz button
                    t.sleep(3)
                    # if the quiz is a kingisle quiz, break out of the loop
                    if driver.find_elements(By.XPATH, '//*[@id="renderRegionDiv"]/tbody/tr[4]/td/div/table[2]/tbody/tr[2]/td[2]/p/b/a'): # kingisle quiz
                        break
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                print("Captcha failed, restarting captcha proccess......")
                driver.refresh()
                self.retry_quiz(driver)
                t.sleep(3)
                # if the quiz is a kingisle quiz, break out of the loop
                if driver.find_elements(By.XPATH, '//*[@id="renderRegionDiv"]/tbody/tr[4]/td/div/table[2]/tbody/tr[2]/td[2]/p/b/a'): # kingisle quiz
                    break
    def solveVerification(self, driver): 
        '''Solves a captcha if the verification message pops up during login.

        Args:
            driver: An instance of the Selenium WebDriver used to control the browser.

        Description:
            If the verification message pops up during login, this function solves the captcha using the Buster extension. It first switches to the verification iframe and clicks the recaptcha button. If the Buster extension is installed, it clicks the "I'm not a robot" button and waits for 10 seconds to let the extension solve the captcha. If the captcha fails, it raises an error message and re-attempts the captcha. Finally, it clicks the "verify login" button and completes the login process.

        Returns:
            None
        '''
        # if the verification message pops up during login do the following:
        if driver.find_elements(By.XPATH, '//*[@id="jPopFrame_content"]'):  # if the verification message pops up
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="jPopFrame_content"]')) # captcha 
            # verify login button
            while driver.find_elements(By.XPATH, '//*[@id="bp_login"]'): # if the verify login button is present
                try:
                    # click the captcha button
                    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="recaptcha"]/div/div/iframe')) # captcha i-frame
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]'))) # recaptcha button
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-anchor"]'))).click() # captcha button
                    driver.switch_to.default_content()
                    
                    # if the buster button is present, click it
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="jPopFrame_content"]'))) # Recaptcha 
                    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="wrapperWizard101A"]/div[3]/div[4]/iframe'))) # verification captcha i-frame
                    # if the buster button is present, click it (Buster extension) make sure to switch to default content first
                    if driver.find_elements(By.XPATH, '//*[@id="rc-audio"]/div[8]/div[2]/div[1]/div[1]/div[4]'): # buster
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-audio"]/div[8]/div[2]/div[1]/div[1]/div[4]'))).click() # buster
                        driver.switch_to.default_content()
                    else:
                        driver.switch_to.default_content()

                        #NOTE:For Buster extension turn off "simulate user interactions" in the settings!!!
                        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="jPopFrame_content"]'))) # Recaptcha 
                        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="wrapperWizard101A"]/div[3]/div[4]/iframe'))) # verification captcha i-frame
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]'))).click() # buster button
                        t.sleep(10)
                        driver.switch_to.default_content()
                        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="jPopFrame_content"]')) # captcha i-frame

                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="bp_login"]'))).click() # verify login button
                    break
                except Exception:
                    print("Restarting verification proccess......")
                    driver.refresh()
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wizardLoginButton"]/tbody/tr/td[1]/div/div/input'))) # login button
                    wizard_login_button = driver.find_element(By.XPATH, '//*[@id="wizardLoginButton"]/tbody/tr/td[1]/div/div/input') # login button
                    wizard_login_button.click()
                    continue
    def clickCookies(self, driver):
            """
            If the cookie button is present, clicks the 'accept all' button and rejects all others.

            Args:
                driver (WebDriver): An instance of a WebDriver used to automate a browser.

            Returns:
                None.

            Raises:
                WebDriverException: If there is an issue with finding or clicking the cookie button.

            """
            # cookie button accept all
            cookie_button_xpath = '//*[@id="onetrust-accept-btn-handler"]'

            while True:
                if driver.find_elements(By.XPATH, cookie_button_xpath):  # if the cookie button is present
                    try:
                        cookie_button = WebDriverWait(driver, 2.5).until(EC.element_to_be_clickable((By.XPATH, cookie_button_xpath)))
                        cookie_button.click()
                        t.sleep(1.5)  # Add a wait after clicking the button
                    except (ElementClickInterceptedException, TimeoutException):
                        print("Cookie button not present.")
                        break
                else:
                    break

