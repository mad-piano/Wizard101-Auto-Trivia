# Wizard101-Auto-Trivia

## Purpose
This is a program that will automatically answer Wizard101 trivia questions; it currently can solve all the Trivia that relate **specifically** to Wizard101 and the Pirate101 Valencia quiz. The program uses Python & Selenium to interact with the web page, you can add more QA of different trivia in the Dictionary if you want more options (it can already solve up to 10 quizes by default).
##

>How do I use this?

* 1: Download [Python](https://www.python.org/).
* 2: Download [Selenium](https://pypi.org/project/selenium/).
* 3: Go into the "main.py", and edit the "enter your username here" and "enter your password here" with the credentials needed.
* 4: Run the "main.py" file, it will automotically open another window. It will auto login, click on a compatiable quiz; then press enter when you're on the quiz page.

>Will this automatically do all 10 quizes at once?

**No**. After it solves a quiz, you need to complete the captcha at the end to reciceve the crowns. Then, go to the next to quiz and press enter into the screen prompt.

>How long does the program take to solve each question?


**5 seconds**. The program has to wait for each question to load, then it clicks the correct answer and waits 1 second before going to the next question. It has some intential delays so that it seems more human and does not spam the webpage with requests.

>I got a keyerror when running the program, what should I do?

This error may show up if values in the dictionary are wrong; if Kingsisle updates the questions with newer ones, the dictionary will need to be updated. I will keep updating the dictionary if needed; however you can also update it manually!

>Is this the same thing as the trivia extension that got people in trouble?

**No.** This program was made to seem human and doesn't run via an extension. It also doesn't solve captchas, so this program is slightly less practacle; however, it's more on the DL and will save you a lot of time!

>I have an idea to improve the bot, can I help? (or questions)

**Sure.** I will take suggestions, message me on Discord (**Dizzy#9275**)
