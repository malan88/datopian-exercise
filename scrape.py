from bs4 import BeautifulSoup
import urllib3
import csv
from pprint import PrettyPrinter

http = urllib3.PoolManager()
URL = 'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm'

# Summary is an identifier unique to target table
SUMMARY = "Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"

pp = PrettyPrinter()


def gettable():
    data = http.request('GET', URL)
    soup = BeautifulSoup(data.data, 'html.parser')
    table = soup.find('table', {'summary': SUMMARY})
    return table


def converttable(soup):
    toplevel = []
    for r in soup.find_all('tr'):
        row = []
        for d in r.find_all('td'):
            row.append(d.string)
        toplevel.append(row)
    toplevel = list(filter(lambda l: bool(list(filter(None, l))), toplevel))
    return toplevel


def writecsv(table):
    with open('data.csv', 'w', newline='') as fout:
        writer = csv.writer(fout, dialect='excel')
        for row in table:
            writer.writerow(row)


def main():
    table = gettable()
    table = converttable(table)
    pp.pprint(table)
    writecsv(table)

if __name__ == "__main__":
    main()
