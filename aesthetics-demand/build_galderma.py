import re,sys,pickle
sys.path.insert(0,'.')
import pandas as pd
from lxml import html
from tbl import rows_of
from parse_abbvie import num
SLUG={'Q12024':'galderma-delivers-strong-start-year-record-net-sales-over-1-billion-usd-first-quarter-and-124','H12024':'galderma-delivers-record-net-sales-22-billion-usd-and-108-year-year-growth-constant-currency','9M2024':'galderma-delivers-record-net-sales-3259-b-usd-first-nine-months-2024-demonstrates-0','FY2024':'galderma.com/news/2024-annual-results','Q12025':'galderma-Q12025-performance','H12025':'galderma-H12025-performance','9M2025':'galderma-Q32025-performance','FY2025':'galderma-delivers-record-2025-results','Q12026':'galderma-Q12026-performance','H12026':'galderma-H12026-performance','9M2026':'galderma-reports-q3-2026-results-and-raises-full-year-guidance'}
URL={k:'https://www.galderma.com/news/'+v for k,v in SLUG.items()}
def tabs(k):
    d=html.fromstring(open(f'cache/galderma/{k}.html','rb').read()); out=[]
    for t in d.xpath('//table'):
        rs=rows_of(t)
        if not any(r[0].startswith('Group total') for r in rs): continue
        hdr=' '.join(' '.join(r) for r in rs[:2])
        o={}
        for r in rs:
            l=r[0].replace('Neuro- modulators','Neuromodulators')
            if l in('Group total','Injectable Aesthetics','Neuromodulators','Fillers & Biostimulators','International','U.S.') and len(r)>=3:
                o[l]=[num(x.replace('%','').replace(' ','')) for x in r[1:]]
        out.append((hdr,o))
    return out
def pick(k,pat):
    for h,o in tabs(k):
        if re.search(pat,h): return o
    raise KeyError((k,pat))
R={'Group total':'Group','Injectable Aesthetics':'Inj','Neuromodulators':'Neuro','Fillers & Biostimulators':'Fill','International':'Intl','U.S.':'US'}
Q={}   # quarter -> dict(name->(value,cc,basis,src))
def put(q,o,col,src,basis,cc=True):
    d=Q.setdefault(q,{})
    for l,s in R.items():
        v=o[l][col]; c=o[l][2] if cc and len(o[l])>2 else None
        d[s]=(v,c)
    d['_basis']=basis; d['_src']=src
t=pick('Q12024','First quarter'); put('2023Q1',t,0,URL['Q12024'],'reported (comparative column in Q1 2024 release)',cc=False); put('2024Q1',t,1,URL['Q12024'],'reported')
h1=pick('H12024','First half'); q1=Q['2023Q1']
Q['2023Q2']={s:(h1[l][0]-q1[s][0],None) for l,s in R.items()}; Q['2023Q2'].update(_basis='derived: H1 2023 (H1 2024 release comparative) less Q1 2023',_src=URL['H12024'])
m9=pick('9M2024','First 9'); 
Q['2023Q3']={s:(m9[l][0]-h1[l][0],None) for l,s in R.items()}; Q['2023Q3'].update(_basis='derived: 9M 2023 (9M 2024 release comparative) less H1 2023',_src=URL['9M2024'])
q4=pick('FY2024','Net sales Q4 2023'); put('2023Q4',q4,0,URL['FY2024'],'reported (comparative column in FY2024 release)',cc=False); put('2024Q4',q4,1,URL['FY2024'],'reported')
q2=pick('H12025','Q2 2024'); put('2024Q2',q2,0,URL['H12025'],'reported (comparative column in H1 2025 release)',cc=False); put('2025Q2',q2,1,URL['H12025'],'reported')
q3=pick('9M2025','Q3 2024'); put('2024Q3',q3,0,URL['9M2025'],'reported (comparative column in 9M 2025 release)',cc=False); put('2025Q3',q3,1,URL['9M2025'],'reported')
put('2025Q1',pick('Q12025','Q1 2024'),1,URL['Q12025'],'reported')
put('2025Q4',pick('FY2025','Q4 2024'),1,URL['FY2025'],'reported')
put('2026Q1',pick('Q12026','Q1 2025'),1,URL['Q12026'],'reported')
put('2026Q2',pick('H12026','Q2 2025'),1,URL['H12026'],'reported')
put('2026Q3',pick('9M2026','Q3 2025'),1,URL['9M2026'],'reported')
NEM={'2024Q3':0,'2024Q4':23,'2025Q1':39,'2025Q2':92,'2025Q3':132,'2025Q4':189,'2026Q1':185,'2026Q2':248,'2026Q3':302}
rows=[]
for q in sorted(Q):
    d=Q[q]; nem=NEM.get(q,0)
    us_exn=d['US'][0]-0.9*nem; grp_exn=d['Group'][0]-nem
    share=d['Inj'][0]/grp_exn
    us_inj=us_exn*share
    us_neuro=us_inj*d['Neuro'][0]/d['Inj'][0]; us_fill=us_inj*d['Fill'][0]/d['Inj'][0]
    rows.append(dict(company='Galderma',quarter=q,group_net_sales=d['Group'][0],inj_aesthetics=d['Inj'][0],neuromodulators=d['Neuro'][0],fillers_biostim=d['Fill'][0],
      inj_cc_growth_pct=d['Inj'][1],neuro_cc_growth_pct=d['Neuro'][1],fill_cc_growth_pct=d['Fill'][1],group_us=d['US'][0],group_intl=d['Intl'][0],
      nemluvio_net_sales=nem,est_us_share_of_inj=round(us_inj/d['Inj'][0],4),est_us_neuromodulators=round(us_neuro,1),est_us_fillers_biostim=round(us_fill,1),
      est_method='US group sales less 90% of Nemluvio, times Injectable Aesthetics share of group sales ex-Nemluvio; split neuro/filler by global mix. Galderma does not report US by category.',
      basis=d['_basis'],source_url=d['_src']))
g=pd.DataFrame(rows); g.to_pickle('galderma_q.pkl')
pd.set_option('display.width',300)
print(g.drop(columns=['est_method','source_url','basis']).to_string())
