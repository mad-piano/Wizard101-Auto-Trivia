from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from answers import *
import difflib



def trivia():
    #configs
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get("https://www.wizard101.com/quiz/trivia/game/kingsisle-trivia")

    username = driver.find_element_by_xpath('//*[@id="loginUserName"]')
    password = driver.find_element_by_xpath('//*[@id="loginPassword"]')
    login = driver.find_element_by_xpath('//*[@id="wizardLoginButton"]/tbody/tr/td[1]/div/div/input')

    #logs the user in
    username.send_keys("enter your username here")
    time.sleep(1)
    password.send_keys("enter your password here")
    time.sleep(1)
    login.click()

    input("Press enter when you're on the quiz page... ")

    while True:
        try:
            #Stores the potential answers
            ANSWERS = []
            #The question str
            question = driver.find_element_by_class_name("quizQuestion")
            #Find the closest matching question (some questions are outdated but close enough)
            parsed_question = difflib.get_close_matches(question.text, Wizard101_Trivia.keys())
            #Gets the value answer based of the question
            answer = Wizard101_Trivia.get(parsed_question[0]) 
            #The next question button
            next_question_button = driver.find_element_by_id('nextQuestion')


            #Prints the q&a
            print(f"QUESTION:{question.text}")
            print(f"ANSWER:{answer}")
            print(" ")

            #appends all the potential answers on-screen in order
            for i in driver.find_elements_by_class_name("answerText"):
                ANSWERS.append(i.text)

            #Finds the closest matching answer
            parsed_answer = difflib.get_close_matches(answer, ANSWERS)

            #Clicks on the box using the numbered box from the answer's index
            driver.find_elements_by_class_name("answerBox")[ANSWERS.index(parsed_answer[0])].click()
            time.sleep(1)
            next_question_button.click()
            ANSWERS.clear() # clear the list to prepare the next answers
            time.sleep(5)
        except Exception as e:
            input("Press enter when you're on the quiz page... ")



if __name__ == "__main__":
    trivia()


