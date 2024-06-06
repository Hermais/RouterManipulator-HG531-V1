import random
import re
import string
import time

import selenium.common.exceptions
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from win10toast import *


class RouterManipulator:
    default_timeout = 30

    def __init__(self, routerLoginPageUserName, routerLoginPagePassword, routerURL,
                 weAccountNumber, weAccountPassword, weURL, currentQuota, logDuration, laptop_implicit_wait,
                 browser="chrome", command="null",
                 is_logging_printable=False):
        # log() method Essentials
        self.is_logging_printable = is_logging_printable
        self.toaster = ToastNotifier()
        # run() method Essentials
        self.command = command
        self.routerLoginPageUserName = routerLoginPageUserName
        self.routerLoginPagePassword = routerLoginPagePassword
        self.routerURL = routerURL
        self.webdriver_browser = browser
        self.driver = None
        self.logDuration = logDuration
        self.laptop_implicit_wait = laptop_implicit_wait
        # We
        self.currentQuota = currentQuota
        self.weAccountNumber = weAccountNumber
        self.weAccountPassword = weAccountPassword
        self.weURL = weURL

    def run_ui(self):
        try:
            self.validate_input(is_ui=True)
        except Exception as e:
            self.log(f"An Unknown Error Occurred: {e}")
            print(f"An error occurred: {e}\n\nTry Again?(y/n)")
            if input().lower() == 'y':
                self.run_ui()
            else:
                quit(0)

    def run_no_ui_args(self, value_):
        self.command = value_
        self.play_startup_sound('router_manipulator/startup_sound.mp3')

        try:
            self.validate_input(is_ui=False)
        except Exception as e:
            self.log(f"An Unknown Error Occurred: {e}")


    def play_startup_sound(self, sound_path):
        playsound(sound_path)





    def validate_input(self, is_ui):
        while True:
            if is_ui:
                print(
                    "Hello! This is a simple program that changes the rate of the Wifi, and allows for a reboot for the router.\n")
                self.command = input(
                    f"Please enter the desired speed being: 1, 2, 5.5, 6, 9, 11 or Type Full, to switch to full speed.\n "
                    "Also type res to restart the router. Type quickmath or q to create a temporary Wifi network.\n "
                    "Default password is 123456789rtx!, and default SSID name vessel (slot4).\n"
                    "To disable the temporary SSID, Enter dis.\n"
                    "To Create a costume temporary SSID name, Enter c.\n"
                    "To Create a random temporary SSID name, Enter r.\n"
                    "To check the speed current speed setting Enter chk.\n"
                    "To check the remaining quota press qchk.\n"
                    f"Finally choose your preferred browser, current one is {self.webdriver_browser.capitalize()}. (chrome, firefox or edge)\n")
            if self.command.lower() == 'full':
                self.command = 101
                self.speed_manip(self.command)
                break
            elif self.command.lower() == 'res':
                self.restart_fun()
                break
            elif self.command.lower() == 'quickmath' or self.command.lower() == 'q':
                self.quick_math('vessel')
                break
            elif self.command.lower() == 'dis':
                self.ssid_dis()
                break
            elif self.command.lower() == 'c':
                print("What is the SSID name?\n"
                      "SSID password is the same 123456789rtx!\n")
                ssid_name = input()
                self.quick_math(ssid_name)
                break
            elif self.command.lower() == 'r':
                ssid_name = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
                    string.ascii_letters) * 2 + random.choice(string.ascii_letters) + random.choice(
                    string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
                    string.ascii_letters) * 3
                self.quick_math(ssid_name)
                break
            elif self.command.lower() == 'chk':
                self.chk_speed()
                break
            elif self.command.lower() == 'qchk':
                self.quota_check()
                break
            elif self.command.lower() == 'firefox':
                self.webdriver_browser = self.command.lower()
                continue
            elif self.command.lower() == 'edge':
                self.webdriver_browser = self.command.lower()
                continue
            elif self.command.lower() == 'chrome':
                self.webdriver_browser = self.command.lower()
                continue
            elif self.command.lower() == "quit" or self.command.lower() == "exit":
                quit(0)
            else:
                try:
                    self.speed_manip(int(self.command))
                    break
                except ValueError:
                    try:
                        self.speed_manip(float(self.command))
                        break
                    except ValueError:
                        print("\n\nINVALID INPUT\n\n")
                        continue



    def speed_manip(self, x):
        self.init_wlan_settings()
        # Custom method that uses explicit wait for a web element.
        self.wait_for_element(By.NAME, "wlgnMode")

        if self.command == 101:
            selection = Select(self.driver.find_element(by=By.NAME, value="wlgnMode"))
            selection.select_by_value('b/g/n')
            self.driver.find_element(by=By.NAME, value="btnApply").click()

            # Exclusive for Laptop (Wi-Fi)
            time.sleep(self.laptop_implicit_wait)

            self.driver.switch_to.default_content()
            self.driver.implicitly_wait(1)
            self.driver.switch_to.frame('logofrm')
            self.driver.find_element(by=By.ID, value="setlogin").click()

            self.wait_for_element(By.ID, "btnCancel")
            self.driver.quit()
            self.log(message="Wi-Fi speed is successfully set to full speed.")
        else:
            selection = Select(self.driver.find_element(by=By.NAME, value="wlgnMode"))
            selection.select_by_value('b/g')
            self.driver.implicitly_wait(1)
            selection = Select(self.driver.find_element(by=By.NAME, value="wlRate"))
            self.driver.implicitly_wait(1)
            selection.select_by_value(str(x))
            self.driver.find_element(by=By.NAME, value="btnApply").click()

            # Exclusive for Laptop (Wi-Fi)
            time.sleep(self.laptop_implicit_wait)

            self.driver.switch_to.default_content()
            self.driver.implicitly_wait(1)
            self.driver.switch_to.frame('logofrm')
            self.driver.find_element(by=By.ID, value="setlogin").click()

            self.wait_for_element(By.ID, "btnCancel")
            self.driver.quit()

            self.log(message=f"Wi-Fi speed is successfully set to {x} Mbps.")

    def restart_fun(self):
        self.specify_browser()

        self.fill_login_page()

        self.driver.implicitly_wait(1)
        self.driver.switch_to.frame('listfrm')
        self.driver.implicitly_wait(1)
        self.driver.find_element(by=By.ID, value="link_Admin_3").click()
        self.driver.find_element(by=By.ID, value="link_Admin_3_1").click()
        self.driver.switch_to.default_content()
        self.driver.implicitly_wait(1)
        self.driver.switch_to.frame("contentfrm")
        self.driver.implicitly_wait(1)
        self.driver.find_element(by=By.NAME, value="btnReboot").click()
        self.driver.switch_to.alert.accept()

        # We can add a wait here to properly log out of the router page, but that's totally not required as the router
        # will automatically redirect to main login page after restart

        time.sleep(1)
        self.driver.quit()

        self.log(message="The router is successfully restarted.")

        """
        self.driver.switch_to.default_content()
        self.driver.implicitly_wait(1)
        self.driver.switch_to.frame('logofrm')
        self.driver.find_element(by=By.ID, value="setlogin").click()
        try:
            WebDriverWait(self.driver, self.default_timeout).until(
                EC.presence_of_element_located((By.ID, "btnCancel"))
            )
        finally:
            self.driver.quit()
        """

    def quick_math(self, y):
        self.init_wlan_settings()

        self.wait_for_element(by=By.NAME, value="wlSsidIdx")

        selection = Select(self.driver.find_element(by=By.NAME, value="wlSsidIdx"))
        self.driver.implicitly_wait(1)
        selection.select_by_value('3')
        self.driver.implicitly_wait(1)
        self.driver.find_element(by=By.NAME, value="wlSsid").clear()
        self.driver.find_element(by=By.NAME, value="wlSsid").send_keys(y)
        check_box = self.driver.find_element(by=By.NAME, value="enableSsid").is_selected()
        if not check_box:
            self.driver.find_element(by=By.NAME, value="enableSsid").click()

        selection = Select(self.driver.find_element(by=By.NAME, value="wlnAuthMode"))
        self.driver.implicitly_wait(1)
        selection.select_by_value('WPAand11i')
        self.driver.find_element(by=By.NAME, value="wlWpaPsk").clear()
        self.driver.find_element(by=By.NAME, value="wlWpaPsk").send_keys('123456789rtx!')
        self.driver.find_element(by=By.NAME, value="btnApply").click()

        # Alternative to implicit wait
        time.sleep(self.laptop_implicit_wait)

        self.driver.switch_to.default_content()
        self.driver.implicitly_wait(1)
        self.driver.switch_to.frame('logofrm')
        self.driver.find_element(by=By.ID, value="setlogin").click()

        self.wait_for_element(By.ID, "btnCancel")
        self.driver.quit()

        self.log(message=f"Temporary Wi-Fi network is successfully created with SSID: {y}.")

    def ssid_dis(self):
        self.init_wlan_settings()

        self.wait_for_element(by=By.NAME, value="wlSsidIdx")

        selection = Select(self.driver.find_element(by=By.NAME, value="wlSsidIdx"))
        self.driver.implicitly_wait(1)
        selection.select_by_value('3')
        self.driver.implicitly_wait(1)

        check_box = self.driver.find_element(by=By.NAME, value="enableSsid").is_selected()
        if check_box:
            self.driver.find_element(by=By.NAME, value="enableSsid").click()
            self.driver.find_element(by=By.NAME, value="btnApply").click()

            time.sleep(self.laptop_implicit_wait)

            self.driver.switch_to.default_content()
            self.driver.implicitly_wait(1)
            self.driver.switch_to.frame('logofrm')
            self.driver.find_element(by=By.ID, value="setlogin").click()

            self.wait_for_element(By.ID, "btnCancel")
            self.driver.quit()

            self.log(message="Temporary Wi-Fi network is successfully disabled.")

        else:
            time.sleep(2)
            self.driver.switch_to.default_content()
            self.driver.implicitly_wait(1)
            self.driver.switch_to.frame('logofrm')
            self.driver.find_element(by=By.ID, value="setlogin").click()

            self.wait_for_element(By.ID, "btnCancel")
            self.driver.quit()

            self.log(message="Temporary Wi-Fi network is already disabled.")

    def chk_speed(self):
        self.init_wlan_settings()

        self.wait_for_element(by=By.NAME, value="wlgnMode")

        selection = Select(self.driver.find_element(by=By.NAME, value="wlgnMode"))
        selected_option = selection.first_selected_option
        if selected_option.text == "802.11b/g":
            selection = Select(self.driver.find_element(by=By.NAME, value="wlRate"))
            selected_option = selection.first_selected_option

            self.log("The Wi-Fi speed is set to " + selected_option.text + ".")

            self.driver.switch_to.default_content()
            self.driver.implicitly_wait(1)
            self.driver.switch_to.frame('logofrm')
            self.driver.find_element(by=By.ID, value="setlogin").click()

            self.wait_for_element(By.ID, "btnCancel")
            self.driver.quit()

            # Not sure why this is here.
            time.sleep(4)
        else:

            self.log("The Wi-Fi speed is maxed.")

            # Not sure why this is here.
            time.sleep(4)
            self.driver.switch_to.default_content()
            self.driver.implicitly_wait(1)
            self.driver.switch_to.frame('logofrm')
            self.driver.find_element(by=By.ID, value="setlogin").click()

            self.wait_for_element(By.ID, "btnCancel")
            self.driver.quit()

            # Not sure why this is here.
            time.sleep(4)

    def log(self, message):
        if self.is_logging_printable:
            print(f"\n\n\n\n {message} \n\n\n\n")
        else:
            self.toaster.show_toast("Router Manipulator", message, icon_path='', duration=self.logDuration)

    def quota_check(self):
        global used_gb_text, renew_date_remaining_days_text
        self.specify_browser()

        self.driver.get(self.weURL)

        repeat = True
        while repeat:
            try:
                WebDriverWait(self.driver, self.default_timeout).until(
                    EC.presence_of_element_located((By.ID, "login_loginid_input_01"))
                )
            except selenium.common.exceptions.NoSuchElementException:
                self.driver.refresh()
                continue
            finally:
                repeat = False
                self.driver.find_element(by=By.ID, value="login_loginid_input_01").send_keys(self.weAccountNumber)
                self.driver.find_element(by=By.ID, value="login_password_input_01").send_keys(self.weAccountPassword)
                self.driver.find_element(by=By.XPATH,
                                         value="/html/body/div[1]/section/main/div/div/div/div[2]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div[1]/span[1]/input").click()
                self.driver.find_element(by=By.XPATH,
                                         value="/html/body/div[1]/section/main/div/div/div/div[2]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div").click()
                self.driver.find_element(by=By.XPATH,
                                         value="/html/body/div[1]/section/main/div/div/div/div[2]/div/div[3]/button").click()

        repeat = True
        while repeat:
            try:
                WebDriverWait(self.driver, self.default_timeout).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "/html/body/div[1]/section/main/div/div/div[2]/div[3]/div/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]"))
                )
            except selenium.common.exceptions.NoSuchElementException:
                continue
            finally:
                time.sleep(2)  # REQUIRED SLEEP DO NOT REMOVE IT
                used_gb_text = self.driver.find_element(by=By.XPATH,
                                                        value="/html/body/div[1]/section/main/div/div/div[2]/div[3]/div/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]").text
                if not self.has_numbers(used_gb_text):
                    continue
                print(f"LOG:: used_gb_text:{used_gb_text}")
                self.driver.find_element(By.XPATH,
                                         "/html/body/div[1]/section/main/div/div/div[2]/div[1]/div/div/div/div/div[3]/div/div/div/div[3]/button").click()
                repeat = False

        repeat = True
        while repeat:
            try:
                self.driver.implicitly_wait(1)
                WebDriverWait(self.driver, self.default_timeout).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "/html/body/div[1]/section/main/div/div/div[3]/div[2]/div/div/div/div/div[4]/div/span"))
                )
            except selenium.common.exceptions.NoSuchElementException:
                self.driver.refresh()
                continue
            finally:
                time.sleep(2)  # REQUIRED SLEEP DO NOT REMOVE IT
                renew_date_remaining_days_text = self.driver.find_element(By.XPATH,
                                                                          "/html/body/div[1]/section/main/div/div/div[3]/div[2]/div/div/div/div/div[4]/div/span").text

                if self.has_numbers(renew_date_remaining_days_text):
                    repeat = False
                print(f"LOG:: renew_date_remaining_days_text: {renew_date_remaining_days_text}")

        pattern = r"[-+]?\d*\.?\d+"  # This pattern matches the float number
        matches = re.findall(pattern, used_gb_text)
        used_gb = float(matches[0])
        remaining_gb = self.currentQuota - used_gb

        self.log(f"{used_gb_text} out of 200GB.\n{remaining_gb: 0.2f} Remaining!\n{renew_date_remaining_days_text}")

        pattern = r', (\d+)'
        remaining_days = int(re.search(pattern, renew_date_remaining_days_text).group(1))

        self.evaluate(used_gb, remaining_days)

        self.driver.quit()

    def has_numbers(self, input_string):
        return any(char.isdigit() for char in input_string)

    def evaluate(self, used_GB, remaining_days):
        std_usage_rate_GB = self.currentQuota / 30.0
        usage_rate_GB = used_GB / (30 - remaining_days)

        if usage_rate_GB - std_usage_rate_GB >= 0.07 * std_usage_rate_GB:
            self.log(
                f"Usage is high⚠️, try lowering it.\n({usage_rate_GB: 0.2f} GB/Day to std {std_usage_rate_GB: 0.2f} GB/Day)")
        else:
            self.log(f"Usage is reasonable👍.\n({usage_rate_GB: 0.2f} GB/Day to std {std_usage_rate_GB: 0.2f} GB/Day)")

    def specify_browser(self):
        if self.webdriver_browser == "firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_service = Service(GeckoDriverManager().install())
            self.set_webdriver_browser(webdriver.Firefox, firefox_options, firefox_service)

        elif self.webdriver_browser == "edge":
            edge_options = webdriver.EdgeOptions()
            edge_service = Service(EdgeChromiumDriverManager().install())
            self.set_webdriver_browser(webdriver.Edge, edge_options, edge_service)

        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_service = Service(ChromeDriverManager().install())
            self.set_webdriver_browser(webdriver.Chrome, chrome_options, chrome_service)

    def set_webdriver_browser(self, webdriver_instance, options, service):
        try:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

            self.driver = webdriver_instance(options=options, service=service)
        except selenium.common.exceptions.SessionNotCreatedException as e:
            print("*" * 100 + "\nFAILED:\n" + "*" * 100 + f"\n")
            print("\n\nTry switching to a different browser.\n\n")
            self.run_ui()

    def fill_login_page(self):
        self.driver.get(self.routerURL)
        self.driver.find_element(by=By.NAME, value="Username").send_keys(self.routerLoginPageUserName)

        self.driver.find_element(by=By.NAME, value="Password").send_keys(self.routerLoginPagePassword)

        self.driver.find_element(by=By.ID, value="btnLogin").click()

    def wait_for_element(self, by, value, timeout=default_timeout):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"Element not found!")
            return None

    def init_wlan_settings(self):
        self.specify_browser()

        self.fill_login_page()

        self.driver.implicitly_wait(1)
        self.wait_for_element(By.ID, 'listfrm')
        self.driver.switch_to.frame('listfrm')
        self.driver.implicitly_wait(1)

        self.wait_for_element(By.ID, "link_Admin_1").click()

        self.driver.find_element(by=By.ID, value="link_Admin_1_2").click()
        self.driver.implicitly_wait(1)
        self.driver.switch_to.default_content()
        self.driver.implicitly_wait(1)
        self.wait_for_element(By.ID, 'contentfrm')
        self.driver.switch_to.frame('contentfrm')
        self.driver.implicitly_wait(1)
