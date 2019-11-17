import json
import requests 
from bs4 import BeautifulSoup 

def try_remove(word, l):
    if word in l:
        l.remove(word)

def extract_dictionary(url):
    # answer  = {'my' : ["lol", 'kkkk'], "your" : 'klk'}
    answer  = {}
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    tables = soup.findAll('table')
    for table in tables:
        for row in table.findAll('tr'):
            values = row.findAll('td')
            key = values[1].text
            attr = values[2].text
            attr = attr.replace(u'\xa0', u'')
            attr = attr.split(', ')
            attr[-1] = attr[-1].replace(u' ।', '')
            attr[-1] = attr[-1].replace(u'।', '')
            if '(' in key:
                key = key.replace("(","")
                key = key.replace(")","")
                key = key.split(' ')
                attr.append(key[1])
                key = key[0]
            try_remove(u'कर',attr)
            try_remove(u'हर',attr)
            try_remove(u'तक',attr)
            answer[key] = attr
    return answer


# Extract the synonyms
URL = "https://hindistudent.com/hindi-vyakaran/paryayvachi-shabd-in-hindi/"
paryavachi = extract_dictionary(URL)
del paryavachi[u'शब्द']
del paryavachi[u'भय']
del paryavachi[u'देशभक्त']
print(paryavachi)
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