import requests
import json
from bs4 import BeautifulSoup

url = 'https://hashcat.net/wiki/doku.php?id=example_hashes'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')

# creating dict
table_dict = {}

# get all tables from the page with class set to "inline"
tables = soup.find_all('table', {'class': 'inline'})
if tables:

    for table in tables:

        # get all table rows in each table
        rows = table.find_all('tr')

        # run loop for all rows except first one, as it contains heading
        for row in rows[1:]:

            # extract columns
            cells = row.find_all(['th', 'td'])

            # {hash_type: hash_module_num}
            table_dict[cells[1].get_text(strip=True)] = int(cells[0].get_text(strip=True))

else:
    print(f'No tables with given attributes on page, check page source for table attr check.')

with open('hash_mod_nums.json','w') as json_file:
    json.dump(table_dict, json_file, indent=4)
    print('File created!')
