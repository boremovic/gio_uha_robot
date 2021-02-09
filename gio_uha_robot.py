### argumenti
from sys import argv, exit
script, folder = argv
###
# import logging
import ast # za pretvaranja stringa u dict
import os # navigacija po direktorijima
import pdfminer_acroform_extract as acroform # pdfminer vadi podatke iz pdfa
### selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
# from selenium.webdriver.remote.remote_connection import LOGGER
# LOGGER.setLevel(logging.WARNING)
### web driver za selenium
# driver = webdriver.Edge('C:\edgedriver_win64\msedgedriver.exe')

### POCETAK
print('Ovo je robot za fajlove')

def gio_login(driver):
    driver.get("http://gio.uha.hr/log-in/")
    assert "uha.hr" in driver.title

    username = driver.find_element_by_name("login_username")
    username.clear()
    username.send_keys("bartoloremovic")

    password = driver.find_element_by_name("login_password")
    password.clear()
    password.send_keys("Z1dj4nzidjan")
    password.send_keys(Keys.RETURN)

def nova_prijavnica(driver):
    dodaj = driver.find_element_by_name("dodaj")
    dodaj.send_keys(Keys.RETURN)

def ispuni_prijavnicu(driver, prijavnica):
    with open(prijavnica.replace('.pdf','.txt'), 'r', encoding='utf8') as ucitana_prijavnica:
        podatci_str = ucitana_prijavnica.read()

    podatci_dict = ast.literal_eval(podatci_str) #pretvori string u dict

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

def ispuni_obrazac(data, prijavnica):
    with open('prijavnica_dict.txt', 'r', encoding='utf8') as prijavnica_predlozak:
        predlozak_str = prijavnica_predlozak.read()
        predlozak_dict = ast.literal_eval(predlozak_str)

    with open(prijavnica.replace('.pdf','.txt'), 'w', encoding='utf8') as prijavnica_nova:
        obrazac_novi = predlozak_dict

        # pripremi podatke za upis u web obrazac ## elegantnije napisati? bez ponavljanja
        obrazac_novi['naziv']=data['Text1']
        obrazac_novi['lokacijaadresa']=data['Text2']
        obrazac_novi['investitornaziv-1']=data['Text3']
        obrazac_novi['autorime1']=data['Text4']

        #prazna polja
        obrazac_novi['autorprezime1']=' '
        obrazac_novi['autoroib1']=' '
        obrazac_novi['kontaktime']=' '
        obrazac_novi['kontaktprezime']=' '
        obrazac_novi['kontaktemail']=' '
        obrazac_novi['lokacijagrad']=' '
        obrazac_novi['lokacijazip']=' '
        obrazac_novi['lokacijagps']=' '
        obrazac_novi['podacigdp']=' '
        obrazac_novi['podacigpg']=' '
        obrazac_novi['podacivrijednost']=' '

        obrazac_novi['projektninaziv-1']=data['Text5']
        obrazac_novi['suradnicinaziv-1']=data['Text6']
        #obrazac_novi['']=data['Text7'] #fotograf
        obrazac_novi['tvrtkanaziv1']=data['Text8']
        obrazac_novi['izvodacnaziv-1']=data['Text9']
        obrazac_novi['podacigpp']=data['Text10']
        obrazac_novi['podacigdg']=data['Text11']
        obrazac_novi['podacipo']=data['Text12']#; obrazac_novi['podacipo']=obrazac_novi['podacipo'][:-2] if obrazac_novi['podacipo'].endswith('m2')
        obrazac_novi['podaciutp']=data['Text13']#; obrazac_novi['podaciutp']=obrazac_novi['podaciutp'][:-2] if obrazac_novi['podaciutp'].endswith('m2')
        #obrazac_novi['podacivrijednost']=obrazac_novi[int('podacipo')*int('podaciutp')]
        obrazac_novi['podacivrijednost']=data['Text14']
        #obrazac_novi['']=data['Text15'] #adresa autora
        obrazac_novi['kontakttel']=data['Text16']
        #obrazac_novi['kontaktemail']=data['Text17'] # problem sa znakom @ - selenium/js ga interpretira kao paste-from-clipboard
        #if 'U+0040' in obrazac_novi['kontaktemail']:
        #obrazac_novi['kontaktemail']=obrazac_novi['kontaktemail'].replace('U+0040', 'U+0040'.decode('utf-8'))
        #obrazac_novi['']=data['Text18'] #mjesto
        #obrazac_novi['']=data['Text19'] #datum

        # pretvori dict u string i formatiraj da bude citljiviji
        obrazac_novi_str = str(obrazac_novi)
        obrazac_novi_str = "{\n" + "\n".join("{!r}: {!r},".format(k, v) for k, v in obrazac_novi.items()) + "\n}"
        prijavnica_nova.write(obrazac_novi_str)

def pronadji_prijavnice(folder, driver): ## zaseban modul??
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".pdf"):
                print (filepath)
                try:
                    data = acroform.acro_extract(filepath)
                    ispuni_obrazac(data, filepath)

                    # driver.get("http://gio.uha.hr/prijavnice/?prijave=5")
                    #nova_prijavnica(driver)

                    # ispuni_prijavnicu(driver, filepath)
                    # forma_submit = driver.find_element_by_class_name('pure-button') # submit forme...
                    # try:
                        # forma_submit.submit()
                    # except UnexpectedAlertPresentException:
                        # forma_submit.submit()
                except ValueError:
                    continue

### main

def main():
    pronadji_prijavnice(folder, driver)
    # gio_login(driver)
    # driver.get("http://gio.uha.hr/prijavnice/?prijave=5")
    # nova_prijavnica(driver)
    # ispuni_obrazac(data, prijavnica)
    # ispuni_prijavnicu(driver, prijavnica)
    driver.stop_client()
    exit()

if __name__ == "__main__":
    main()

### KRAJ
