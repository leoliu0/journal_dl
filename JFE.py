import requests
from lxml import html
import shutil
import os
import argparse
parser = argparse.ArgumentParser(description='Specify year to download')
parser.add_argument('year', type=int, help='The year of articles to download')
args = parser.parse_args()
year = args.year


headers= {
     'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'
}

try:
    os.mkdir(f'{year}_JFE')
except:
    pass

start_vol_no = (year - 2000) * 4 + 55
for vol in range(start_vol_no, start_vol_no+4):
    for issue_no in range(1,4):
        issue_url = f'https://www.sciencedirect.com/journal/journal-of-financial-economics/vol/{vol}/issue/{issue_no}'
        print(issue_url)
        a = requests.get(issue_url,headers=headers)
        b = html.document_fromstring(a.text)

        titles = b.xpath('//span[@class="js-article-title"]/text()')
        pdfurl = [x for x in b.xpath('//a[@href]/@href') if 'md5' in x]
        for title,pdfurl in zip(titles, pdfurl):
            title = title.replace(' ','_').replace(':','_')+'.pdf'
            path = os.path.join(f'{year}_JFE',title)
            # skip downloaded pdfs
            if os.path.isfile(path):
                pass
            c = requests.get('https://www.sciencedirect.com/'+pdfurl,
                             headers=headers)
            pdf = html.document_fromstring(c.text).xpath('//a[@href]/@href')[0]
            c = requests.get(pdf, headers=headers,stream=True)

            with open(path,'wb') as f:
                shutil.copyfileobj(c.raw,f)
