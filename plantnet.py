import urllib.parse
import re
import time
import csv
import json
from urllib import request
import requests
from bs4 import BeautifulSoup

url = "https://plantnet.rbgsyd.nsw.gov.au/cgi-bin/NSWfl.pl"
params = {"page": "nswfl", "search": "yes", "namesearch":"", "dist":"", "constat":"I"}


if __name__ == '__main__':
    with open('out.csv', 'w') as file_out:
        spam = csv.writer(file_out, dialect="excel")
        response = requests.get(url=url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        search_result = tables[4]
        # a_results = search_result.find_all(string='br')

        raw_species = list()
        for raw in search_result.prettify().split('<br/>'):
            time.sleep(2)
            if "NSWfl.pl?page=nswfl&amp;lvl=sp&amp;name=" not in raw:
                continue

            raw = raw.replace('\n','' ).strip()
            match = re.match(string=raw, pattern=r'.*<a href="NSWfl.pl\?(.+)">.*<i>(.+)</i>.*</a>(.*)')
            family_url_link = match[1].strip()
            species = match[2].strip()
            common_name = match[3].strip().replace('&gt;', '')
            query = family_url_link.replace('&amp;', '&')


            family_lookup = requests.get(url=url+ "?" + query)
            soup = BeautifulSoup(family_lookup.text, 'html.parser')

            family = ''
            for element in soup.find_all('td', attrs={"align": "right"}):
                if 'Family' in element.text:
                    family = element.text.replace("Family ", "")
                    if "Subfamily" in family:
                        family = family.replace("Subfamily ", " (") + ")"
                    
                    break
            print(f"Found {(family, species,common_name)}")
            spam.writerow((family, species,common_name))

