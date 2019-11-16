import json
import requests 
from bs4 import BeautifulSoup 

def extract_dictionary(url):
    # answer  = {'my' : ["lol", 'kkkk'], "your" : 'klk'}
    answer  = {}
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    tables = soup.findAll('table')
    for table in tables:
        for row in table.findAll('tr'):
            values = row.findAll('td')
            key = values[1].text
            attr = values[2].text
            attr = attr.split(', ')
            answer[key] = attr
    return answer


# Extract the synonyms
URL = "https://hindistudent.com/hindi-vyakaran/paryayvachi-shabd-in-hindi/"
paryavachi = extract_dictionary(URL)
del paryavachi[u'शब्द']
final = []
for key in paryavachi.keys():
    paryavachi[key].append(key)
    final.append(paryavachi[key])
with open('paryavachis.txt', 'w+') as json_file:
    json.dump(final, json_file)

# Extract the antonyms
URL = "https://hindistudent.com/hindi-vyakaran/vilom-shabd/vilom-shabd-in-hindi/"
vilom_shabd = extract_dictionary(URL)
final = {}
for key in vilom_shabd.keys():
    final[key] = vilom_shabd[key]
    for opposite in vilom_shabd[key]:
        final[opposite] = [key]
with open('vilom_shabds.txt', 'w+') as json_file:
    json.dump(final, json_file)