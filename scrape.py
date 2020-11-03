from bs4 import BeautifulSoup
import urllib3
import csv

http = urllib3.PoolManager()
URL = 'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm'

# Summary is an identifier unique to target table
SUMMARY = "Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"


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
            row.append(str(d))
        toplevel.append(row)

    return toplevel



def main():
    table = gettable()
    table = converttable(table)
    print(table)

if __name__ == "__main__":
    main()
