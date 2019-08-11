import requests
from lxml import html
import shutil
import os

import argparse
import re
parser = argparse.ArgumentParser(description='Specify year to download')
parser.add_argument('year', type=int, help='The year of articles to download')
args = parser.parse_args()
year = args.year

headers= {
     'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'
}

try:
    os.mkdir(f'{year}_AER')
except:
    pass

url = 'https://www.aeaweb.org/journals/aer/issues'

a = html.document_fromstring(requests.get(url,headers=headers).text)

issues = [ref for ref,vol in zip(a.xpath('//a[@href]/@href'),a.xpath('//a[@href]/text()'))
             if 'issues' in ref and str(year) in vol]

for issue in issues:
    url2 = 'https://www.aeaweb.org'+issue
    print(url2)

    b = html.document_fromstring(requests.get(url2,headers=headers).text)

    [x for x in b.xpath('//a[@href]/text()') if 'articles?' in x]

    ids, aer, names = [],[],[]
    for ref, name in zip(b.xpath('//a[@href]/@href'),b.xpath('//a[@href]/text()')):
        if 'articles?' in ref and len(ref.split('/')[2])==12:
            aer.append(ref.split('/')[2])
            ids.append(ref.split('id=')[1].split('/')[0])
            names.append(name)

    for id, ae, name in zip(ids,aer,names):
        name = os.path.join(f'{year}_AER',name.replace(' ','_').replace(':','_').replace('?','')+'.pdf')
        print(name)
        with open(name,'wb') as f:
            content = requests.get(f'https://pubs.aeaweb.org/doi/pdfplus/{id}/{ae}',stream=True)
            shutil.copyfileobj(content.raw,f)

