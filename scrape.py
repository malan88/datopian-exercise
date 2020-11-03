from bs4 import BeautifulSoup
import urllib3
import csv
from datetime import datetime, timedelta
from pprint import PrettyPrinter

http = urllib3.PoolManager()
URL = 'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm'

# Summary is an identifier unique to target table
SUMMARY = "Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"

pp = PrettyPrinter()


def get():
    data = http.request('GET', URL)
    soup = BeautifulSoup(data.data, 'html.parser')
    table = soup.find('table', {'summary': SUMMARY})
    return table


def convert(soup):
    toplevel = []
    for r in soup.find_all('tr'):
        row = []
        for d in r.find_all('td'):
            row.append(d.string)
        toplevel.append(row)

    # filter out empty rows
    toplevel = list(
        filter(lambda l: bool(list(filter(None, l))),
               toplevel)
    )
    toplevel.pop(0)
    return toplevel


def normalize(table):
    newtable = []

    for row in table:
        rawdate = row[0].split(' to ')[0].replace('\xa0\xa0', '')
        prepped_date = rawdate.replace('- ', '-0')
        date = datetime.strptime(prepped_date, '%Y %b-%d').date()
        for i, price in enumerate(row[1:]):
            currentdate = date + timedelta(days=i)
            newtable.append([currentdate.strftime('%Y-%m-%d'), price])

    return newtable


def writecsv(table):
    with open('data.csv', 'w', newline='') as fout:
        writer = csv.writer(fout, dialect='excel')
        for row in table:
            writer.writerow(row)


def main():
    table = get()
    table = convert(table)
    table = normalize(table)
    writecsv(table)

if __name__ == "__main__":
    main()
