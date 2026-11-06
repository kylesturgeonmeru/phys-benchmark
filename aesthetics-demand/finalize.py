import sys; sys.path.insert(0,'.')
import pandas as pd, numpy as np, json, datetime as dt
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
exec(open('build_index.py').read().split("out=ix[[")[0].replace("pd.set_option","(lambda *a,**k:None)"))  # reuse ab, ev, gd, ix, qs, est rows
com=pd.read_pickle('commentary_raw.pkl')
# ---------------- raw_by_company
raw=[]
for _,r in ab.iterrows():
    raw.append(dict(company=r.company,quarter=r.quarter,category='Toxin' if r['product']=='Botox Cosmetic' else ('Filler' if r['product'].startswith('Juv') else 'Other aesthetics'),product=r['product'],region=r.region.replace('Intl','International'),metric='Net revenue',value_usd_m=r.revenue_usd_m,cc_growth_pct=None,basis=r.basis,estimate_method=r.get('note',''),source_url=r.source_url))
for q,r in ev.set_index('quarter').iterrows():
    for prod,cat,val in [('Total net revenues','Total',r.total_net_revenue),('Jeuveau (toxin; = product revenue before Evolysse split)','Toxin',r.toxin_jeuveau),('Evolysse','Filler',r.filler_evolysse)]:
        raw.append(dict(company='Evolus',quarter=q,category=cat,product=prod,region='Total (US-weighted; international about 2% 2022, 3% 2023, 5% 2024)',metric='Net revenue',value_usd_m=round(val,3),cc_growth_pct=None,basis=r.basis,estimate_method='',source_url=r.source_url))
for q,r in gd.set_index('quarter').iterrows():
    for prod,cat,val,cc in [('Injectable Aesthetics','Total injectables',r.inj_aesthetics,r.inj_cc_growth_pct),('Neuromodulators','Toxin',r.neuromodulators,r.neuro_cc_growth_pct),('Fillers & Biostimulators','Filler',r.fillers_biostim,r.fill_cc_growth_pct)]:
        raw.append(dict(company='Galderma',quarter=q,category=cat,product=prod,region='Global (category US/International split not reported)',metric='Net sales',value_usd_m=val,cc_growth_pct=None if pd.isna(cc) else cc,basis=r.basis,estimate_method='',source_url=r.source_url))
    for prod,val in [('Group total, U.S.',r.group_us),('Group total, International',r.group_intl),('Nemluvio (Therapeutic Dermatology, used in US estimate)',r.nemluvio_net_sales)]:
        raw.append(dict(company='Galderma',quarter=q,category='Group context',product=prod,region='U.S.' if 'U.S.' in prod else ('International' if 'Intl' in prod or 'International' in prod else 'Global'),metric='Net sales',value_usd_m=val,cc_growth_pct=None,basis='reported (Nemluvio quarterly split derived from YTD disclosures; 2024 split assumed)' if 'Nemluvio' in prod else r.basis,estimate_method='',source_url=r.source_url))
    for prod,cat,val in [('Neuromodulators, US (estimate)','Toxin',r.est_us_neuromodulators),('Fillers & Biostimulators, US (estimate)','Filler',r.est_us_fillers_biostim)]:
        raw.append(dict(company='Galderma',quarter=q,category=cat,product=prod,region='U.S. (estimated)',metric='Net sales',value_usd_m=val,cc_growth_pct=None,basis='ESTIMATED',estimate_method=r.est_method+f' US share of injectables used: {r.est_us_share_of_inj:.1%}. Nemluvio assumed 90% US.',source_url=r.source_url))
raw=pd.DataFrame(raw)
raw['_o']=raw.company.map({'Allergan plc':0,'AbbVie':0,'Evolus':1,'Galderma':2}); raw=raw.sort_values(['_o','company','category','product','region','quarter']).drop(columns='_o')
# ---------------- commentary
com=com.sort_values(['quarter','company','product']).reset_index(drop=True)
com['words']=com.quote.str.replace('…','').str.split().str.len()
assert com.words.max()<40, com.words.max()
comlog=com.rename(columns={'primary_driver':'driver_tag','driver_tags':'all_driver_tags'})[['quarter','period','company','product','region','driver_tag','all_driver_tags','quote','source_url']]
# ---------------- price vs volume
V,P,S,I='mostly volume','mostly price or promotions','mostly share shift','mostly inventory timing'
pv={ # quarter: (toxin call, conf, toxin why, filler call, conf, filler why)
}
def setq(qlist,t,tc,tw,f,fc,fw):
    for q in qlist: pv[q]=(t,tc,tw,f,fc,fw)
