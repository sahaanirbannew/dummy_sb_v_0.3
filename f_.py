import datetime as dt
from urllib import request
import json
import time
from googlesearch import search
import facebook as fb
import g_
from tkinter.filedialog import askdirectory
from plyer import notification
import ui_


def get_folder_name():
    folder = askdirectory(initialdir=g_.root, title='Please select a directory')
    return folder


def fb_page_graph_build(page_id, client_token):
    cfg = {
        "page_id": page_id,
        "access_token": client_token
    }
    graph = fb.GraphAPI(cfg['access_token'], version='3.1')
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
            page_access_token = page['access_token']
    graph = fb.GraphAPI(page_access_token)
    return graph


def fb_user_profile_graph_build(user_id, user_access_token):
    cfg = {
        "user_id": user_id,
        "access_token": user_access_token
    }
    graph = fb.GraphAPI(cfg['access_token'], version='3.1')
    return graph


def fb_page_post_image(username, file, graph, description, count):
    with open(file, "rb") as image:
        graph.put_photo(image=image, message=description)
    notification.notify("Uploaded:", str(file))
    ui_.message_out(username, g_.s, 'Uploaded '+str(file))

    # Update the log
    log = g_.root + g_.folder_db + 'db.csv'
    log_content = open(log, 'a', encoding='utf-8')
    log_content.write(str(dt.datetime.now()) + ',' + "Uploaded" + ',' + str(file) + '\n')
    log_content.close()

    # Update count number.
    count = count + 1
    counter = g_.root + g_.folder_db + 'count.txt'
    counter_content = open(counter, 'w', encoding='utf-8')
    counter_content.write(str(count))
    counter_content.close()

    time.sleep(60)
    return count


def get_count():
    counter = g_.root + g_.folder_db + 'count.txt'
    counter_content = open(counter, 'r')
    count = counter_content.read()
    counter_content.close()
    return count


def reset_count():
    counter = g_.root + g_.folder_db + 'count.txt'
    counter_content = open(counter, 'w', encoding='utf-8')
    counter_content.write("0")
    counter_content.close()


def set_count(val):
    counter = g_.root + g_.folder_db + 'count.txt'
    counter_content = open(counter, 'w', encoding='utf-8')
    counter_content.write(str(val))
    counter_content.close()


def save_description(text, link):
    if link.replace(' ', '') != '':
        link = '\nRead more at: ' + link
    description = text + link
    desc_path = g_.root + g_.folder_db + 'Description.txt'
    desc_content = open(desc_path, 'w', encoding='utf-8')
    desc_content.write(description)
    desc_content.close()
    return description


def save_foldname(text):
    fold_path = g_.root + g_.folder_db + 'folder.txt'
    fold_content = open(fold_path, 'w', encoding='utf-8')
    fold_content.write(text)
    fold_content.close()


def get_foldname():
    fold_path = g_.root + g_.folder_db + 'folder.txt'
    fold_content = open(fold_path, 'r')
    return fold_content.read()


def get_suggested_link(specific_folder_name):
    searchterm = str(specific_folder_name).replace(g_.root, '')
    searchterm = searchterm.replace('/', '')
    query = searchterm + ' + anirbansaha'
    for j in search(query, tld="com", num=1, stop=1, pause=10):
        return j

    return 0


def create_link(specific_folder_name):
    suggested_link = get_suggested_link(specific_folder_name)
    confirm = input("Is this link correct? [Y/N] Link: " + suggested_link + " :")
    if confirm in g_.yes:
        link = suggested_link
    else:
        link = input("Please enter the link: ").replace('\n', '')

    if link != '':
        analytics_param = '?utm_campaign=as_automate'
        link = link.replace(' ', '')
        link = link + analytics_param
        #link = shorten_link(link)
    return link


def shorten_link(link):
    bitly_link = 'http://api.bitly.com/v3/shorten?login=o_51r4v9v39b&apiKey=R_7e968b93a19046989b917643a8d60401&longUrl='
    link = bitly_link + link
    response = request.urlopen(link)
    a = json.loads(response.read())
    link = a['data']['url']
    return link
