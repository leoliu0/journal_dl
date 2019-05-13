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
    os.mkdir(f'{year}_RFS')
except:
    pass

main = 'https://academic.oup.com'

vol = year-1987

for issue in range(1,13):
    a = requests.get(f'https://academic.oup.com/rfs/issue/{vol}/{issue}',headers=headers)
    if 'cannot be found' in a.text:
        continue
    b = html.document_fromstring(a.text)
    articles = [x for x in b.xpath('//a[@href]/@href') if re.search(r'/rfs/article/\d*/\d*/\d*/\d*$',x)]
    for art in articles:
        title = b.xpath('//a[@href="{}"]/text()'.format(art))[0].replace(' ','_').replace(':','_')+'.pdf'
        print(title)
        path = os.path.join(f'{year}_RFS',title)
        if os.path.isfile(path):
            continue
        c = html.document_fromstring(requests.get(main+art,headers=headers).text)
        pdflink = c.xpath('//a[@class="al-link pdf article-pdfLink"]/@href')[0]
        d = requests.get(main+pdflink,headers=headers,stream=True)
        with open(path,'wb') as f:
            shutil.copyfileobj(d.raw,f)
