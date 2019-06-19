import g_
import datetime as dt
import dropbox
import f_
import os
import pandas as pd
import ui_
import summarise
import time


def is_service_active(service_name, username):
    file_path = g_.root + g_.folder_db + 'user-services.csv'
    try:
        service_details = open(file_path, 'r', encoding='utf-8')
        # service_list is a table for all users and all services.
        service_list = pd.read_csv(file_path)
        service_details.close()
        # service_list is a table for all users and all services.
        user_service = service_list.loc[(service_list['username'] == username) &
                                        (service_list['service_name'] == service_name)]

        # This should ideally be one row of data
        is_active = str(user_service.iloc[0]['status']).strip()
        if is_active == 'active':
            return 'active'
        else:
            return 'inactive'
    except:
        return 'failed'


def get_config_data(username, service, parameter):
    print("Getting Config Data for " + service + '/' + parameter)
    try:
        file_path = g_.root + g_.folder_db + username + '_config.csv'
        # service_list is a table for all users and all services.
        user_config_data = pd.read_csv(file_path)
        user_row = user_config_data.loc[
            (user_config_data['service_name'] == service) & (user_config_data['parameter'] == parameter)]
        value = str(user_row.loc[0, 'value']).strip()
        return value
    except:
        return 'failed'


def find_next_photo(username):
    file_path = g_.root + g_.folder_db + username + '_sequence.csv'
    data = pd.read_csv(file_path)
    rows = data.loc[data['uploaded'] == 'not-done']
    if rows.empty:
        ui_.message_out(username, g_.e, "No more photographs to share.")
        time.sleep(15)
        return ''
    else:
        folder_no = rows.iloc[0]['folder_no']
        photo_path = rows.iloc[0]['file_path']
        return [folder_no, photo_path]


def find_links(username, folder_no):
    # Find the folder specific details: blog post and shortened url.
    file_path = g_.root + g_.folder_db + username + '_folder_details.csv'
    data = pd.read_csv(file_path)
    rows = data.loc[data['num'] == folder_no]

    print(rows)

    # Find the blog post link and the shortened url .
    blogpost_link = rows.iloc[0]['blogpost_link']
    shortened_link = str(rows.iloc[0]['shortened_link']).strip()
    print(blogpost_link)
    print(shortened_link)


    return [blogpost_link, shortened_link]


def mark_the_file_done(username, photo_path):
    file_path = g_.root + g_.folder_db + username + '_sequence.csv'
    data = pd.read_csv(file_path)
    data.loc[data['file_path'] == photo_path, 'uploaded'] = 'done'
    data.to_csv(file_path, index=False)
    return 1


def is_photo_available(username, photo_path):

    # Find the Dropbox access code.
    dropbox_access_code = get_config_data(username, 'dropbox', 'access_token')
    # Connect to Dropbox to fetch the image.
    dbx = dropbox.Dropbox(dropbox_access_code)
    try:
        dbx.files_download_to_file(g_.root + 'temp_', photo_path)
    except:
        # Mark the file as done.
        mark_the_file_done(username, photo_path)

        # Get another one.
        folder_und_path = find_next_photo(username)
        if folder_und_path:
            photo_path = folder_und_path[1]
            photo_available = is_photo_available(username, photo_path)
            if photo_available:
                if photo_available[0] == 'works':
                    return folder_und_path
            else:
                return []
        if not folder_und_path:
            return []
    return ['works']


def run_service_1(username):
    # Service 1: Fetch photographs from the schedule and upload on Facebook.

    # Check if service 1 is active for the username.
    is_active = is_service_active('service_1', username)
    if is_active != 'active':
        ui_.message_out(username, g_.e, 'Service is not active.')
        return 0
    elif is_active == 'failed':
        ui_.message_out(username, g_.e, 'Could not connect to user_services database.')
        return 0
    else:
        ui_.message_out(username, g_.s, 'Started the service "Upload to Facebook at regular interval."')
        print(g_.selected_fb_time)
        while is_active == 'active':

            curr_time = str(dt.datetime.now().hour) + ":" + str(dt.datetime.now().minute)
            if curr_time in g_.selected_fb_time:
                is_active = is_service_active('service_1', username)
                if is_active == 'active':
                    print("shob active ache.")
                    # Read from the scheduled csv file: Get folder no. and file path.
                    folder_und_path = find_next_photo(username)
                    print(folder_und_path)
                    if not folder_und_path:
                        print("No photographs to share")
                    if folder_und_path != '':
                        folder_no = folder_und_path[0]
                        photo_path = folder_und_path[1]
                        photo_available = is_photo_available(username, photo_path)
                        if not photo_available:
                            ui_.message_out(username, g_.e, 'No more photographs to share.')
                            folder_no = ''
                            photo_path = ''
                        elif photo_available[0] != 'works':
                            # If the photo is not available, choose the next available one.
                            folder_no = photo_available[0]
                            photo_path = photo_available[1]

                        if folder_no != '':
                            # Find the long link, short link.
                            long_link_und_short_link = find_links(username, folder_no)
                            print(long_link_und_short_link)
                            long_link = long_link_und_short_link[0]
                            short_link = long_link_und_short_link[1]

                            # Fetch a description using the long link.
                            description = summarise.get_summary_description(long_link, 'fb')

                            # Check if the shortened link exist.
                            if short_link != '':
                                description = description + " Check out more at " + short_link

                            # Upload the image with the description.
                            page_graph = f_.fb_page_graph_build(g_.page_id, g_.client_token)
                            try:
                                with open(g_.root + 'temp_', "rb") as image:
                                    page_graph.put_photo(image=image, message=description)
                                ui_.message_out(username, g_.s, 'Uploaded: ' + str(photo_path))
                            except:
                                ui_.message_out(username, g_.e, 'Upload failed: ' + str(photo_path))

                            # Delete the temporary file.
                            os.remove(g_.root + 'temp_')

                            # Mark the file as done.
                            mark_the_file_done(username, photo_path)

                            # Put to sleep for 59 seconds.
                            time.sleep(59)
        return 1
