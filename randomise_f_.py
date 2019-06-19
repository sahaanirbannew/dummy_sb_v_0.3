# This page is a support to sequence.py


import g_
import f_
import random
import glob
from pandas import DataFrame


def build_folder_record():
    confirm = 'Y'
    list_names = []
    file_paths = []
    folder_no = 0

    while confirm == 'Y':
        specific_folder_name = f_.get_folder_name() + '/'
        if specific_folder_name != '/':
            link = f_.create_link(specific_folder_name)
            #short_link = f_.shorten_link(link)
            short_link = 'bit.ly/link'

            file_path = glob.glob(specific_folder_name + "*.jpg") + glob.glob(specific_folder_name + "*.png")
            num_of_files = len(file_path)
            g_.total_num_of_files = g_.total_num_of_files + num_of_files

            list_names.append(specific_folder_name)
            file_paths.append(file_path)
            folder_no = folder_no + 1
            to_folder_rec('\n'+str(folder_no), str(specific_folder_name), link, short_link)
            confirm = input("Add another folder? [Y/N] : ")
            if confirm in g_.yes:
                confirm = 'Y'
        else:
            return 'User cancelled it.'

    return 'proceed'


def to_folder_rec(num, folder_name, link, short_link):
    db_path = g_.root + g_.folder_db + 'folder_rec.csv'
    db_content = open(db_path, 'a', encoding='utf-8')
    db_content.write(str(num)+','+folder_name+','+link+','+short_link)
    db_content.close()


def generate_random_number(max_number):
    number = random.randint(1, max_number)
    if number in g_.chosen_nos:
        number = generate_random_number(max_number)
    g_.chosen_nos.append(number)
    return number


def generate_schedule_draft_1():
    data = {'no': [],
            'folder_no': [],
            'file_path': [],
            }
    folder_table = DataFrame(data, columns=['no', 'folder_no', 'file_path'])

    db_path = g_.root + g_.folder_db + 'folder_rec.csv'
    db_content = open(db_path, 'r')
    db_line = db_content.readline()

    while db_line != '':
        db_elements = db_line.split(',')

        # Assign values
        folder_no = db_elements[0]
        folder_path = db_elements[1]

        # Find files in folder
        file_path = glob.glob(folder_path + "*.jpg") + glob.glob(folder_path + "*.png")
        num_of_files = len(file_path)
        count = 0
        while count < num_of_files:
            random_number = generate_random_number(10000)
            print("Entering the second while loop." + str(random_number) + " | Count: " + str(count))
            new_line = {'no': [random_number],
                        'folder_no': [folder_no],
                        'file_path': [file_path[count]],
                        }
            new_table = DataFrame(new_line, columns=['no', 'folder_no', 'file_path'])
            folder_table = folder_table.append(new_table, ignore_index=True)
            count = count + 1
        db_line = db_content.readline()

    folder_table = folder_table.sort_values('no', ascending=False)
    folder_table.to_csv(g_.root + g_.folder_db + '/schedule.csv')

