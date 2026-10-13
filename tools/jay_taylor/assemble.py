import json,subprocess,os,shutil,sys,re
from plan2 import PLAN,REAL
from timing import build,avail
from vfx import VF,typer
P=json.load(open('lib/pieces.json')); C={int(k):v for k,v in json.load(open('lib/clean.json')).items()}
FPS=30
def run(*a): subprocess.run(['./ff','-v','error','-y',*a],check=True)
def rng(spec):
    if isinstance(spec,str): _,src,a,b=spec.split(':'); return src,float(a),float(b),'iw:ih:0:0'
    a,b=C.get(spec,(P[spec]['a'],P[spec]['b'])); return P[spec]['src'],a,b,P[spec]['crop']
def piece(spec,nf,out):
    if spec=='BLACK':
        run('-f','lavfi','-i','color=black:s=1920x1080:r=30','-frames:v',str(nf),'-pix_fmt','yuv420p','-c:v','libx264','-preset','fast','-crf','17','-video_track_timescale','15360',out); return
    src,a,b,crop=rng(spec); D=nf/FPS; av=b-a
    if src.startswith('stock') and av>D+2: a+=min(1.0,(av-D)/2)
    sp=1.0 if av>=D else max(av/D,0.5)
    take=min(av,D*sp)+0.1
    pre=f"setpts=PTS/{sp:.4f}," if sp<1 else ""
    run('-ss',f'{a:.3f}','-t',f'{take:.3f}','-i',src,'-filter_complex',VF(crop,pre)+",tpad=stop_mode=clone:stop_duration=20[v]",'-map','[v]','-an','-frames:v',str(nf),'-c:v','libx264','-preset','fast','-crf','17','-video_track_timescale','15360',out)
def concat(files,out):
    lst=out+'.txt'; open(lst,'w').write(''.join(f"file '{os.path.abspath(f)}'\n" for f in files))
    run('-f','concat','-safe','0','-i',lst,'-c','copy',out); os.remove(lst)
def shot(specs,text,nf,out):
    specs=[s for s in specs if s=='BLACK' or isinstance(s,str) or (rng(s)[2]-rng(s)[1])>=1.0]
    avs=[ (99 if s=='BLACK' else rng(s)[2]-rng(s)[1]) for s in specs]
    if len(specs)>1:
        if 'BLACK' in specs:  # real piece first at its natural length, black takes rest
            n0=min(nf-15,int(avs[0]*FPS)) ; alloc=[n0,nf-n0]
        else:
            tot=sum(avs); alloc=[int(round(nf*a/tot)) for a in avs]; alloc[-1]=nf-sum(alloc[:-1])
    else: alloc=[nf]
    print('shot',out,specs,alloc,nf,flush=True)
    global CUTS
    off=0
    parts=[]
    for k,(s,n) in enumerate(zip(specs,alloc)):
        CUTS.append((POS[0]+off)/FPS); off+=max(n,0)
        if n<=0: continue
        o=f'{out}.{k}.mp4'; piece(s,n,o); parts.append(o)
    base=out+'.b.mp4'
    if len(parts)>1: concat(parts,base)
    else: os.replace(parts[0],base)
    for p in parts:
        if os.path.exists(p): os.remove(p)
    if text:
        d=out+'_t'; typer(text,nf/FPS,d)
        run('-i',base,'-framerate','30','-i',f'{d}/%04d.png','-filter_complex',"[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]",'-map','[v]','-frames:v',str(nf),'-c:v','libx264','-preset','fast','-crf','17','-video_track_timescale','15360',out)
        shutil.rmtree(d); os.remove(base)
    else: os.replace(base,out)
