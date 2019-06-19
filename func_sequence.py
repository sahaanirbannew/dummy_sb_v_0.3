import random
import dropbox
import pandas as pd
from pandas import DataFrame
import g_
import f_
import datetime as dt
import main_3
import ui_



def get_latest_folder_no(username):
    db_path = g_.root + g_.folder_db + username + '_folder_details.csv'
    data = pd.read_csv(db_path)
    try:
        count = data['num'].count()
        return count
    except:
        return 0


def to_folder_rec(username, num, folder_name, link, short_link):
    db_path = g_.root + g_.folder_db + username + '_folder_details.csv'
    line_entry = '\n' + str(num) + ',' + folder_name + ',' + link + ',' + short_link
    db_content = open(db_path, 'a', encoding='utf-8')
    db_content.write(line_entry)
    db_content.close()


def generate_random_number(max_number):
    number = random.randint(1, max_number)
    if number in g_.chosen_nos:
        number = generate_random_number(max_number)
    g_.chosen_nos.append(number)
    return number


def refresh_sequence(username):
    try:
        file_path = g_.root + g_.folder_db + username + '_sequence.csv'
        data = pd.read_csv(file_path)
        done = data[data['uploaded'] == 'done'].index
        data.drop(done, inplace=True)
        data = data.sort_values('no', ascending=True)
        data.to_csv(file_path, index=False)
        return 1
    except:
        return 0


def sequence_files(username, num, folder_name):
    # Dropbox details of Anirban.
    app_key = '996l11cz45kgdb2'
    app_secret = 'wbr5jnd20e4n8jx'
    access_token = 'QUD-vyfoLlUAAAAAAAEjuKWK5KQg6WeOOGI12ZuzLN9dMBJbmm7ZkzLwCG5DLQc2'

    dbx = dropbox.Dropbox(access_token)
    file_names = []
    folder_name = '/' + folder_name + '/'

    schedule_new_path = g_.root + g_.folder_db + username + '_sequence.csv'

    data = {'no': [],
            'uploaded': [],
            'folder_no': [],
            'file_path': [],
            }
    folder_table = DataFrame(data, columns=['no', 'uploaded', 'folder_no', 'file_path'])

    for entry in dbx.files_list_folder(folder_name).entries:
        random_number = generate_random_number(10000)
        new_line = {'no': [random_number],
                    'uploaded': ["not-done"],
                    'folder_no': [num],
                    'file_path': [entry.path_display],
                    }
        new_table = DataFrame(new_line, columns=['no', 'uploaded', 'folder_no', 'file_path'])
        folder_table = folder_table.append(new_table, ignore_index=True)

    if num == 1:
        folder_table.to_csv(schedule_new_path, header=True, index=False)
    else:
        with open(schedule_new_path, 'a') as f:
            folder_table.to_csv(f, header=False, index=False)

    # Delete from the table entries which have been uploaded already.
    # Sorts it back to order.
    proceed = refresh_sequence(username)
    if proceed == 1:
        return 1
    else:
        return 0


def check_folder_exists(folder_name):
    # Connect to Dropbox.

    # Fetch a list of folders.

    # Check if folder_name is one of the folder names.

    # Find the closest name in the Dropbox.
    # if you find that, Confirm that.
    # else: Ask for a new valid folder name.

    return 1


def add_folder(username):
    # Authorise Dropbox. [Out of Scope of this program. We work with predefined user; Me.]
    folder_name = input("Enter folder name: ").strip()

    if folder_name != '':
        # Check if the folder exists.
        folder_exists = check_folder_exists(folder_name)

        # Finds the most relevant link for the folder.
        link = f_.create_link(folder_name)  # Finding the link.
        # Shortens the link using Bit.ly.
        short_link = f_.shorten_link(link)  # Shortened link.

        # Creates the folder number:
        try:
            num = get_latest_folder_no(username)
            num = num + 1
        except:
            num = 1

        # Enters the folder, link, shortened link to the database.
        to_folder_rec(username, num, folder_name, link, short_link)

        # Randomises the files.
        proceed = sequence_files(username, num, folder_name)

        if proceed == 1:
            ui_.message_out(username, g_.s, 'Randomised List made.')
            return 1
        if proceed == 0:
            ui_.message_out(username, g_.e, 'Randomised List failed.')
            return 0

    else:
        ui_.message_out(username, g_.e, 'No folder name entered.')
        return 0


