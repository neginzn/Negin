import json,re
from plan2 import PLAN
from anchors import A
W=json.load(open('vo/words.json'))
P=json.load(open('lib/pieces.json')); C={int(k):v for k,v in json.load(open('lib/clean.json')).items()}
def norm(w): return re.sub(r'[^a-z0-9]','',w.lower())
def toks(ws): return [norm(x) for x in ws if norm(x)]
def find(words,phrase,start):
    p=toks(phrase.replace('-',' ').split()); wn=[norm(w[2]) for w in words]
    for i in range(start,len(words)):
        j=i; ok=True
        for t in p:
            while j<len(words) and wn[j]=='' : j+=1
            if j>=len(words) or not (wn[j]==t or (wn[j].startswith(t) and len(t)>=2) ): ok=False;break
            j+=1
        if ok: return i
    raise Exception(f'not found {phrase} from {start}')
def avail(spec):
    if spec=='BLACK': return 99
    if isinstance(spec,str): _,_,a,b=spec.split(':'); return float(b)-float(a)
    a,b=C.get(spec,(P[spec]['a'],P[spec]['b'])); return b-a
def build():
    out={}
    for ch in A:
        items=[r for r in PLAN if r[0]==ch]; assert len(items)==len(A[ch]),(ch,len(items),len(A[ch]))
        words=W['T'+ch]; pos=0; marks=[]
        for r,ph in zip(items,A[ch]):
            if ph=='@R': marks.append(('R',r)); continue
            i=find(words,ph,pos); pos=i+1
            prev_end=words[i-1][1] if i>0 else 0.0
            t=0.0 if not marks or all(m[0]=='R' for m in marks) and i==0 else (prev_end+words[i][0])/2
            if i==0: t=0.0
            marks.append((t,r))
        end=words[-1][1]
        if ch=='10':  # voice cut off after "tool in" -> end after "tool"
            k=max(i for i,w in enumerate(words) if norm(w[2])=='tool'); end=words[k][1]
        out[ch]=(marks,end)
    return out
if __name__=='__main__':
    o=build()
    for ch,(marks,end) in o.items():
        ts=[m[0] for m in marks if m[0]!='R']+[end+0.6]
        k=0
        for m in marks:
            if m[0]=='R': print(ch,'  INSERT',m[1][4]); continue
            d=ts[k+1]-ts[k]; k+=1
            av=sum(avail(s) for s in m[1][2])
            flag='  <<SHORT' if av<d*0.6 else ''
            print(ch,f'{m[0]:6.2f} dur {d:5.2f} avail {av:5.2f}',m[1][4],flag)
