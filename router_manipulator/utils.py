import logging

import psutil
from playsound import playsound
from plyer import notification
import random
import string


class Util:


    @staticmethod
    def log_to_file(message):
        logging.basicConfig(filename='error_log.log',
                            level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        logging.info(message)

    @staticmethod
    def play_sound(sound_path):
        playsound(sound_path)

    @staticmethod
    def terminate_process(process_names_list):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in process_names_list:
                    proc.terminate()
                    print(f"Terminated {proc.info['name']} with PID {proc.info['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print('Process termination done.')

    @staticmethod
    def has_numbers(input_string):
        return any(char.isdigit() for char in input_string)

    @staticmethod
    def windows_log(message, log_duration):
        message = message[:256]  # Truncate the message to 256 characters

        print(f"\n\n\n\n {message} \n\n\n\n")
        notification.notify(
            title='Router Manipulator',
            message=message,
            timeout=log_duration

        )



    @staticmethod
    def generate_random_text(length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))