setq(['2019Q1','2019Q2','2019Q3','2019Q4'],V,'Low','Allergan FY2019 10-K: Botox Cosmetics growth from demand growth and higher average prices; demand is the larger part.',V,'Low','Allergan FY2019 10-K: Juvederm growth from demand growth.')
setq(['2020Q1'],V,'High','Allergan Q1 2020 10-Q: COVID-19 closures from mid-March; US Botox Cosmetics -7%.',V,'High','Same; US Juvederm -17% as practices closed.')
setq(['2020Q2'],V,'High','Practice closures April to early May, reopening from May. Q2 is an estimate (AbbVie reported a stub).',V,'High','Same; filler more elective, deeper hole.')
setq(['2020Q3','2020Q4'],V,'Medium','Reopening; toxin back to 2019 level by Q3. No price commentary.',V,'Medium','Filler still below 2019 as patients prioritised toxin after reopening.')
setq(['2021Q1','2021Q2','2021Q3','2021Q4'],V,'High','AbbVie 10-Q/10-K: increased brand investment and strong recovery from COVID-19 (volume rebound).',V,'High','Same filings; Q2 2021 YoY is distorted by the closed Q2 2020 base.')
setq(['2022Q1','2022Q2'],V,'Medium','AbbVie: increased consumer demand and penetration, targeted brand investment.',V,'Medium','AbbVie Q1 2022: demand and penetration; Q2 2022 US Juvederm down vs a very high 2021 base.')
setq(['2022Q3','2022Q4'],V,'Medium','AbbVie: US market growth moderated by economic pressure on discretionary spend.',P,'Low','AbbVie FY2022: Juvederm hit by economic pressure and increased pricing promotions; US down 21% to 29% YoY. Volume and promotions are hard to separate.')
setq(['2023Q1','2023Q2'],V,'Medium','AbbVie: decreased US consumer demand and some unfavorable pricing, due to economic pressure on discretionary spending.',V,'Medium','AbbVie: US Juvederm down on decreased consumer demand from economic pressure.')
setq(['2023Q3','2023Q4'],V,'Medium','AbbVie: US demand up on recovery in the toxin market.',V,'Low','AbbVie: demand down, partly offset by new product launches (Q4 US Juvederm +22% looks launch and phasing assisted).')
setq(['2024Q1'],I,'High','AbbVie Q1 2024: US decline due to timing of customer inventory destocking.',I,'High','AbbVie Q1 2024: destocking in the United States.')
setq(['2024Q2'],P,'Medium','AbbVie Q2 2024: favorable pricing and increased consumer demand (US +7%).',S,'Medium','AbbVie Q2 2024: US Juvederm +10% on market share uptake.')
setq(['2024Q3'],P,'Medium','AbbVie Q3 2024: favorable pricing drove the increase.',V,'Low','AbbVie cites decreased consumer demand (international named). US call is inferred.')
setq(['2024Q4'],V,'Low','No Q4 text. FY2024 lists favorable pricing offset by destocking and lower demand; Q4 US -5% read as softer demand.',V,'Low','FY2024: decreased consumer demand and destocking; Q4 US -23%.')
setq(['2025Q1'],P,'High','AbbVie Q1 2025: US -24% on unfavorable pricing from consumer loyalty program changes and lower share.',V,'Medium','AbbVie: decreased global consumer demand plus unfavorable pricing from US loyalty changes. Demand named first; price is a real second.')
setq(['2025Q2'],S,'High','AbbVie Q2 2025: US -9% on lower market share and decreased demand. Galderma and Evolus gained share.',V,'High','AbbVie: decreased global consumer demand. Galderma: filler market soft, intense promotions.')
setq(['2025Q3'],P,'Medium','AbbVie Q3 2025: unfavorable pricing from loyalty changes, lower share, lower demand, offset by prior-year destocking.',V,'Medium','AbbVie: decreased global demand, offset by prior-year destocking. Galderma: soft filler market with promotions.')
setq(['2025Q4'],P,'Low','AbbVie FY2025: loyalty-driven pricing, lower share, lower demand, offset by prior-year destocking. Quarter itself is near flat.',V,'Medium','AbbVie FY2025: decreased consumer demand. Galderma Q4: filler pricing pressure and aggressive mid-face promotions.')
setq(['2026Q1'],I,'Medium','AbbVie Q1 2026: favorable pricing from lapping the loyalty changes plus timing of customer stocking. Galderma: favorable US phasing in Q1.',I,'Medium','AbbVie and Galderma both cite stocking or phasing and lapping of 2025 loyalty pricing, against lower consumer demand.')
setq(['2026Q2'],I,'Low','Galderma: US phasing from Q1 unwound in Q2. AbbVie US -2%, no US driver given.',V,'Medium','AbbVie: decreased consumer demand and unfavorable pricing.')
setq(['2026Q3'],S,'Low','AbbVie US +2% with no US driver given; Galderma and Evolus (Jeuveau +10%) growing faster, so share movement is a better read than market growth.',V,'Medium','AbbVie: decreased consumer demand and unfavorable pricing. Galderma filler growth slowed to +4.8% cc.')
pvdf=pd.DataFrame([dict(quarter=q,us_toxin_call=v[0],toxin_confidence=v[1],toxin_rationale=v[2],us_filler_call=v[3],filler_confidence=v[4],filler_rationale=v[5]) for q,v in pv.items()]).sort_values('quarter')
# ---------------- events
EV=[
('2019-02-01','Jeuveau (Evolus) FDA approval; commercial launch May 2019','Launch','Evolus 10-K FY2019 and 10-Qs (filing)'),
('2020-03-15','COVID-19 closures: US practices close elective procedures (mid-March, state by state)','COVID','Allergan Q1 2020 10-Q expects significant Q2 decline (filing). Exact dates vary by state, from public record'),
('2020-05-08','AbbVie completes Allergan acquisition (Q2 2020 AbbVie figures are a stub)','Corporate','AbbVie Q2 2020 10-Q (filing)'),
('2020-06-01','Reopening begins, staggered by state through mid-2020','COVID','Public record; Evolus and AbbVie filings describe recovery in 2021'),
('2021-04-01','2021 rebound: strong recovery from COVID plus brand investment; Q2 2021 YoY above 100%','Demand','AbbVie 10-Q Q2 2021 (filing)'),
('2021-06-04','Wegovy (semaglutide) launched in US for weight management; start of GLP-1 ramp','GLP-1','Public record, not re-verified in this session'),
('2022-03-16','Fed begins rate hikes (first 25 bp move)','Macro','Public record'),
('2022-09-07','Daxxify (Revance) FDA approval for glabellar lines; launched late 2022','Launch','Public record, not re-verified in this session; Revance optional pull not done'),
('2022-05-13','Mounjaro (tirzepatide) FDA approval; GLP-1 ramp accelerates','GLP-1','Public record, not re-verified in this session'),
('2023-07-26','Last Fed hike of the cycle (5.25% to 5.50%)','Macro','Public record'),
('2023-11-08','Zepbound (tirzepatide) approved for weight loss; GLP-1 demand and supply constrained through 2024','GLP-1','Public record, not re-verified in this session'),
('2025-01-01','AbbVie consumer loyalty program changes weigh on US Botox Cosmetic and Juvederm pricing (Q1 2025 first cited; exact effective date not stated in 10-Q)','Loyalty program','AbbVie 10-Q Q1 2025 (filing)'),
('2025-01-15','Southern California wildfires temporarily hit Galderma sales','Other','Galderma Q1 2025 release (company)'),
('2025-02-01','Relfydess (Galderma liquid neuromodulator) approvals roll out: 15 European markets, Switzerland, Australia, UK by Q1 2025 release','Launch','Galderma Q1 2025 release (company). US BLA received a Complete Response Letter in June 2026 per Q3 2026 release'),
('2025-05-15','Evolysse Form and Smooth US commercial launch (first revenue Q2 2025); FDA approval 2025','Launch','Evolus 10-Q Q2 2025 (filing); approval year from Evolus 10-K FY2025'),
('2025-04-15','US tariff assumptions (15% on Restylane and Sculptra imports) enter Galderma guidance','Policy','Galderma Q1 2026 release (company)'),
('2026-06-15','Galderma receives FDA Complete Response Letter for RelabotulinumtoxinA; plans resubmission Q1 2027','Launch','Galderma Q3 2026 release (company)'),
]
events=pd.DataFrame(EV,columns=['date','event','type','source_or_evidence']).sort_values('date')
# ---------------- sources
F=json.load(open('filings.json')); CIK={'abbvie':'AbbVie 10-Q/10-K','allergan':'Allergan plc 10-Q/10-K','evolus':'Evolus 10-Q/10-K'}
src=[]
for co,rows in F.items():
    for form,acc,rd,fd,doc in rows:
        if rd<'2019-03-31' and not (rd=='2018-12-31' and False): continue
        cik={'abbvie':'1551152','allergan':'1578845','evolus':'1570562'}[co]
        src.append(dict(company=co.capitalize() if co!='abbvie' else 'AbbVie',document=form,period_end=rd,filed=fd,url=f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-','')}/{doc}",used_for='Product revenue tables (HTML parsed) and MD&A commentary'))
src.append(dict(company='AbbVie',document='8-K ex. 99.1 (Q2 2021 earnings release)',period_end='2021-06-30',filed='2021-07-30',url=PR,used_for='Comparable-basis H1 2021 growth, used to estimate full-quarter Q2 2020'))
for k,u in __import__('build_galderma').URL.items():
    src.append(dict(company='Galderma',document=f'Results release {k}',period_end='',filed='',url=u,used_for='Category net sales, group US/International, constant-currency growth, commentary'))
src=pd.DataFrame(src)
notes=pd.DataFrame({'method_note':[
 'All SEC requests sent User-Agent "MERU research kyle@wearemeru.com" at under 10 requests per second.',
 'AbbVie Q4 and Allergan Q4 are 10-K full year less the 9M YTD in the Q3 10-Q. Reclassifications between filings can introduce small errors.',
 'AbbVie Q2 2020 covers only 8 May to 30 Jun. Full quarter is estimated from comparable-basis growth. Other Aesthetics before Q2 2020 is Allergan Total Medical Aesthetics less Botox Cosmetics less Juvederm, not exactly comparable.',
 'Galderma Q2 and Q3 2023 are derived from H1 and 9M comparative columns in the 2024 releases. Galderma 2023 constant-currency growth by quarter and Q2/Q3 2024 quarterly cc growth are not in the tables, left blank.',
 'Galderma does not report US versus International by category. US neuromodulators and fillers are estimated as: (group US less 90% of Nemluvio) x (Injectable Aesthetics share of group sales ex Nemluvio), split by global neuromodulator/filler mix. Group US is the only US figure Galderma reports.',
 'Evolus toxin includes international sales (about 2% of revenue 2022, 3% 2023, 5% 2024 per the FY2024 10-K country table; later years not parsed). Evolus quarterly Evolysse starts Q2 2025.',
 'Full index: AbbVie plus Evolus only through 2023Q4. From 2024Q1 each quarter equals the prior-year full index times YoY growth of the composite that includes Galderma, so the series has no level break.',
 'Not done (optional, out of time box): Revance (Daxxify, RHA) and BeautyHealth (Hydrafacial). Merz and other private players are excluded. Event dates marked "public record" were not re-verified in this session.']})
# ---------------- chart
def qmid(q): y=int(q[:4]); n=int(q[5]); return dt.date(y,3*(n-1)+2,15)
X=[qmid(q) for q in qs]
fig,ax=plt.subplots(figsize=(14,7.2),dpi=160)
blue,orange,ink,mut='#2a78d6','#eb6834','#0b0b0b','#52514e'
ax.plot(X,ix.tox_full_index,color=blue,lw=2.2,label='Neurotoxin index (full)',marker='o',ms=3.5)
ax.plot(X,ix.fil_full_index,color=orange,lw=2.2,label='Filler index (full)',marker='o',ms=3.5)
ax.plot(X,ix.tox_AE_index,color=blue,lw=1.1,ls=(0,(2,2)),alpha=.8,label='Neurotoxin, AbbVie + Evolus only')
ax.plot(X,ix.fil_AE_index,color=orange,lw=1.1,ls=(0,(2,2)),alpha=.8,label='Filler, AbbVie + Evolus only')
ax.set_ylim(0,260); ax.set_ylabel('Index, 2019 average = 100',color=mut)
ev_chart=[('2020-03-15','COVID closures'),('2020-06-01','Reopening'),('2021-04-01','2021 rebound'),('2022-03-16','Rate hikes begin'),('2022-09-07','Daxxify approved'),('2023-07-26','Last rate hike'),('2023-11-08','Zepbound (GLP-1 ramp)'),('2025-01-01','AbbVie loyalty changes'),('2025-05-15','Evolysse US launch'),('2025-02-01','Relfydess approvals')]
hts=[250,238,226]
for i,(d,l) in enumerate(ev_chart):
    x=dt.date.fromisoformat(d); ax.axvline(x,color='#8a8984',lw=.9,ls='-',alpha=.8,zorder=0)
    ax.text(x,hts[i%3],' '+l,fontsize=8.5,color=ink,va='center',ha='left',bbox=dict(boxstyle='round,pad=0.15',fc='#fcfcfb',ec='none',alpha=.85))
for y in range(2019,2027): pass
ax.set_xlim(dt.date(2019,1,1),dt.date(2026,12,31))
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
for s in('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',color='#e6e5e1',lw=.8); ax.tick_params(colors=mut)
ax.text(X[-1],ix.tox_full_index.iloc[-1]+7,f"{ix.tox_full_index.iloc[-1]:.0f}",color=blue,fontsize=9,ha='center')
ax.text(X[-1],ix.fil_full_index.iloc[-1]+7,f"{ix.fil_full_index.iloc[-1]:.0f}",color=orange,fontsize=9,ha='center')
ax.legend(loc='lower left',frameon=False,fontsize=9,ncol=2,bbox_to_anchor=(0.0,0.0))
ax.set_title('US aesthetics sell-in index by quarter, Q1 2019 to Q3 2026',loc='left',fontsize=13,color=ink,pad=14)
fig.text(0.01,0.005,'Manufacturer sell-in, US. AbbVie/Allergan + Evolus + Galderma (US estimated). Galderma included from 2023; Q2 2020 AbbVie estimated. Merz and private players excluded.',fontsize=8,color=mut)
fig.tight_layout(rect=(0,0.02,1,1)); fig.savefig('aesthetics_demand_index.png',facecolor='#fcfcfb'); 
# ---------------- workbook
idx=ix.reset_index()[['quarter','abbv_us_botox_cosmetic','evolus_toxin_jeuveau','galderma_us_neuro_est','tox_AE_usd','tox_full_usd','tox_AE_index','tox_AE_yoy_pct','tox_full_index','tox_full_yoy_pct','tox_gap_index_pts','abbv_us_juvederm','evolus_filler_evolysse','galderma_us_filler_est','fil_AE_usd','fil_full_usd','fil_AE_index','fil_AE_yoy_pct','fil_full_index','fil_full_yoy_pct','fil_gap_index_pts','estimate_flags']].round(2)
idx.columns=['quarter','AbbVie US Botox Cosmetic $M','Evolus toxin $M','Galderma US neuromodulators $M (ESTIMATE)','Toxin $M AbbVie+Evolus','Toxin $M incl. Galderma (2023+)','Toxin index AbbVie+Evolus (2019 avg=100)','Toxin YoY % AbbVie+Evolus','Toxin index full (chained)','Toxin YoY % full','Toxin gap, full minus AE-only (index pts)','AbbVie US Juvederm $M','Evolus Evolysse $M','Galderma US fillers & biostim $M (ESTIMATE)','Filler $M AbbVie+Evolus','Filler $M incl. Galderma (2023+)','Filler index AbbVie+Evolus (2019 avg=100)','Filler YoY % AbbVie+Evolus','Filler index full (chained)','Filler YoY % full','Filler gap, full minus AE-only (index pts)','Estimates and method']
with pd.ExcelWriter('aesthetics_demand.xlsx',engine='openpyxl') as xw:
    raw.to_excel(xw,sheet_name='raw_by_company',index=False); idx.to_excel(xw,sheet_name='index',index=False); comlog.to_excel(xw,sheet_name='commentary_log',index=False)
    pvdf.to_excel(xw,sheet_name='price_vs_volume',index=False); events.to_excel(xw,sheet_name='events',index=False)
    src.to_excel(xw,sheet_name='sources',index=False); notes.to_excel(xw,sheet_name='sources',index=False,startrow=len(src)+3)
    from openpyxl.styles import Font,Alignment,PatternFill
    for ws in xw.book.worksheets:
        ws.freeze_panes='B2'
        for c in ws[1]: c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='1F3A5F'); c.alignment=Alignment(wrap_text=True,vertical='top')
        for col in ws.columns:
            L=max((len(str(c.value)) if c.value is not None else 0) for c in col[:60]); ws.column_dimensions[col[0].column_letter].width=min(60,max(10,L+2))
        if ws.title in('commentary_log','price_vs_volume','events','index'):
            for row in ws.iter_rows(min_row=2):
                for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
pvdf.to_pickle('pv.pkl'); print('ok',len(raw),len(comlog),len(pvdf),len(events),len(src))
