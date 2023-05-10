from trivia_qa import wizard101_trivia_questions_and_answers as wt
import difflib
import os
import time as t
from selenium.common.exceptions import *
import dill
from functions import WebDriver
from threadium import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pathlib
import requests
from bs4 import BeautifulSoup
from random import choice
from threadium import Threadium

class AutoTrivia():
    """Main module that automates the trivia"""
    def __init__(self):
        self.user_account = {}
        self.chromewebdriver = WebDriver()
        self.script_directory = pathlib.Path().absolute()
        self.chrome_driver_path = os.path.join('chromedriver.exe')
        self.has_quizes = True
    
    def setup(self):
        """Opens a unique driver per account and adds arguments"""
        for key, value in self.user_account.items():
            print(f"Starting thread for the user: {key}...")
            th = Thread(target=self.process_account, args=(key, value))
            th.start()
            th.join()  # Wait for the thread to complete before moving on to the next account
            print(f"Success! {key}'s thread is complete!")
        print("Success! All accounts have successfully completed the trivia!")

    def process_account(self, key, value):
        """Processes a single account"""
        th = Threadium(1)
        th.start_all(
            args=(key, value),
            single_target=self.run,
            profile_dir=[f"user-data-dir\\{key}-dir", f"{key}-user-data"],
    )
        
    def proxy_generator(self):
        response = requests.get("https://sslproxies.org/")
        soup = BeautifulSoup(response.content, 'html5lib')
        proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
        return proxy    
        
    def run(self, user, passwrd, driver):
        all_quizes = []
        # These are the default quizes that are available on the trivia site; you can add more if you want -- just make sure to add the quiz name to the list below
        quizes = [
        "Pirate101 Valencia Trivia", 
        "Wizard101 Adventuring Trivia", 
        "Wizard101 Conjuring Trivia", 
        "Wizard101 Magical Trivia", 
        "Wizard101 Marleybone Trivia", 
        "Wizard101 Mystical Trivia", 
        "Wizard101 Spellbinding Trivia", 
        "Wizard101 Spells Trivia", 
        "Wizard101 Wizard City Trivia", 
        "Wizard101 Zafaria Trivia"
        ]

        # generate a random proxy
        proxy = self.proxy_generator()
        Threadium().chrome_options.add_argument('--proxy-server=https://%s' % proxy['https'])
        print("Proxy currently being used: {}".format(proxy))

        driver.get("https://www.wizard101.com/quiz/trivia/game/kingsisle-trivia")

        # Switch to the tab with the Wizard101 website
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "Wizard101" in driver.title:
                break
        driver.delete_all_cookies()
        driver.refresh()
        t.sleep(5)
        self.chromewebdriver.clickCookies(driver=driver)

        # All the button xpath's/frames/clickables/etc. that are used in the script:
        username_button = '//*[@id="loginUserName"]'
        password_button = '//*[@id="loginPassword"]'
        login_button = '//*[@id="wizardLoginButton"]/tbody/tr/td[1]/div/div/input'
        quiz_header = 'darkerparchment_headermiddle'
        quiz = 'darkerparchment_pattern'
        get_results_button = '//*[@id="quizFormComponent"]/div[3]/div[3]/a'
        j_pop_frame_content = '//*[@id="jPopFrame_content"]'
        cliam_reward_button = '//*[@id="submit"]'
        kingsisle_trivia_page = '//*[@id="renderRegionDiv"]/tbody/tr[4]/td/div/table[2]/tbody/tr[2]/td[2]/p/b/a'

        # Wait for the username button to appear
        if driver.find_elements(By.XPATH, username_button):
            try:
                #This is the username button
                username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, username_button)))
                username.clear()
                username.send_keys(user)
                #This is the password button
                password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, password_button)))
                password.clear()
                password.send_keys(passwrd)
            
                # Wait for the login button to appear
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, login_button)))

                # Click the login button if it exists
                if driver.find_elements(By.XPATH, login_button):
                    try:
                        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, login_button)))
                        login_button.click()
                        t.sleep(5)  # Add a wait after clicking the button
                    except ElementClickInterceptedException:
                        print("User is already logged in!")

                self.chromewebdriver.clickCookies(driver=driver)
                self.chromewebdriver.solveVerification(driver=driver)
            except Exception as e:
                print("Error while logging in: {}".format(e))
        self.chromewebdriver.clickCookies(driver=driver)

        # Loop until all quizes are finished
        while len(quizes) > 0:
            # adds all the names from the image class name
            for i in driver.find_elements(By.CLASS_NAME, quiz_header):
                all_quizes.append(i.text)
            # Loop and picks a quiz until the entire question is loaded
            while self.has_quizes:
                # Checks the header to find a compitable quiz
                for i in driver.find_elements(By.CLASS_NAME, quiz_header):
                    try:
                        # If the quiz header is the same as the quiz name, click the image
                        if i.text == quizes[0]:
                            # This is the image that can be clicked
                            driver.find_elements(By.CLASS_NAME, quiz)[all_quizes.index(i.text)].click()
                            # Removes the quiz from the list
                            quizes.remove(quizes[0])
                            break
                    except IndexError:
                        # If there are no more quizes, break the loop
                        self.has_quizes = False
                        break
                #If the quiz questioned appear, break the while loop and continue
                if driver.find_elements(By.CLASS_NAME,'quizQuestion'):
                    break
            # If there are no more quizes, break the loop
            if self.has_quizes == False:
                break
            # otherwise continue with the quiz questions and answers 
            else:
                while True:
                    try:
                        #If the 'get results' button is visable, do the following:
                        if driver.find_elements(By.XPATH, get_results_button):
                            driver.refresh()  # refresh the page
                            #Clicks the 'get results' button
                            try:
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, get_results_button))).click()
                                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, j_pop_frame_content)))
                                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, cliam_reward_button))).click()
                            except TimeoutException:
                                driver.refresh()
                                continue 
                            driver.switch_to.default_content()
                            self.chromewebdriver.solveCaptcha(driver=driver)
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, kingsisle_trivia_page))).click()
                            if os.stat('data.pkl').st_size != 0:
                                with open(f'data.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                                    self.chromewebdriver.crowns_earned = dill.load(f)
                            self.chromewebdriver.crowns_earned += 10
                            print(f"You've recieved 10 crowns, with a lifetime total of {self.chromewebdriver.crowns_earned} crowns!")
                            try:
                                self.chromewebdriver.dump(self.chromewebdriver.crowns_earned)
                            except Exception as e:
                                print(e)
                            break
                        # Wait for the question to become visible
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'quizQuestion')))

                        # The question str
                        question = driver.find_element(By.CLASS_NAME, 'quizQuestion').text

                        # Find the closest matching question (some questions are outdated but close enough)
                        parsed_question = difflib.get_close_matches(question, wt.keys())
                        # Gets the value answer based on the question
                        answer = wt.get(parsed_question[0])

                        # Stores the answers
                        ANSWERS = []

                        # Wait for all 4 elements to become clickable
                        while True:
                            try:
                                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, 'nextQuestion')))
                                break
                            except TimeoutException:
                                # if element is not clickable within a second, wait again
                                continue

                        # Once all 4 elements are clickable, append the potential answers on-screen in order (removes unidentified symbols)
                        for i in driver.find_elements(By.CLASS_NAME, "answerText"):
                            # Removes the unidentified symbols
                            if '�' in i.text:
                                # Replaces the unidentified symbols with nothing
                                driver.execute_script(f"arguments[0].innerText = '{i.text.replace('�', '')}'", i)
                            ANSWERS.append(i.text)

                        # Finds the closest matching answer
                        parsed_answer = difflib.get_close_matches(answer, ANSWERS)

                        # Clicks on the box using the numbered box from the answer's index
                        answer_index = ANSWERS.index(parsed_answer[0])

                        # Clicks on the answer box
                        driver.find_elements(By.CLASS_NAME, "answerBox")[answer_index].click()

                        # Wait for the next question button to become clickable
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'nextQuestion')))

                        ANSWERS.clear()
                        driver.find_element(By.ID, 'nextQuestion').click()
                    except Exception as e:
                        # If there is an error, refresh the page and continue
                        print(f"Refreshing the page and continuing...")
                        driver.refresh()
                        continue
        print(f"All quizes have been completed for {user}'s account! Now moving on to the next account...")
        self.has_quizes = True
        driver.quit()
    # continue with your code
if __name__ == "__main__":
    # initialize the class and run the setup function to start the script 
    at = AutoTrivia()
    with open(os.path.join('text_files', 'accounts.txt'), 'r') as accounts:
        for i in accounts.readlines():
            at.user_account[i.split(' ')[0]] = i.split(' ')[1]
    at.setup()
