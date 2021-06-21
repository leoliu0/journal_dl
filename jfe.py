import argparse
import zipfile
from glob import glob
import shutil
import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

parser = argparse.ArgumentParser()
parser.add_argument('year')
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
year = int(args.year)

wd = f"{year}_jfe"
try:
    os.mkdir(wd)
except:
    shutil.rmtree(wd)
    os.mkdir(wd)

os.chdir(wd)

options = Options()
if not args.debug:
    options.headless = True
profile = webdriver.FirefoxProfile()

profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference('browser.download.dir', os.getcwd())

mime_types = [
    'text/plain', 'application/vnd.ms-excel', 'text/csv', 'application/csv',
    'text/comma-separated-values', 'application/download',
    'application/octet-stream', 'binary/octet-stream', 'application/binary',
    'application/x-unknown'
]
profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       ",".join(mime_types))

n = 0
start_vol_no = (year - 2000) * 4 + 55
for vol in range(start_vol_no, start_vol_no + 4):
    for issue_no in range(1, 4):
        n += 1
        url = f'https://www.sciencedirect.com/journal/journal-of-financial-economics/vol/{vol}/issue/{issue_no}'
        print(url)
        d = webdriver.Firefox(options=options, firefox_profile=profile)
        while len(glob("*.zip")) < n:
            d.get(url)
            time.sleep(5)
            try:
                d.find_element_by_xpath(
                    "/html/body/div[4]/div/div/div/main/section[1]/div/div/div/form/button"
                ).click()
                time.sleep(10)
            except:
                time.sleep(10)
        d.close()

for file in glob(f"*.zip"):
    if zipfile.is_zipfile(file):
        with zipfile.ZipFile(file) as item:
            item.extractall()
        os.remove(file)
