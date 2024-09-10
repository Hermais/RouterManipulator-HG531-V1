import re
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from secret import MySecrets
from .utils import Util


class HG531V1RouterManipulator:
    default_timeout = 30

    def __init__(self, router_login_page_user_name, router_login_page_password, router_url,
                 we_account_number, we_account_password, we_url, current_quota, log_duration, laptop_implicit_wait,
                 browser="chrome", command="null", processes_to_eliminate=None, default_ssid_password=None,
                 is_logging_printable=False):
        # log() method Essentials
        if default_ssid_password is None:
            default_ssid_password = MySecrets.default_wifi_password
        if processes_to_eliminate is None:
            processes_to_eliminate = ["msedge.exe", "msedgewebview2.exe", "msedgedriver.exe"]
        self.default_temp_password = default_ssid_password
        self.processes_to_eliminate = processes_to_eliminate
        self.is_logging_printable = is_logging_printable

        # run() method Essentials
        self.command = command
        self.router_login_page_user_name = router_login_page_user_name
        self.router_login_page_password = router_login_page_password
        self.routerURL = router_url
        self.webdriver_browser = browser
        self.driver = None
        self.log_duration = log_duration
        self.laptop_implicit_wait = laptop_implicit_wait
        # We
        self.current_quota = current_quota
        self.we_account_number = we_account_number
        self.we_account_password = we_account_password
        self.we_url = we_url

        self.we_elements_xpath = {
            "input_field": "/html/body/div[1]/section/main/div/div/div/div[2]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div[1]/span[1]/input",
            "dropdown_menu": "/html/body/div[1]/section/main/div/div/div/div[2]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div",
            "submit_button": "/html/body/div[1]/section/main/div/div/div/div[2]/div/div[3]/button",
            "used_gb_field": "/html/body/div[1]/section/main/div/div/div[2]/div[3]/div/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]",
            "confirm_button": "/html/body/div[1]/section/main/div/div/div[2]/div[1]/div/div/div/div/div[3]/div/div/div/div[3]/button",
            "renew_date_field": "/html/body/div[1]/section/main/div/div/div[3]/div[2]/div/div/div/div/div[4]/div/span"
        }

    def run_ui(self):
        try:
            # self.terminate_process(self.processes_to_eliminate)
            self.validate_input(is_ui=True)
        except Exception as e:
            Util.windows_log(log_duration=self.log_duration, message=f"An Unknown Error Occurred: {e}")
            print(f"An error occurred: {e}\n\nTry Again?(y/n)")
            if input().lower() == 'y':
                self.run_ui()
            else:
                quit(0)

    def run_args(self, value_):
        self.command = value_
        try:
            Util.play_sound('router_manipulator/startup_sound.mp3')
            # self.terminate_process(self.processes_to_eliminate)
            self.validate_input(is_ui=False)
        except Exception as e:
            Util.log_to_file('router_manipulator/failure_sound.mp3')
            Util.windows_log(log_duration=self.log_duration, message=f"An Unknown Error Occurred: {e}")
            Util.log_to_file(e)

    def validate_input(self, is_ui):
        while True:
            if is_ui:
                print(
                    "Hello! This is a simple program that changes the rate of the Wifi, and allows for a reboot for the router.\n")
                self.command = input(
                    f"Please enter the desired speed being: 1, 2, 5.5, 6, 9, 11 or Type Full, to switch to full speed.\n "
                    "Also type res to restart the router.\n "
                    f"Default password is {self.default_temp_password}.\n"
                    "To disable the temporary SSID, Enter dis.\n"
                    "To Create a costume temporary SSID name, Enter c.\n"
                    "To Create a random temporary SSID name, Enter r.\n"
                    "To check the speed current speed setting Enter chk.\n"
                    "To check the remaining quota press qchk.\n"
                    f"Finally choose your preferred browser, current one is {self.webdriver_browser.capitalize()}. (chrome, firefox or edge)\n")
            if self.command.lower() == 'full':
                self.command = 101
                self.speed_selector(self.command)
                break
            elif self.command.lower() == 'res' or self.command.lower() == 'restart router':
                self.restart_fun()
                break
            elif self.command.lower() == 'dis' or self.command.lower() == 'disable ssid':
                self.ssid_dis(ssid_index=3)
                break
            elif self.command.lower() == 'c' or self.command.lower() == 'create ssid':
                print("What is the SSID name?\n"
                      "SSID password is the same 123456789rtx!\n")
                self.create_ssid(ssid_name=input())
                break
            elif self.command.lower() == 'r' or self.command.lower() == 'random ssid':
                self.create_ssid(ssid_name=Util.generate_random_text(length=12))
                break
            elif self.command.lower() == 'chk' or self.command.lower() == 'check speed':
                self.chk_speed()
                break
            elif self.command.lower() == 'qchk' or self.command.lower() == 'quota check':
                self.internet_quota_check()
                break
            elif self.command.lower() == 'block':
                self.block_device('00:00:00:00:00:00')
                break
            elif self.command.lower() == 'getit':
                self.go_to_basic_settings()
                time.sleep(1000)
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
                    self.speed_selector(int(self.command))
                    break
                except ValueError:
                    try:
                        self.speed_selector(float(self.command))
                        break
                    except ValueError:
                        print("\n\nINVALID INPUT\n\n")
                        continue

    def go_to_we_login_page(self):
        self.specify_browser()

        self.driver.get(self.we_url)

    def fill_login_info_we_internet(self):
        self.wait_for_element(by=By.ID, value="login_loginid_input_01").send_keys(self.we_account_number)
        self.driver.find_element(by=By.ID, value="login_password_input_01").send_keys(self.we_account_password)
        self.driver.find_element(by=By.XPATH, value=self.we_elements_xpath["input_field"]).click()
        self.driver.find_element(by=By.XPATH, value=self.we_elements_xpath["dropdown_menu"]).click()
        self.driver.find_element(by=By.XPATH, value=self.we_elements_xpath["submit_button"]).click()

    def internet_quota_check(self):

        self.go_to_we_login_page()
        self.fill_login_info_we_internet()

        while True:
            used_gb_text = self.wait_for_element(by=By.XPATH,
                                                 value=self.we_elements_xpath["used_gb_field"],
                                                 wait_after=2).text
            if Util.has_numbers(used_gb_text):
                self.driver.find_element(By.XPATH, value=self.we_elements_xpath["confirm_button"]).click()
                break

        while True:
            renew_date_remaining_days_text = self.wait_for_element(by=By.XPATH,
                                                                   value=self.we_elements_xpath["renew_date_field"],
                                                                   wait_after=2).text
            if Util.has_numbers(renew_date_remaining_days_text):
                break

        float_pattern = r"[-+]?\d*\.?\d+"
        matches = re.findall(float_pattern, used_gb_text)
        used_gb = float(matches[0])
        remaining_gb = self.current_quota - used_gb

        Util.windows_log(log_duration=self.log_duration,
                         message=f"{used_gb_text} out of {self.current_quota}GB.\n{remaining_gb: 0.2f} Remaining!\n{renew_date_remaining_days_text}")

        float_pattern = r', (\d+)'
        remaining_days = int(re.search(float_pattern, renew_date_remaining_days_text).group(1))

        self.evaluate_rate_of_usage(used_gb, remaining_days)

        self.driver.quit()

    def submit_basic_wifi_settings(self):
        self.driver.find_element(by=By.NAME, value="btnApply").click()

        # Exclusive for Laptop (Wi-Fi)
        time.sleep(self.laptop_implicit_wait)

    def exit_from_basic_wlan_settings(self):
        self.driver.switch_to.default_content()
        self.driver.implicitly_wait(1)
        self.driver.switch_to.frame('logofrm')
        self.driver.find_element(by=By.ID, value="setlogin").click()

        self.driver.quit()

    def speed_selector(self, speed):
        self.go_to_basic_wlan_settings()

        selection = Select(self.wait_for_element(by=By.NAME, value="wlgnMode"))

        if self.command == 101:
            selection.select_by_value('b/g/n')
            self.submit_basic_wifi_settings()
            self.exit_from_basic_wlan_settings()

        else:
            selection.select_by_value('b/g')
            selection = Select(self.wait_for_element(by=By.NAME, value="wlRate"))
            selection.select_by_value(str(speed))

            self.submit_basic_wifi_settings()
            self.exit_from_basic_wlan_settings()

        Util.windows_log(log_duration=self.log_duration,
                         message=f"Wi-Fi speed is successfully set to {"max" if self.command == 101 else str(speed) + " Mbps"}.")

    def restart_fun(self):
        self.specify_browser()

        self.fill_login_page()

        self.switch_to_left_side_frame()
        self.click_on_maintenance_settings()
        self.click_on_maintenance_device_settings()
        self.switch_to_content_frame()
        self.click_on_reboot_button()
        self.confirm_reboot_alert()

        # We can add a wait here to properly log out of the router page, but that's totally not required as the router
        # will automatically redirect to main login page after restart

        time.sleep(1)
        self.driver.quit()

        Util.windows_log(log_duration=self.log_duration, message="The router is successfully restarted.")

    def create_ssid(self, ssid_name=None, ssid_index: str | int = 3, ssid_password=None):
        self.go_to_basic_wlan_settings()

        selection = Select(self.wait_for_element(by=By.NAME, value="wlSsidIdx"))
        selection.select_by_value(str(ssid_index))
        self.driver.find_element(by=By.NAME, value="wlSsid").clear()
        self.driver.find_element(by=By.NAME, value="wlSsid").send_keys(
            Util.generate_random_text(10) if ssid_name is None else ssid_name)
        check_box = self.driver.find_element(by=By.NAME, value="enableSsid").is_selected()
        if not check_box:
            self.driver.find_element(by=By.NAME, value="enableSsid").click()

        selection = Select(self.driver.find_element(by=By.NAME, value="wlnAuthMode"))
        selection.select_by_value('WPAand11i')
        self.driver.find_element(by=By.NAME, value="wlWpaPsk").clear()
        self.driver.find_element(by=By.NAME, value="wlWpaPsk").send_keys(
            self.default_temp_password if ssid_password is None else ssid_password)
        self.submit_basic_wifi_settings()
        self.exit_from_basic_wlan_settings()

        Util.windows_log(log_duration=self.log_duration,
                         message=f"Temporary Wi-Fi network is successfully created with SSID: {ssid_name}.")

    def ssid_dis(self, ssid_index=3):
        self.go_to_basic_wlan_settings()
        selection = Select(self.wait_for_element(by=By.NAME, value="wlSsidIdx"))
        self.driver.implicitly_wait(1)
        selection.select_by_value(str(ssid_index))
        self.driver.implicitly_wait(1)
        check_box = self.driver.find_element(by=By.NAME, value="enableSsid").is_selected()

        if check_box:
            self.driver.find_element(by=By.NAME, value="enableSsid").click()
            self.submit_basic_wifi_settings()
            self.exit_from_basic_wlan_settings()

            Util.windows_log(log_duration=self.log_duration,
                             message="Temporary Wi-Fi network is successfully disabled.")

        else:
            self.exit_from_basic_wlan_settings()
            Util.windows_log(log_duration=self.log_duration, message="Temporary Wi-Fi network is already disabled.")

    def chk_speed(self):
        self.go_to_basic_wlan_settings()

        selection = Select(self.wait_for_element(by=By.NAME, value="wlgnMode"))
        selected_option = selection.first_selected_option.text
        if selected_option == "802.11b/g":
            selection = Select(self.driver.find_element(by=By.NAME, value="wlRate"))
            wlan_mode = selection.first_selected_option.text


        self.exit_from_basic_wlan_settings()
        Util.windows_log(log_duration=self.log_duration,
                         message=f"Wi-Fi speed is  {"maxed" if selected_option != "802.11b/g" else wlan_mode}.")

    # TODO: Complete this code.
    def block_device(self, device_mac):
        self.go_to_basic_wlan_filtering_settings()
        if not self.driver.find_element(by=By.ID, value="isFilter").is_selected():
            self.driver.find_element(by=By.ID, value="isFilter").click()
            time.sleep(self.laptop_implicit_wait)

        wlan_filtering_table_element = self.wait_for_element(by=By.XPATH,
                                                             value="/html/body/form/div[1]/table[2]/tbody/tr[2]/td/table[1]")
        wlan_filtering_table_rows_elements = wlan_filtering_table_element.find_elements(by=By.TAG_NAME, value="tr")
        wlan_filtering_table_rows = [row.text.strip() for row in wlan_filtering_table_rows_elements][1:]

        print(wlan_filtering_table_rows)

        if device_mac.upper() in wlan_filtering_table_rows:
            Util.windows_log(log_duration=self.log_duration,
                             message=f"The device with MAC address {device_mac} is already blocked.")
            return

        # TODO: Now that requested mac isn't already blocked, we need to add to blacklist.

    def evaluate_rate_of_usage(self, used_gb, remaining_days):
        std_usage_rate_gb = self.current_quota / 30.0
        try:
            usage_rate_gb = used_gb / (30 - remaining_days)
        except ZeroDivisionError:
            Util.windows_log(log_duration=self.log_duration, message=
            f"Wait another day to calculate the accurate rate of usage.")
            return


        if usage_rate_gb - std_usage_rate_gb >= 0.07 * std_usage_rate_gb:
            Util.windows_log(log_duration=self.log_duration, message=
            f"Usage is high⚠️, try lowering it.\n({usage_rate_gb: 0.2f} GB/Day to std {std_usage_rate_gb: 0.2f} GB/Day)")
        else:
            Util.windows_log(log_duration=self.log_duration,
                             message=f"Usage is reasonable👍.\n({usage_rate_gb: 0.2f} GB/Day to std {std_usage_rate_gb: 0.2f} GB/Day)")

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
            # options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

            self.driver = webdriver_instance(options=options, service=service)
        except selenium.common.exceptions.SessionNotCreatedException:
            print("*" * 100 + "\nFAILED:\n" + "*" * 100 + f"\n")
            print("\n\nTry switching to a different browser.\n\n")
            self.run_ui()

    def fill_login_page(self):
        self.driver.get(self.routerURL)
        self.driver.find_element(by=By.NAME, value="Username").send_keys(self.router_login_page_user_name)

        self.driver.find_element(by=By.NAME, value="Password").send_keys(self.router_login_page_password)

        self.driver.find_element(by=By.ID, value="btnLogin").click()

    def wait_for_element(self, by, value, timeout=default_timeout, wait_after=0):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            if wait_after != 0:
                time.sleep(wait_after)
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            return element
        except Exception as e:
            print(f"Element not found: {e}")
            Util.windows_log(log_duration=self.log_duration, message="Element not found Error.")
            return None

    def go_to_basic_settings(self):
        self.specify_browser()
        self.fill_login_page()
        self.switch_to_left_side_frame()
        self.click_on_basic_settings()

    def switch_to_left_side_frame(self):
        self.wait_for_element(By.ID, 'listfrm')
        self.driver.switch_to.frame('listfrm')

    def click_on_basic_settings(self):
        self.wait_for_element(By.ID, "link_Admin_1").click()

    def go_to_basic_wlan_settings(self):
        self.go_to_basic_settings()
        self.driver.find_element(by=By.ID, value="link_Admin_1_2").click()
        self.driver.switch_to.default_content()
        self.switch_to_content_frame()

    def go_to_maintenance_settings(self):
        self.specify_browser()
        self.fill_login_page()
        self.switch_to_left_side_frame()
        self.click_on_maintenance_settings()

    def go_to_maintenance_device_settings(self):
        self.go_to_maintenance_settings()
        self.switch_to_tab_frame()
        self.wait_for_element(by=By.ID, value="link_Admin_3_2").click()
        self.switch_to_content_frame()

    def click_on_maintenance_settings(self):
        self.wait_for_element(By.ID, "link_Admin_3").click()

    def click_on_maintenance_device_settings(self):
        self.wait_for_element(By.ID, "link_Admin_3_1").click()

    def click_on_reboot_button(self):
        self.wait_for_element(By.NAME, "btnReboot").click()

    def confirm_reboot_alert(self):
        self.driver.switch_to.alert.accept()

    def switch_to_content_frame(self):
        self.driver.switch_to.default_content()
        self.wait_for_element(By.ID, 'contentfrm')
        self.driver.switch_to.frame('contentfrm')

    def go_to_basic_wlan_filtering_settings(self):
        self.go_to_basic_wlan_settings()
        self.switch_to_tab_frame()
        self.wait_for_element(by=By.ID, value="link_Admin_1_2_1").click()
        self.switch_to_content_frame()

    def switch_to_tab_frame(self):
        self.driver.switch_to.default_content()
        self.wait_for_element(By.ID, 'tabfrm')
        self.driver.switch_to.frame('tabfrm')
