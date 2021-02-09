from sys import argv

script, prijavnica = argv

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text

from PyPDF2 import PdfFileReader
#
data = {}
# 
def decode_value(value):

    # decode PSLiteral, PSKeyword
    if isinstance(value, (PSLiteral, PSKeyword)):
        value = value.name

    # decode bytes
    if isinstance(value, bytes):
        value = decode_text(value)

    return value

def acro_extract(prijavnica):
    while True:
        with open(prijavnica, 'rb') as fp:
            # provjeri je li AcroForm
            parser = PDFParser(fp)

            doc = PDFDocument(parser)
            res = resolve1(doc.catalog)

            if 'AcroForm' not in res:
                raise ValueError("No AcroForm Found")

            # pypdf2 - procitaj naslov

            pdf = PdfFileReader(fp)
            information = pdf.getDocumentInfo()
            #print(information.title)

            # provjeri je li ucitani pdf pravilna prijavnica

            if 'Godišnja izložba ostvarenja hrvatskih arhitekata' not in information.title:
                raise ValueError("Ovo nije prijavnica")
            elif type(information.title) is None:
                continue

            # pdfminer - iscitaj vrijednosti iz polja

            fields = resolve1(doc.catalog['AcroForm'])['Fields']  # may need further resolving

            for f in fields:
                field = resolve1(f)
                name, values = field.get('T'), field.get('V')

                # decode name
                name = decode_text(name)

                # resolve indirect obj
                values = resolve1(values)

                #print(type(values))

                # decode value(s)
                if isinstance(values, list):
                    values = [decode_value(v) for v in values]
                elif isinstance(values, type(None)):
                    values = str(decode_value(values) or ' ') # ako je polje prazno pretvori vrijednost u prazan string
                    #pass
                elif '\r' in decode_value(values): # provjeri je li u vise redova
                    values = decode_value(values)
                    values = values.splitlines()
                    values = ' '.join(values)
                else:
                    values = decode_value(values)

                data.update({name: values})

            return(data)

def main():
    acro_extract(prijavnica)

if __name__ == "__main__":
    main()
