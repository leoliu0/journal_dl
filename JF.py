import requests
from lxml import html
import re
import shutil
import argparse
import os

parser = argparse.ArgumentParser(description='Specify year to download')
parser.add_argument('year', type=int, help='The year of articles to download')

args = parser.parse_args()
year = args.year
url = 'https://onlinelibrary.wiley.com'

try:
    os.mkdir(f'{year}_JF')
except:
    pass

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
}

volume = requests.get(f'https://onlinelibrary.wiley.com/loi/15406261/year/{year}',headers=headers)
volumes = html.document_fromstring(volume.content)

issues = set([x for x in volumes.xpath('//a[@href]/@href') if re.search('/\d{4}/',x)])

for issue in issues:
    issue_res = requests.get(url + issue,headers=headers)

    elem = html.document_fromstring(issue_res.content)
    dois = [x for x in elem.xpath("//div[h3[@title='ARTICLES']]//a[@href]/@href") if '/pdf/' in x]
    fnames = ([x for x in elem.xpath("//div[h3[@title='ARTICLES']]//a/h2/text()")])

    for doi,fname in zip(dois,fnames):
        pdf = requests.get(url+doi,headers=headers,stream=True)
        fname =  os.path.join(f'{year}_JF/', fname.replace(' ','_')+ '_' + str(year) + '.pdf')
        print(fname)
        with open(fname,'wb') as f:
            shutil.copyfileobj(pdf.raw,f)
