########################################################################################
# This file is responsible for the communication.
# I do not know how rest API works. But I believe there should be one point of input
#   and output.
########################################################################################
import func_sequence
from plyer import notification


def message_out(username, message_type, message):
    if username != '':
        # Also put it in the log.
        func_sequence.add_to_log(username, message_type, message)

    # Send it to user interface.
    print(message_type + ': ' + message)
