import requests,json,time,os
H={"User-Agent":"MERU research kyle@wearemeru.com"}
F=json.load(open('filings.json'))
CIK={"abbvie":"1551152","allergan":"1578845","evolus":"1570562"}
for co,rows in F.items():
    for form,acc,rd,fd,doc in rows:
        p=f"cache/{co}_{rd}_{form}.htm"
        if os.path.exists(p): continue
        u=f"https://www.sec.gov/Archives/edgar/data/{CIK[co]}/{acc.replace('-','')}/{doc}"
        r=requests.get(u,headers=H,timeout=60)
        if r.status_code!=200: print('FAIL',u,r.status_code);continue
        open(p,'wb').write(r.content);time.sleep(.3)
        print(p,len(r.content))
