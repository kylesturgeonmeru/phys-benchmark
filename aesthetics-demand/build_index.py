import pandas as pd, numpy as np, json, pickle
pd.set_option('display.width',250,'display.max_columns',40)
ab=pd.read_pickle('abbvie_long.pkl'); ev=pd.read_pickle('evolus_q.pkl'); gd=pd.read_pickle('galderma_q.pkl')
qs=[f"{y}Q{q}" for y in range(2019,2027) for q in range(1,5)][:-1]   # to 2026Q3
# ---------- Q2 2020 full-quarter estimate (AbbVie reports only 8 May-30 Jun)
PR='https://www.sec.gov/Archives/edgar/data/1551152/000155115221000021/abbv-20210630xexhibit991.htm'
a=ab.set_index(['quarter','product','region']).revenue_usd_m
H1_2021={('Botox Cosmetic','US'):(671,0.840),('Botox Cosmetic','Intl'):(390,0.837),('Juvederm Collection','US'):(319,0.918),('Other Aesthetics','US'):(663,0.499)}
est={}
for (p,g),(h1,gr) in H1_2021.items():
    est[(p,g)]=h1/(1+gr)-a[('2020Q1',p,g)]
ratio=est[('Botox Cosmetic','Intl')]/a[('2020Q2','Botox Cosmetic','Intl')]
for (p,g) in [('Juvederm Collection','Intl'),('Other Aesthetics','Intl')]:
    est[(p,g)]=a[('2020Q2',p,g)]*ratio
estrows=[]
for (p,g),v in est.items():
    meth=('Full-quarter Q2 2020 = H1 2021 reported / (1 + H1 2021 growth on comparable operational basis, AbbVie 8-K ex. 99.1 of 30 Jul 2021) less Allergan Q1 2020 (10-Q). ' if (p,g) in H1_2021 else 'Stub value scaled by the full-quarter/stub ratio of international Botox Cosmetic (comparable-basis growth not disclosed for this line). ')
    estrows.append(dict(company='AbbVie',quarter='2020Q2',product=p,region=g,revenue_usd_m=round(v,1),basis='ESTIMATED full quarter',source_url=PR,note=meth+'AbbVie reported only the 8 May to 30 Jun stub for Q2 2020.'))
ab=pd.concat([ab,pd.DataFrame(estrows)],ignore_index=True)
ab['est']=ab.basis.str.startswith('ESTIMATED')
def abv(q,p,g):
    s=ab[(ab.quarter==q)&(ab['product']==p)&(ab.region==g)]
    if (s.est).any(): s=s[s.est]
    elif q=='2020Q2': s=s
    return float(s.revenue_usd_m.iloc[0])
E=ev.set_index('quarter'); G=gd.set_index('quarter')
rows=[]
for q in qs:
    r=dict(quarter=q)
    r['abbv_us_botox_cosmetic']=abv(q,'Botox Cosmetic','US'); r['abbv_us_juvederm']=abv(q,'Juvederm Collection','US')
    r['evolus_toxin_jeuveau']=E.loc[q,'toxin_jeuveau']; r['evolus_filler_evolysse']=E.loc[q,'filler_evolysse']
    r['galderma_us_neuro_est']=G.loc[q,'est_us_neuromodulators'] if q in G.index else np.nan
    r['galderma_us_filler_est']=G.loc[q,'est_us_fillers_biostim'] if q in G.index else np.nan
    rows.append(r)
ix=pd.DataFrame(rows).set_index('quarter')
for k,(a1,e1,g1) in {'tox':('abbv_us_botox_cosmetic','evolus_toxin_jeuveau','galderma_us_neuro_est'),'fil':('abbv_us_juvederm','evolus_filler_evolysse','galderma_us_filler_est')}.items():
    ix[f'{k}_AE_usd']=ix[a1]+ix[e1]
    ix[f'{k}_full_usd']=ix[a1]+ix[e1]+ix[g1]
    base=ix.loc[[x for x in qs if x.startswith('2019')],f'{k}_AE_usd'].mean()
    ix[f'{k}_AE_index']=ix[f'{k}_AE_usd']/base*100
    full=ix[f'{k}_AE_index'].copy()
    for i,q in enumerate(qs):
        if q>='2024Q1': full[q]=full[qs[i-4]]*ix.loc[q,f'{k}_full_usd']/ix.loc[qs[i-4],f'{k}_full_usd']
    ix[f'{k}_full_index']=full
    for v in('AE','full'):
        ix[f'{k}_{v}_yoy_pct']=[ (ix.loc[q,f'{k}_{v}_index']/ix.loc[qs[i-4],f'{k}_{v}_index']-1)*100 if i>=4 else np.nan for i,q in enumerate(qs)]
    ix[f'{k}_gap_index_pts']=ix[f'{k}_full_index']-ix[f'{k}_AE_index']
