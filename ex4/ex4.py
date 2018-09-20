import nltk
import re
import urllib3
from bs4 import BeautifulSoup

def get_content(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)

    soup = BeautifulSoup(r.data,'html.parser')

    p1 = r"<.+?>"
    p2 = r"\[.+?\]"
    rep1 = re.compile(p1)
    rep2 = re.compile(p2)

    reps = ["\n"]

    text = ''
    for i in soup.find_all('p'):
        s = str(i)
        for r in reps:
            s = s.replace(r," ")
        
        s = rep1.sub(" ", s)
        s = rep2.sub(" ", s)
        s = s.strip()
        text += s
        text += ' '
    return text

