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
        for w in s.split(' '):
            if w:
                text += w
                text += ' '
    return text


import sys
import os
if __name__ == '__main__':
    for name in open(sys.argv[1]):
        name = name.strip()
        out = sys.argv[2] + '/' + os.path.basename(name)
        print(out)
        with open(out, mode='w') as f:

            f.write(get_content('https://en.wikipedia.org'+name))


        