ix['estimate_flags']=''
for q in qs:
    f=[]
    if q=='2020Q2': f.append('AbbVie Q2 2020 full quarter estimated (stub reported only); see raw_by_company')
    if q>='2023Q1': f.append('Galderma US neuromodulators/fillers estimated (Galderma does not report US by category)')
    if q in('2023Q2','2023Q3'): f.append('Galderma Q2/Q3 2023 derived from H1/9M comparatives')
    if q>='2024Q1': f.append('Full index = prior-year full index x YoY growth of the composite that includes Galderma')
    if q<='2023Q4': f.append('Full index equals AbbVie+Evolus index (no Galderma data before 2023)')
    if q<='2019Q4' and q.startswith('2019'): f.append('2019 quarters from Allergan plc 10-Qs/10-K (pre-acquisition)')
    f.append('Evolus toxin includes small international sales (2% 2022, 3% 2023, 5% 2024 of revenue)') if q>='2022Q1' else None
    ix.loc[q,'estimate_flags']='; '.join([x for x in f if x])
ix.to_pickle('index.pkl')
out=ix[['tox_AE_usd','tox_full_usd','tox_AE_index','tox_full_index','tox_AE_yoy_pct','tox_full_yoy_pct','fil_AE_usd','fil_full_usd','fil_AE_index','fil_full_index','fil_AE_yoy_pct','fil_full_yoy_pct']].round(1)
print(out.to_string())
def fy(col,y): return ix.loc[[q for q in qs if q.startswith(str(y))],col].sum()
for k in('tox','fil'):
    print(k,'FY24->25 full usd %.1f%%'%((fy(f'{k}_full_usd',2025)/fy(f'{k}_full_usd',2024)-1)*100),'AE %.1f%%'%((fy(f'{k}_AE_usd',2025)/fy(f'{k}_AE_usd',2024)-1)*100))
    for v in('full','AE'):
        m=lambda y:ix.loc[[q for q in qs if q.startswith(str(y))],f'{k}_{v}_index'].mean()
        print(k,v,'avg index 2023 %.1f 2024 %.1f 2025 %.1f; 24->25 %.1f%%; 23->25 %.1f%%'%(m(2023),m(2024),m(2025),(m(2025)/m(2024)-1)*100,(m(2025)/m(2023)-1)*100))
    ytd=lambda y,col:ix.loc[[f'{y}Q1',f'{y}Q2',f'{y}Q3'],col].sum()
    print(k,'YTD26 vs YTD25 full %.1f%% AE %.1f%%'%((ytd(2026,f'{k}_full_usd')/ytd(2025,f'{k}_full_usd')-1)*100,(ytd(2026,f'{k}_AE_usd')/ytd(2025,f'{k}_AE_usd')-1)*100))
    print(k,'min yoy full',ix[f'{k}_full_yoy_pct'].loc['2024Q1':].min(),ix[f'{k}_full_yoy_pct'].loc['2024Q1':].idxmin(), 'gap mean abs 2024+',ix[f'{k}_gap_index_pts'].loc['2024Q1':].abs().mean(),'yoy gap ppt mean abs',(ix[f'{k}_full_yoy_pct']-ix[f'{k}_AE_yoy_pct']).loc['2024Q1':].abs().mean())
print('Q3 26 index',ix.loc['2026Q3',['tox_full_index','fil_full_index','tox_AE_index','fil_AE_index']].round(1).to_dict(),'peak',ix[['tox_full_index','fil_full_index']].max().round(1).to_dict(),ix[['tox_full_index','fil_full_index']].idxmax().to_dict())
