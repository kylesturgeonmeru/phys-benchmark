import re,glob,json,sys
sys.path.insert(0,'.')
import pandas as pd
from lxml import html
def text(p):
    d=html.fromstring(open(p,'rb').read())
    for x in d.xpath('//script|//style|//nav|//header|//footer'):
        if x.getparent() is not None: x.getparent().remove(x)
    t=re.sub(r'\s+',' ',d.text_content().replace('\xa0',' '))
    t=re.sub(r'\d+ \| 20\d\d Form 10-[KQ]\s*',' ',t); t=re.sub(r'20\d\d Form 10-[KQ] \| \d+\s*',' ',t)
    return t
ABBR=['U.S.','U.K.','e.g.','i.e.','Inc.','Ltd.','Co.','No.','vs.','approx.']
def sents(t):
    for i,a in enumerate(ABBR): t=t.replace(a,f'@@{i}@@')
    t=re.sub(r'(?<=[a-z0-9%\)\]“”"’]\.)(?=[A-Z])',' ',t)   # joined sentences
    ss=re.split(r'(?<=[.!?])\s+(?=[A-Z“"(])',t)
    out=[]
    for s in ss:
        for i,a in enumerate(ABBR): s=s.replace(f'@@{i}@@',a)
        out.append(s.strip())
    return out
TAGS=[('loyalty',r'loyalty|Allē|\bAlle\b|rewards'),
 ('inventory',r'destock|stocking|inventory|timing of|phasing|buy-in|ordering patterns'),
 ('price_promo',r'pricing|\bprice|promotion|discount|rebate|incentive|gross-to-net'),
 ('share',r'market share|share gain|share loss|lower share|gain(?:ed|ing)? share|competit|outperform'),
 ('volume',r'\bvolumes?\b|units sold'),
 ('demand',r'demand|softness|soft market|consumer spending|consumer confidence|economic|macro|market (?:growth|environment)|penetrat|GLP'),
 ('launch',r'launch|approval|ramp|new product'),
 ('covid',r'COVID|pandemic|closure|reopen|shutdown|lockdown'),
 ('fx',r'foreign (?:currency|exchange)|\bFX\b|currency (?:headwind|tailwind)'),
 ('tariff',r'tariff')]
def tags(s):
    f=[]
    for tg,pat in TAGS:
        m=re.search(pat,s,re.I)
        if m: f.append((m.start(),tg))
    f.sort(); return [t for _,t in f]
def prod(s):
    for pat,p in [(r'Botox.{0,3} Cosmetic','Botox Cosmetic'),(r'Juvederm','Juvederm Collection'),(r'Other Aesthetics','Other Aesthetics'),(r'Jeuveau','Jeuveau'),(r'Evolysse','Evolysse'),
                  (r'Neuromodulator|Dysport|Relfydess','Neuromodulators'),(r'Fillers|Biostimulator|Restylane|Sculptra','Fillers & Biostimulators'),(r'Injectable Aesthetics','Injectable Aesthetics'),(r'(?i)aesthetic','Aesthetics (general)')]:
        if re.search(pat,s): return p
    return None
def region(s):
    us=bool(re.search(r'United States|U\.S\.|\bUS\b',s)); intl=bool(re.search(r'Internationally|International|outside the U|Europe|China|Canada',s))
    return 'US' if us and not intl else ('International' if intl and not us else ('US and International' if us and intl else 'Global/unspecified'))
def quote(s,tg):
    w=s.split()
    if len(w)<=38: return s
    pat=None
    for t_,p in TAGS:
        if t_==(tg[0] if tg else None): pat=p
    i=0
    if pat:
        m=re.search(pat,s,re.I)
        if m: i=len(s[:m.start()].split())
    a=max(0,i-14); b=min(len(w),a+37)
    return ('… ' if a>0 else '')+' '.join(w[a:b])+(' …' if b<len(w) else '')
rows=[]
def add(q,period,co,s,url,filt):
    tg=tags(s)
    if not tg: return
    rows.append(dict(quarter=q,period=period,company=co,product=prod(s) or '',region=region(s),primary_driver=tg[0],driver_tags=', '.join(tg),quote=quote(s,tg),source_url=url))
