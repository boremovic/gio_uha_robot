### argumenti
from sys import argv, exit
script, prijavnica = argv
###
# import logging
import ast # za pretvaranja stringa u dict
import os # navigacija po direktorijima
import time
# import pdfminer_acroform_extract as acroform # pdfminer vadi podatke iz pdfa
### selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
#
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.remote.remote_connection import LOGGER
# LOGGER.setLevel(logging.WARNING)
### web driver za selenium
driver = webdriver.Edge('C:\edgedriver_win64\msedgedriver.exe')

### POCETAK
def gio_login(driver, podatci_dict):
    driver.get("http://gio.uha.hr/log-in/")
    assert "uha.hr" in driver.title
    gio_uha = driver.current_window_handle
    # ulogiraj se
    username = driver.find_element_by_name("login_username")
    username.clear()
    username.send_keys("bartoloremovic")
    # password
    password = driver.find_element_by_name("login_password")
    password.clear()
    password.send_keys("Z1dj4nzidjan")
    password.send_keys(Keys.RETURN)
    # otvori tab
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    # ucitaj stranicu u tab
    # driver.get('https://maps.google.com')
    # pozovi javascript komandu
    driver.execute_script('''window.open("https://maps.google.com", "_blank");''')
    # maps_gumb = driver.find_element_by_xpath("//div[@id='introAgreeButton']")
    # maps_gumb = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='introAgreeButton']")))
    # maps_gumb = driver.find_element_by_xpath("//*[@id='introAgreeButton']")
    # xpath...
    # /html/body/div/c-wiz/div[2]/div/div/div/div/div[2]/form/div
    # //*[@id="introAgreeButton"]
    # maps_gumb.click()
    # adresa = driver.find_element_by_id('searchboxinput')
    # adresa.send_keys(str(podatci_dict[21]))
    time.sleep(3)
    driver.switch_to.window(gio_uha)

def nova_prijavnica(driver):
    dodaj = driver.find_element_by_name("dodaj")
    dodaj.send_keys(Keys.RETURN)

def ispuni_prijavnicu(driver, podatci_dict):
    for key in podatci_dict:
        try:
            polje = driver.find_element_by_name(key)
            polje.send_keys(str(podatci_dict[key]))
            print(podatci_dict[key])
        except ElementNotInteractableException as exception:
            continue

    # tekst = driver.find_element_by_xpath("//iframe[@class_name='cke_wysiwyg_frame']") #???
    # driver.switch_to.frame(iframe);
    # tekst.send_keys('/')
    # driver.switch_to.default_content()

    autor_clanstvo = driver.find_element_by_xpath("//select[@name='autorclanstvo1']")
    opcija = autor_clanstvo.find_element_by_xpath("//option[@value='NIJE']")
    opcija.click()

### main

def main():
    print('Ovo je robot za gio.uha.hr')
    # ucitaj prijavnicu
    with open(prijavnica.replace('.pdf','.txt'), 'r', encoding='utf8') as ucitana_prijavnica:
        podatci_str = ucitana_prijavnica.read()
    podatci_dict = ast.literal_eval(podatci_str) #pretvori string u dict
    # logiraj se...
    gio_login(driver, podatci_dict)
    driver.get("http://gio.uha.hr/prijavnice/?prijave=5")
    nova_prijavnica(driver)
    ispuni_prijavnicu(driver, podatci_dict)
    driver.stop_client()
    exit()

if __name__ == "__main__":
    main()

### KRAJ
