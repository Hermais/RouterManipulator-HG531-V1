### README for HG531V1 Router Manipulator

## Overview
The **HG531V1RouterManipulator** is a Python-based module designed to interact with Huawei HG531V1 routers. It allows users to manipulate router settings such as WiFi speed, SSID creation, router reboot, and internet quota checking. The module is capable of being run in both a command-line (CLI) interface as well as a User Interface (UI) mode.

## Features
- Change Wi-Fi speed (options: 1, 2, 5.5, 6, 9, 11, or Full speed).
- Reboot the router.
- Disable or create temporary SSID networks.
- Check internet quota usage and remaining quota.
- Switch between Chrome, Firefox, and Edge browsers.
- Perform device blocking operations (soon).
- Log router actions for future reference.
- Customizable via a wide array of command-line options.

## Prerequisites
- Python 3.x
- A WebDriver for your preferred browser (Chrome, Firefox, Edge).
- Required libraries (install using `pip` if not already available):
  ```bash
  pip install selenium
  pip install playsound
  pip install webdriver_manager
  pip install plyer
  pip install psutil
  ```


## Configuration
Before running the module, you need to set up your router login credentials and WE account details (if using quota checking functionality).

```python
from router_manipulator import hg_531_v1
manipulator = hg_531_v1.HG531V1RouterManipulator(
    router_login_page_user_name="your_router_username",
    router_login_page_password="your_router_password",
    router_url="http://your.router.url",
    we_account_number="your_we_account_number",
    we_account_password="your_we_account_password",
    we_url="https://your.we.account.url",
    current_quota=100,  # Set to your current quota in GB
    log_duration=30,  # Time for logging duration
    laptop_implicit_wait=10  # Implicit wait time for WebDriver
)
```

### Parameters:
- **router_login_page_user_name**: Your router's admin username.
- **router_login_page_password**: Your router's admin password.
- **router_url**: The URL of your router's login page.
- **we_account_number**: Your WE (internet provider) account number.
- **we_account_password**: Your WE account password.
- **we_url**: The WE account management URL.
- **current_quota**: Current internet quota in GB.
- **log_duration**: The duration for logging activities (in seconds).
- **laptop_implicit_wait**: Implicit wait time for WebDriver actions.

## Usage

### Running in User Interface (UI) Mode
This mode interacts with the user through prompts and allows for manipulation via manual input.

```python
manipulator.run_ui()
```

### Running in Command-line (CLI) Mode
The CLI mode allows you to pass in arguments to perform specific actions directly.

```python
manipulator.run_args('full')  # Example: Set the WiFi to full speed
```

#### Supported Commands:
- **full**: Switches the WiFi speed to full.
- **res**: Reboot the router.
- **dis**: Disable temporary SSID.
- **c**: Create a custom temporary SSID.
- **r**: Create a random temporary SSID.
- **chk**: Check the current WiFi speed setting.
- **qchk**: Check the remaining internet quota.
- **block**: Block a device by MAC address.
- **firefox, chrome, edge**: Switches between different browsers.
- **quit/exit**: Exit the program.

### Example Commands in UI Mode
- Enter `full` to set WiFi speed to full.
- Enter `res` to restart the router.
- Enter `chk` to check the current WiFi speed.
- Enter `qchk` to check the remaining quota.

### Example Script that accepts CLI arguments
```python
from  secret import MySecrets
import sys
from router_manipulator import hg_531_v1
program = hg_531_v1.HG531V1RouterManipulator(router_login_page_user_name="admin",
                                       router_login_page_password=MySecrets.routerLoginPagePassword,
                                       router_url="http://192.168.1.1/",
                                       we_account_number=MySecrets.weAccountNumber,
                                       we_account_password=MySecrets.weAccountPassword,
                                       we_url="https://my.te.eg/user/login",
                                       current_quota=200,
                                       log_duration=5,
                                       browser="edge",
                                       laptop_implicit_wait=15,
                                       )
program.command = program.run_args(sys.argv[1])
```

Assuming the script file name is `router_script.py`, you can run the script with the following command:
```bash
python router_script.py full
```
Also you can use the provided example autohotkey script `router_manip_args_no_exe.ahk`, after providing you python path and script absolute path.  
This means that you need to install authotkey on your system first.


*Note*: The `secret.py` file should contain your router login password and WE account password.

## Error Handling
In case of an unknown error, a log entry will be created in the Windows logs, and the error will be displayed. The user will have the option to retry or quit the program.

## Logging
The module includes logging capabilities that store important events such as speed changes, SSID changes, and router reboots. Logs are stored in a file for future reference.

## Contribution
Feel free to fork this repository and contribute by submitting a pull request.

## Contact
For issues or inquiries, please submit an issue on this repository.


