from selenium_stealth import stealth
from fake_useragent import UserAgent

# This is a class that contains all the functions that are used to make the chrome driver stealthy
class Stealth():
    def __init__(self, driver=None):
        self.stealth_driver = driver
        self.user_agent = UserAgent(browsers=['chrome'])
        self.user_agent_random = UserAgent(browsers=["chrome", "edge", "internet explorer", "firefox", "safari", "opera"])
    def stealth(self):
        # This function makes the chrome driver stealthy
        stealth(self.stealth_driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
        return self.stealth_driver
    def create_useragent(self):
        # This function creates a user agent for the chrome driver
        user_agent = self.user_agent
        return user_agent
    def create_random_useragent(self):
        # This function creates a random user agent for the chrome driver
        user_agent = self.user_agent_random
        return user_agent.random