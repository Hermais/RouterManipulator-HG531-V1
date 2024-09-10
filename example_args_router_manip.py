import sys

from router_manipulator.hg_531_v1 import HG531V1RouterManipulator
from secret import MySecrets

program = HG531V1RouterManipulator(router_login_page_user_name="admin",
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