F=json.load(open('filings.json'))
CIK={'abbvie':'1551152','allergan':'1578845','evolus':'1570562'}
def ql(rd): y,m=rd[:4],rd[5:7]; return f"{y}Q{(int(m)-1)//3+1}"
CH=r'(increase[ds]?|decrease[ds]?|grew|growth|declin|favorabl|unfavorabl|primarily (?:driven|due|attribut)|higher|lower|reflect)'
for co in ('allergan','abbvie','evolus'):
    for form,acc,rd,fd,doc in F[co]:
        if rd<'2019-03-31': continue
        p=f"cache/{co}_{rd}_{form}.htm"
        url=f"https://www.sec.gov/Archives/edgar/data/{CIK[co]}/{acc.replace('-','')}/{doc}"
        t=text(p); seen=set()
        for s in sents(t):
            if len(s)>900 or len(s)<40 or s in seen: continue
            if co in('abbvie','allergan'):
                ok=re.search(r'Botox.{0,3} Cosmetics?|Juvederm|Other Aesthetics|Facial Aesthetics|Medical Aesthetics',s) and re.search(r'net revenues|revenues|sales',s,re.I) and re.search(CH,s) and not re.search(r'(?i)risk|could|may be|forward-looking|estimated|competitors? (?:may|could)|expects|Elahere|Skyrizi',s)
                if co=='abbvie' and form=='10-Q' and not re.search(r'(three|six|nine) months|year ended|2\d\d\d',s): ok=False
            else:
                ok=re.search(r'(?i)net revenues?(?: of Jeuveau.{0,12} sales)? (?:increased|decreased)|net revenues? (?:were|was) (?:flat|relatively)',s) and re.search(r'(?i)(three|six|nine) months|year ended|quarter',s) and re.search(r'(?i)primarily|due to|driven|attributable|resulting',s)
                ok=ok and not re.search(r'(?i)milestone|cash|losses|we expect|we anticipate|depend|if we|could|risk',s)
            if ok:
                yrs=[int(y) for y in re.findall(r'(20\d\d)',s)]
                if co=='evolus':
                    m_=re.search(r'ended \w+ \d+, (20\d\d)',s)
                    if m_ and int(m_.group(1))!=int(rd[:4]): ok=False
                elif co=='abbvie' and yrs and max(yrs)!=int(rd[:4]): ok=False
            if ok:
                seen.add(s)
                per='FY' if form=='10-K' else ('3M' if rd[5:7]=='03' else '3M/YTD')
                add(ql(rd),per,'AbbVie' if co=='abbvie' else ('Allergan plc' if co=='allergan' else 'Evolus'),s,url,None)
# Galderma
sys.path.insert(0,'.')
from build_galderma import URL as GU
GM={'Q12024':'2024Q1','H12024':'2024Q2','9M2024':'2024Q3','FY2024':'2024Q4','Q12025':'2025Q1','H12025':'2025Q2','9M2025':'2025Q3','FY2025':'2025Q4','Q12026':'2026Q1','H12026':'2026Q2','9M2026':'2026Q3'}
for k,q in GM.items():
    t=text(f'cache/galderma/{k}.html'); seen=set(); cand=[]
    for s in sents(t):
        if len(s)>800 or len(s)<50 or s in seen: continue
        if re.search(r'Neuromodulator|Fillers|Biostimulator|Injectable Aesthetics|Dysport|Relfydess|Sculptra|Restylane',s) and re.search(r'growth|grew|growing|declin|softness|share|phasing|base|demand|launch|promotional|impact|driven|benefit',s,re.I) and not re.search(r'(?i)forward-looking|guidance|investor|webcast|is a leader|pipeline',s):
            tg_=tags(s)
            if not set(tg_)&{'share','demand','inventory','price_promo','launch','volume','tariff','covid'}: continue
            if not re.search(r'(?i)neuromodulator|filler|biostimulator|injectable',s[:200]): continue
            seen.add(s); cand.append(s)
    cand.sort(key=lambda x:-len(set(tags(x))&{'share','demand','inventory','price_promo','volume','tariff'}))
    for s in cand[:7]:
        add(q,'3M' if k.startswith('Q1') else ('H1' if k.startswith('H1') else ('9M' if k.startswith('9M') else 'FY')),'Galderma',s,GU[k],None)
df=pd.DataFrame(rows)
df.to_pickle('commentary_raw.pkl')
print(df.groupby('company').size()); print(len(df))
print(df.groupby(['company','quarter']).size().unstack(0).fillna(0).astype(int).to_string())
