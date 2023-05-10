import os
import undetected_chromedriver as uc
from threading import Barrier, Thread
import time as t
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
import shutil
import pathlib
from stealth import Stealth
from fake_useragent import UserAgent

class Threadium():
    """A Python module that makes implementing threads with selenium chrome easier."""
    def __init__(self, threads=0):
        self.user_accounts = {}
        self.threads = threads
        self.user_agent = UserAgent().chrome
        self.script_directory = pathlib.Path().absolute()
        self.chrome_options = Options()
        self.random = 'random'
        self.chrome_driver_path = os.path.join('chromedriver.exe')
    def add_user_accounts(self):
        """Gets all user accounts"""
        # creates a dictionary of all user accounts
        with open(os.path.join('text_files', 'accounts.txt'), 'r') as accounts:
            for i in accounts.readlines():
                self.user_accounts[i.split(' ')[0]] = i.split(' ')[1]
    def create_user_data_dir(self, funnel):
        """Creates a chrome directory
        
        funnel -> Str (path to chrome user data directory)
        """
        # creates a chrome directory for each user account (used for creating chrome profiles)
        try:
            # Note: the following line of code is for creating a chrome profile for each user account
            self.chrome_options.add_argument(f"user-data-dir={self.script_directory}\\{funnel[0]}")
        except Exception as e:
            raise Exception(f"Failure! The following error has occured while attempting to make a chrome profile (most likely due to improper funnel path): {e}")
    def create_profile_dir(self, funnel=None):
        """Creates a chrome profile

        funnel -> Str (name of chrome profile)
        """
        # creates a chrome profile for each user account (used for creating chrome profiles) 
        try:
            self.chrome_options.add_argument(f"profile-directory={funnel[1]}")
        except Exception as e:
            raise Exception(f"Failure! The following error has occured while attempting to make a chrome profile (most likely due to improper funnel path): {e}")
    def patch_profile_dirs(self, src, dir):
        """Replaces a dir of chrome profiles with a src profile

        """
        self.add_user_accounts()
        # NOTE: use this in a setup file; only need to run once per account (used for creating chrome profiles)
        try:
            for key in self.user_accounts.keys(): #used to copy over profile #NOTE: use this in a setup file; only need to run once per account
                print(f"Patching the user {key}'s chrome profile...")
                shutil.rmtree(os.path.join(f"user-data-dir\\{key}-dir", f'{key}-user-data'))
                shutil.copytree("chrome_profile_data", os.path.join(f'user-data-dir\\{key}-dir', f'{key}-user-data'))
                print(f"{key}'s chrome profile was successfully patched!")
                print(f"Progress:{round((len(self.user_accounts)/len(self.user_accounts))*100, 0)}%")
        except Exception as e:
            raise Exception(f"Failure! The following error has occured while attempting to patch the chrome profiles: {e}")
    def set_user_agent(self, user_agent=None):
        """Sets the user agent"""
        # sets the user agent for the chrome webdriver
        if user_agent is not None and user_agent != self.random:
            Stealth().create_useragent()
        # sets the user agent to a random user agent for the chrome webdriver
        elif user_agent is not None and user_agent == self.random:
            Stealth().create_random_useragent()
    def start_all(self, args, stealth=False, profile_dir=None, user_agent=None, single_target=None):
        """Starts all the Chrome webdriver threads."""
        self.chrome_options.add_argument("--window-size=1800,1800")
        if single_target is not None: #for one function
            for _ in range(self.threads):
                if profile_dir is not None: #creates chrome profiles
                    self.create_user_data_dir(funnel=profile_dir)
                    self.create_profile_dir(funnel=profile_dir)
                th = Thread(target=single_target, args=args+(uc.Chrome(executable_path=self.chrome_driver_path, options=self.chrome_options),))
                th.start()
                th.join()




