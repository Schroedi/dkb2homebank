#! /usr/bin/env python

import argparse
import csv
from datetime import datetime

class n26(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL

csv.register_dialect("n26", n26)

n26FieldNames = ["Datum","Empfänger","Kontonummer","Transaktionstyp","Verwendungszweck","Kategorie","Betrag (EUR)","Betrag (Fremdwährung)","Fremdwährung","Wechselkurs"]

homebankFieldNames = ["date",
                      "paymode",
                      "info",
                      "payee",
                      "memo",
                      "amount",
                      "category",
                      "tags"]


def convertN26(filename):
    with open(filename, 'r', encoding='iso-8859-1') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(transactionLines(csvfile), dialect=dialect, fieldnames=n26FieldNames)

        with open("N26Homebank.csv", 'w') as outfile:
            writer = csv.DictWriter(outfile, dialect='n26', fieldnames=homebankFieldNames)
            for row in reader:
                writer.writerow(
                    {
                    'date': convertDate(row["Datum"]),
                    'paymode': 1,
                    'info': None,
                    'payee': row["Empfänger"],
                    'memo': f'{row["Verwendungszweck"]} [{row["Kategorie"]}]',
                    'amount': row["Betrag (EUR)"],
                    'category': None,
                    'tags': None
                    })

def transactionLines(file):
    lines = file.readlines()
    i = 1
    for line in lines:
        if "Betrag" in line:
            return lines[i:]
        i = i + 1

def convertDate(dateString):
    date = datetime.strptime(dateString, "%Y-%m-%d")
    return date.strftime('%d-%m-%Y')

def main():
    parser = argparse.ArgumentParser(description="Convert a CSV export file from N26 online banking to a Homebank compatible CSV format.")
    parser.add_argument("filename", help="The CSV file to convert.")

    args = parser.parse_args()

    convertN26(args.filename)
    print("N26 Cash file converted. Output file: 'N26Homebank.csv'")


if __name__ == '__main__':
    main()