def validate_username(username, password, email):
    if username == ''or password == '' or email == '':
        return -1

    file_path = g_.root + g_.folder_db + 'users.csv'
    user_details = open(file_path, 'r', encoding='utf-8')
    user_list = pd.read_csv(file_path)
    user_details.close()
    # So user_list is a table with all usernames and passwords.

    # check email format:

    # check if email exists before:

    return 1


def create_user_in_table(username, password, email):
    try:
        file_path = g_.root + g_.folder_db + 'users.csv'
        user_details = open(file_path, 'a', encoding='utf-8')
        user_details.write('\n'+username+','+password+','+email)
        user_details.close()
        ui_.message_out(username, g_.s, 'User added.')
    except:
        return 0
    return 1


def creat_user_log_file(username):
    file_path = g_.root + g_.folder_db + username + '_log.csv'
    user_log = open(file_path, 'w', encoding='utf-8')
    user_log.write('Time,Type,Text')
    user_log.close()
    pass


def create_user_config_file(username):
    file_path = g_.root + g_.folder_db + username + '_config.csv'
    user_log = open(file_path, 'w', encoding='utf-8')
    user_log.write('service_name,parameter,value')
    user_log.close()
    pass

#####################################################
#
#####################################################
def add_user():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    email = input("Enter email address: ").strip()

    # Validate username.
    validated = validate_username(username, password, email)
    if validated == 1:
        ui_.message_out(username, g_.s, 'No Duplicate entries exist.')
        proceed = create_user_in_table(username, password, email)
        ui_.message_out(username, g_.s, 'User created confirmed.')
        if proceed != 1:
            return 0
    elif validated == -1:
        ui_.message_out('', g_.e, 'Username or Password or email is blank.')
        return 0
    elif validated == -2:
        ui_.message_out('', g_.e, 'Email address already registered.')
        return 0
    else:
        ui_.message_out('', g_.e, 'Username exists.')
        add_user()

    creat_user_log_file(username)
    create_user_config_file(username)
    main_3.main(username, 'activate_service_1')
    main_3.main(username, 'add_folder')
    main_3.main(username, 'run')
    return username


def check_signin(username, password):
    file_path = g_.root + g_.folder_db + 'users.csv'
    # user_details = open(file_path, 'r', encoding='utf-8')
    user_list = pd.read_csv(file_path)
    # user_details.close()

    # So user_list is a table with all usernames and passwords.
    row = user_list.loc[(user_list['username'] == username)]
    if row.empty:
        return 0
    else:
        try:
            if str(row.iloc[0]['password']).strip() != password:
                ui_.message_out('', g_.e, 'Password did not match')
                return 0
        except:
            return 0

    # username and password match.
    ui_.message_out(username, g_.s, 'User signed in.')
    return 1


def signin():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    perfect = check_signin(username, password)
    if perfect == 1:
        return username
    else:
        return 'error'


# Creates the files required for service_1
# Input: username
# Output: Files.
def activate_service_1(username):
    file_path = g_.root + g_.folder_db + username + '_folder_details.csv'
    file = open(file_path, 'w', encoding='utf-8')
    content_to_write = 'num,folder_name,blogpost_link,shortened_link'
    file.write(content_to_write)
    file.close()

    file_path = g_.root + g_.folder_db + username + '_sequence.csv'
    file = open(file_path, 'w', encoding='utf-8')
    content_to_write = 'no,uploaded,folder_no,file_path'
    file.write(content_to_write)
    file.close()

    return 1


def activate_service(username, num):
    file_path = g_.root + g_.folder_db + 'user-services.csv'
    file = open(file_path, 'a', encoding='utf-8')
    content_to_write = '\n'+username+','+'service_'+str(num)+','+'active'
    file.write(content_to_write)
    if num == 1:
        activate_service_1(username)
    return 1


def add_to_log(username, message_type, message):
    file_path = g_.root + g_.folder_db + username + '_log.csv'
    user_log = open(file_path, 'a', encoding='utf-8')
    curr_time = str(dt.datetime.now())
    user_log.write('\n'+curr_time+','+message_type+','+message)
    user_log.close()
    return 1
