import io
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer

add_printer(1)


def patch_exe(executable_path):
    if is_binary_patched(executable_path=executable_path):
        return True
    start = time.perf_counter()
    with io.open(executable_path, "r+b") as fh:
        content = fh.read()
        # match_injected_codeblock = re.search(rb"{window.*;}", content)
        match_injected_codeblock = re.search(rb"\{window\.cdc.*?;\}", content)
        if match_injected_codeblock:
            target_bytes = match_injected_codeblock[0]
            new_target_bytes = (
                b'{console.log("undetected chromedriver 1337!")}'.ljust(
                    len(target_bytes), b" "
                )
            )
            new_content = content.replace(target_bytes, new_target_bytes)
            if new_content == content:

                print(
                    "something went wrong patching the driver binary. could not find injection code block"
                )
            else:
                print(
                    "found block:\n%s\nreplacing with:\n%s"
                    % (target_bytes, new_target_bytes)
                )
            fh.seek(0)
            fh.write(new_content)
    print(
        "patching took us {:.2f} seconds".format(time.perf_counter() - start)
    )


def is_binary_patched(executable_path=None):
    try:
        with io.open(executable_path, "rb") as fh:
            return fh.read().find(b"undetected chromedriver") != -1
    except FileNotFoundError:
        return False


def g(q='*'):
    return get_df(driver, By, WebDriverWait, expected_conditions, queryselector=q,
                  with_methods=True, )


operapath = r"C:\ProgramData\anaconda3\envs\dfdir\operadriver.exe"
patch_exe(operapath)
webdriver_service = service.Service(operapath)
webdriver_service.start()
userdir = 'c:\\operauser'
if not os.path.exists(userdir):
    os.makedirs(userdir)
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Opera GX\opera.exe"
options.add_experimental_option('w3c', True)
options.add_argument(f'--user-data-dir={userdir}')
options.add_argument("--incognito")
options.arguments.extend(["--no-default-browser-check", "--no-first-run"])
options.arguments.extend(["--no-sandbox", "--test-type"])
# options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")

driver = webdriver.Remote(webdriver_service.service_url, options=options)
driver.get('https://www.google.com/')