T=build()
CUTS=[];POS=[0]
def chapter(ch):
    CUTS.clear(); POS[0]=0
    marks,end=T[ch]; wd=f'build/CH{ch}'; os.makedirs(wd,exist_ok=True)
    nar=f'{wd}/nar.wav'
    run('-i',f'vo/T{ch}.wav','-af','loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000','-ac','2',nar)
    # blocks
    blocks=[]; cur=[]
    for m in marks:
        if m[0]=='R': blocks.append(('N',cur)); blocks.append(('R',m[1])); cur=[]
        else: cur.append(m)
    blocks.append(('N',cur))
    blocks=[b for b in blocks if not (b[0]=='N' and not b[1])]
    last_n=max(i for i,b in enumerate(blocks) if b[0]=='N')
    ends_with_insert=blocks[-1][0]=='R'
    tail=0.35 if ends_with_insert else 0.9
    outs=[]; idx=0
    for bi,(kind,data) in enumerate(blocks):
        if kind=='R':
            name=data[4]; f=[x for x in os.listdir(f'out/CH{ch}') if name in x][0]
            o=f'{wd}/blk{bi:02d}.mp4'
            run('-i',f'out/CH{ch}/{f}','-af','afade=t=in:d=0.03,areverse,afade=t=in:d=0.08,areverse','-c:v','copy','-c:a','pcm_s16le','-ar','48000','-ac','2',o.replace('.mp4','.mov'))
            outs.append(o.replace('.mp4','.mov')); CUTS.append(POS[0]/FPS); POS[0]+=round(float(re.search(r'Duration: \d+:\d+:([\d.]+)',subprocess.run(['./ff','-i',o.replace('.mp4','.mov')],capture_output=True,text=True).stderr).group(1))*FPS); CUTS.append(POS[0]/FPS); continue
        # narration block
        t0=data[0][0]
        # block end: next block's first mark time, or end+tail
        nxt=None
        for b in blocks[bi+1:]:
            if b[0]=='N': nxt=b[1][0][0]; break
        t1=nxt if nxt is not None else end+tail
        if nxt is not None and bi+1<len(blocks) and blocks[bi+1][0]=='R':
            pass
        F=lambda t:int(round(t*FPS))
        times=[m[0] for m in data]+[t1]
        shots=[]
        for k,m in enumerate(data):
            nf=F(times[k+1])-F(times[k]); idx+=1
            so=f'{wd}/s{idx:03d}.mp4'
            shot(m[1][2],m[1][3],nf,so); POS[0]+=nf
            shots.append(so)
        v=f'{wd}/blk{bi:02d}_v.mp4'; concat(shots,v)
        a0=F(t0)/FPS; a1=F(t1)/FPS
        o=f'{wd}/blk{bi:02d}.mov'
        run('-i',v,'-ss',f'{a0:.4f}','-t',f'{a1-a0:.4f}','-i',nar,'-filter_complex',f"[1:a]apad,atrim=0:{a1-a0:.4f},afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse[a]",'-map','0:v','-map','[a]','-c:v','copy','-c:a','pcm_s16le',o)
        outs.append(o)
    # final
    n=len(outs); dur=sum(float(re.search(r'Duration: \d+:(\d+):([\d.]+)',subprocess.run(['./ff','-i',f],capture_output=True,text=True).stderr).group(2))+60*float(re.search(r'Duration: \d+:(\d+):',subprocess.run(['./ff','-i',f],capture_output=True,text=True).stderr).group(1)) for f in outs)
    vb=int(min(9000,(27.5e6*8/dur)/1000-192))
    ins=sum([['-i',f] for f in outs],[])
    fc=''.join(f'[{i}:v]setsar=1,fps=30,format=yuv420p[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];' for i in range(n))+''.join(f'[v{i}][a{i}]' for i in range(n))+f'concat=n={n}:v=1:a=1[v][a]'
    final=f'final/JayTaylor_CH{ch}.mp4'; os.makedirs('final',exist_ok=True)
    for p in (1,2):
        args=[*ins,'-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-b:v',f'{vb}k','-pass',str(p),'-passlogfile',f'{wd}/x264']
        if p==1: run(*args,'-an','-f','mp4','/dev/null')
        else: run(*args,'-c:a','aac','-b:a','192k','-movflags','+faststart',final)
    json.dump(CUTS,open(f'{wd}/cuts.json','w'))
    print(ch,'dur',round(dur,2),'vb',vb,'size',os.path.getsize(final)//1e6,'MB',flush=True)
if __name__=='__main__':
    for ch in sys.argv[1:]: chapter(ch)
