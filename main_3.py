########################################################################################################################
# Improvements on previous version main_1.py
# What version 2.000 did:
#   Takes folder names as input.
#   Posts photographs from the folders in randomised order,
#   finds relevant blog link, shortens links, creates description.
#   Postings happen at predefined times.
# Developer: Anirban Saha.
########################################################################################################################
# Version   Status  Date        Comments
# 2.001     Draft   06.06.2019  Creates the randomised list of photograps from multiple Dropbox folders.
# 2.002     Draft   09.06.2019  Uploads one image at a time to Facebook from the randomised list.
########################################################################################################################

import func_sequence
import g_
import main_bg
import ui_


def main(user, text):
    if text.strip() == 'add_folder':
        proceed = func_sequence.add_folder(user)
        if proceed == 1:
            ui_.message_out(user, g_.s, 'Folder is added successfully.')
        confirm = input("Add another folder?").strip()
        if confirm in g_.yes:
            main(user, 'add_folder')
    elif text == 'sign_up':
        proceed = func_sequence.add_user()
        if proceed != 0:
            ui_.message_out(proceed, g_.s, 'User created.')
    elif text == 'run':
        main_bg.run_service_1(user)
    elif text == 'activate_service_1':
        func_sequence.activate_service(user, 1)
        ui_.message_out(user, g_.s, user)
    else:
        ui_.message_out('', g_.e, text+' is not a recognised command.')


if __name__ == '__main__':
    username = func_sequence.signin()
    if username != 'error':
        ok_continue = 1
        while ok_continue == 1:
            selection = input("Input the following options:\n"
                              "'add_folder' to add folder\n")
            main(username, selection)
            ok_continue = input("Would you want to continue? ")
            if ok_continue in g_.yes:
                ok_continue = 1
    else:
        ui_.message_out('', g_.e, 'Signing in failed.')
        ok_continue = input("Would you like to sign up?")
        if ok_continue in g_.yes:
            main('', 'sign_up')
        else:
            ui_.message_out('', g_.i, 'Bye.')
