import re
from lxml import html
def load(p):
    return html.fromstring(open(p,'rb').read())
def rows_of(t):
    out=[]
    for tr in t.iter('tr'):
        cells=[re.sub(r'\s+',' ',(td.text_content() or '').replace('\xa0',' ')).strip() for td in tr.iter('td','th')]
        cells=[c for c in cells if c not in('','$',')','%','(')]
        if cells: out.append(cells)
    return out
def find_tables(doc,pat):
    res=[]
    for t in doc.iter('table'):
        txt=t.text_content()
        if re.search(pat,txt): res.append(rows_of(t))
    return res
