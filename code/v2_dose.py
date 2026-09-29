import numpy as np,pandas as pd,statsmodels.api as sm,json
rng=np.random.default_rng(20260713)
df=pd.read_pickle('pixels_v2.pkl')
# UN Degree of Urbanisation: rural grid cells (SMOD 11) in 1995 and 2020, and no built-up growth
rural=(df.smod95==11)&(df.smod20==11)&(df.b1<0.01)&(df.nb<0.01)
df['rural']=rural
labs=['2-5','5-10','10-20','>=20']
df['grp']=np.where(rural,'rural',pd.cut(df.dbf,[0.02,0.05,0.10,0.20,1.0],labels=labs).astype(str))
df.loc[(df.smod95>=21)&(df.dbf<0.05),'grp']='established'
# also: UN classes by 2020
df['un']=np.select([df.smod20==30,df.smod20.isin([21,22,23]),df.smod20.isin([11,12,13])],['urban centre','urban cluster','rural'],'other')
blks=np.sort(df.blk.unique()); bi=np.searchsorted(blks,df.blk.values); nbk=len(blks); nd=6
W=rng.multinomial(nbk,np.ones(nbk)/nbk,size=2000).astype(float)
def SN(sel,var):
    S=np.zeros((nbk,nd));N=np.zeros((nbk,nd))
    np.add.at(S,(bi[sel],df.dbin.values[sel]),df[var].values[sel]); np.add.at(N,(bi[sel],df.dbin.values[sel]),1); return S,N
def dfrom(Su,Nu,Sr,Nr):
    ok=(Nu>0)&(Nr>0); w=np.where(ok,Nu,0.); w=w/w.sum(-1,keepdims=True)
    um=np.where(ok,Su/np.where(Nu>0,Nu,1),0); rm=np.where(ok,Sr/np.where(Nr>0,Nr,1),0)
    return (um*w).sum(-1)-(rm*w).sum(-1),(um*w).sum(-1),(rm*w).sum(-1)
def mdiff(sel,var):
    Su,Nu=SN(sel.values,var); Sr,Nr=SN(rural.values,var)
    e=dfrom(Su.sum(0),Nu.sum(0),Sr.sum(0),Nr.sum(0)); b=dfrom(W@Su,W@Nu,W@Sr,W@Nr)[0]
    return dict(diff=float(e[0]),urban=float(e[1]),rural=float(e[2]),lo=float(np.nanpercentile(b,2.5)),hi=float(np.nanpercentile(b,97.5)),n=int(sel.sum()))
rows=[]
for g in labs+['established']:
    for var in ['tn','td','en','ex']:
        r=mdiff(df.grp==g,var); r.update(group=g,var=var); rows.append(r)
for g in ['urban centre','urban cluster']:
    for var in ['tn','td','en','ex']:
        r=mdiff((df.un==g)&~rural,var); r.update(group=g,var=var); rows.append(r)
R=pd.DataFrame(rows)[['group','var','n','urban','rural','diff','lo','hi']]
R.to_csv('dose_v2.csv',index=False); print(R.round(3).to_string())
out={}
def reg(d,var,extra=()):
    X=pd.get_dummies(d[['dbin','emi']].astype(str),drop_first=True).astype(float)
    X['dbf']=d.dbf*10; X['b0']=d.b0*10; X['lat']=d.lat; X['lon']=d.lon
    for e in extra: X[e]=d[e]
    X=sm.add_constant(X); return sm.OLS(d[var],X).fit(cov_type='cluster',cov_kwds={'groups':d.blk})
d=df.dropna(subset=['dndvi','dalb','ndvi0','alb0','dntl'])
print('regression n',len(d))
for var in ['tn','td','en','ex']:
    for nm,extra in [('base',()),('ndvi',('dndvi','ndvi0')),('alb',('dalb','alb0')),('ntl',('dntl',)),('all',('dndvi','ndvi0','dalb','alb0','dntl'))]:
        f=reg(d,var,extra); ci=f.conf_int()
        r=dict(dbf=float(f.params['dbf']),lo=float(ci.loc['dbf',0]),hi=float(ci.loc['dbf',1]),p=float(f.pvalues['dbf']))
        for e in extra: r[e]=[float(f.params[e]),float(ci.loc[e,0]),float(ci.loc[e,1]),float(f.pvalues[e])]
        out[f'{var}_{nm}']=r
        if nm in('base','ndvi','alb','ntl','all'): print(var,nm,'dbf %.3f (%.3f,%.3f)'%(r['dbf'],r['lo'],r['hi']),{e:round(r[e][0],3) for e in extra})
# seasonal
for var in ['tn_s','tn_w','td_s','td_w']:
    f=reg(d,var); ci=f.conf_int(); out[var+'_base']=dict(dbf=float(f.params['dbf']),lo=float(ci.loc['dbf',0]),hi=float(ci.loc['dbf',1]))
    print(var,round(f.params['dbf'],3),round(ci.loc['dbf',0],3),round(ci.loc['dbf',1],3))
# sensitivities
for nm,dd in [('excl_coast5',d[d.dist>5]),('within50km',d[d.dist<=50]),('ols_vs_sen','skip')]:
    if isinstance(dd,str): continue
    for var in ['tn','td']:
        f=reg(dd,var); ci=f.conf_int(); out[f'{var}_{nm}']=[float(f.params['dbf']),float(ci.loc['dbf',0]),float(ci.loc['dbf',1])]
        print(nm,var,round(f.params['dbf'],3))
json.dump(out,open('reg_v2.json','w'),indent=1)
df.to_pickle('pixels_v2.pkl')
