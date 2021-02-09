### argumenti
from sys import argv, exit
script, folder = argv
###
# import logging
import ast # za pretvaranja stringa u dict
import os # navigacija po direktorijima
import pdfminer_acroform_extract as acroform # pdfminer vadi podatke iz pdfa
import textract
import pathlib
# LOGGER.setLevel(logging.WARNING)

### POCETAK
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
        #
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

def pronadji_prijavnice(folder): ## zaseban modul??
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".pdf"):
                print (filepath)
                try:
                    data = acroform.acro_extract(filepath)
                    ispuni_obrazac(data, filepath)
                except ValueError:
                    continue

def txtrct(folder):
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath_txt = subdir + os.sep + filename

            if filepath_txt.endswith('.docx'):
                print(filepath_txt)
                try:
                    tekst = textract.process(filepath_txt)
                    tekst = tekst.decode(encoding='utf-8')
                    print(tekst)
                    #
                    with open(filepath_txt.replace(pathlib.Path(filepath_txt).suffix,'.txt'), 'w', encoding='utf8') as tekstic:
                        tekstic.write(tekst)
                except (ValueError, FileNotFoundError):
                    continue
### main

def main():
    print('Ovo je robot za fajlove')
    txtrct(folder)
    pronadji_prijavnice(folder)
    # ispuni_obrazac(data, prijavnica)

if __name__ == "__main__":
    main()

### KRAJ
