import subprocess, json, os, re, sys
FF="./ff"; P=json.load(open("lib/pieces.json"))
def dur(f):
    o=subprocess.run([FF,"-i",f],capture_output=True,text=True).stderr
    h,m,s=re.search(r"Duration: (\d+):(\d+):([\d.]+)",o).groups(); return int(h)*3600+int(m)*60+float(s)
def run(*a):
    r=subprocess.run([FF,"-loglevel","error","-y",*a],capture_output=True,text=True)
    if r.returncode: print(r.stderr[-800:]); raise SystemExit("ffmpeg failed")
def lufs(f):
    o=subprocess.run([FF,"-i",f,"-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS",o)[-1])
fr=lambda t: round(t*30)/30
# framing: crop region -> fit into 1920x864 band (blur fill) -> letterbox 1920x1080
def crop_for(src,t=None):
    if "21a_interro" in src and t is not None and t>85: return "iw*0.9:ih*0.72:iw*0.05:ih*0.03"
    if "wndu_appeal" in src and t is not None and 43<t<48.2: return "iw*0.46:ih*0.41:iw*0.0:ih*0.15"
    if "wndu_arrest22" in src and t is not None and t<15: return "iw*0.92:ih*0.84:iw*0.04:ih*0.03"
    if "cnn_bridge" in src and t is not None and 13<t<64: return "iw*0.644:ih*0.74:iw*0.178:ih*0.13"
    if "cnn_bridge" in src: return "iw*0.9:ih*0.72:iw*0.05:ih*0.14"
    if "21a_interro" in src: return "iw*0.762:ih*0.632:iw*0.117:ih*0.125"
    if "wndu_interro" in src: return "iw*0.666:ih*0.667:iw*0.234:ih*0.118"
    if "wndu_2019_sketch" in src: return "iw*0.306:ih:iw*0.590:0"
    return "iw*0.9:ih*0.72:iw*0.05:ih*0.03"
def VF(crop, pre=""):
    return (f"[0:v]{pre}crop={crop},setsar=1,split[a][b];[b]scale=1920:864:force_original_aspect_ratio=increase,crop=1920:864,gblur=sigma=28,eq=brightness=-0.3[bg];"
            "[a]scale=1920:864:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,pad=1920:1080:0:108:black,setsar=1,fps=30,format=yuv420p,"
            "setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709,settb=1/15360")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT=ImageFont.truetype("lib/SpecialElite.ttf",78)
def typer(text, sd, d):
    os.makedirs(d,exist_ok=True); n=int(round(sd*30)); cps=0.075; t0=0.25
    for i in range(n):
        t=i/30; k=max(0,min(len(text),int((t-t0)/cps)+1)) if t>=t0 else 0
        alpha=1.0 if t<sd-0.45 else max(0,(sd-t)/0.45)
        img=Image.new("RGBA",(1920,1080),(0,0,0,0))
        if k>0:
            s=text[:k]+("|" if (k<len(text) or int(t*2)%2==0) and t<sd-0.45 else "")
            sh=Image.new("RGBA",(1920,1080),(0,0,0,0)); ImageDraw.Draw(sh).text((114,1080-108-150+4),s,font=FONT,fill=(0,0,0,int(200*alpha)))
            sh=sh.filter(ImageFilter.GaussianBlur(4)); img.alpha_composite(sh)
            ImageDraw.Draw(img).text((110,1080-108-150),s,font=FONT,fill=(245,240,230,int(255*alpha)))
        img.save(f"{d}/{i:04d}.png")
def shot(pid, off, sd, out, text=None):
    p=P[pid]; a=p["a"]+off; rem=p["b"]-a
    if rem<0.6: a=p["a"]; rem=p["b"]-p["a"]
    sp=1.0 if rem>=sd else max(rem/sd,0.58)
    pre=f"setpts=PTS/{sp:.4f}," if sp<1 else ""
    run("-ss",f"{a:.3f}","-t",f"{min(rem,sd*sp)+0.05:.3f}","-i",p["src"],"-filter_complex",VF(crop_for(p["src"],a),pre)+f",tpad=stop_mode=clone:stop_duration=3,trim=duration={sd:.4f}[v]",
        "-map","[v]","-an","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18",out)
    if text:
        d=out+"_txt"; typer(text,sd,d)
        run("-i",out,"-framerate","30","-i",f"{d}/%04d.png","-filter_complex","[0:v][1:v]overlay=0:0:format=auto,format=yuv420p,settb=1/15360[v]","-map","[v]","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18",out+".t.mp4")
        os.replace(out+".t.mp4",out)
# inserts with real audio: id -> (src, start, dur, cover_seconds_with_piece)
INS={"004":("21a_appeal1.mp4",96.5,10.85,None),"021":("wndu_2019_sketch.mp4",26.5,8.5,None),"028":("wndu_2019_a.mp4",52.6,12.0,None),
"040":("21a_interro.mp4",30.3,25.5,None),"042":("wndu_arrest22.mp4",51.0,22.3,None),"045t":("wndu_interro.mp4",[(45.3,59.7),(62.9,68.1)],None,None),
"046":("21a_appeal1.mp4",34.3,17.4,None),"047":("21a_interro.mp4",90.8,37.5,None),"058":("21a_sentence2.mp4",0.0,21.0,(122,2.6)),
"061":("wndu_appeal.mp4",133.8,8.8,None),"062":("21a_appeal1.mp4",58.6,13.7,None),"065":("21a_appeal1.mp4",79.0,28.35,None)}
def make_insert(k, w):
    src,st,d,cover=INS[k]; vo=f"{w}/ins{k}.mp4"
    if src=="CONF":
        if not os.path.exists("lib/mug.png"):
            p=P[272]; run("-ss",str(p["a"]+3),"-i",p["src"],"-frames:v","1","-vf","crop=iw:ih*0.8:0:0","lib/mug.png")
        run("-loop","1","-framerate","30","-i","lib/mug.png","-ss",str(st),"-t",str(d),"-i","21a_interro.mp4","-filter_complex",
            "[0:v]scale=3840:-2,zoompan=z='1+0.10*on/1125':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x864:fps=30,eq=saturation=0.7:brightness=-0.05,vignette=PI/4,pad=1920:1080:0:108:black,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709,settb=1/15360[v];[1:a]anull[a]",
            "-map","[v]","-map","[a]","-t",str(d),"-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18","-c:a","pcm_s16le","-f","mov",vo)
    elif isinstance(st,list):
        parts=[]
        for i,(a,b) in enumerate(st):
            o=f"{w}/ins{k}_{i}.mov"
            run("-ss",str(a),"-t",str(b-a),"-i",src,"-filter_complex",VF(crop_for(src))+"[v]","-map","[v]","-map","0:a","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18","-c:a","pcm_s16le","-ar","48000","-ac","2",o); parts.append(o)
        inp=sum([["-i",x] for x in parts],[])
        run(*inp,"-filter_complex","".join(f"[{i}:v][{i}:a]" for i in range(len(parts)))+f"concat=n={len(parts)}:v=1:a=1[v][a]","-map","[v]","-map","[a]","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18","-c:a","pcm_s16le","-f","mov",vo)
    else:
        run("-ss",str(st),"-t",str(d),"-i",src,"-filter_complex",VF(crop_for(src,st))+"[v]","-map","[v]","-map","0:a","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18","-c:a","pcm_s16le","-ar","48000","-ac","2","-f","mov",vo)
        if cover:
            pid,cs=cover; c=f"{w}/cov{k}.mp4"; shot(pid,0,cs,c)
            run("-i",vo,"-i",c,"-filter_complex",f"[0:v][1:v]overlay=0:0:enable='lt(t,{cs})'[v]","-map","[v]","-map","0:a","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18","-c:a","copy","-f","mov",vo+".2")
            os.replace(vo+".2",vo)
    return vo
PLAN=json.load(open("plan.json"))
def build(ch):
    cfg=PLAN[str(ch)]; vo_f=f"vo/B{ch}.mp3"; D=dur(vo_f); w=f"t2_{ch}"; os.makedirs(w,exist_ok=True)
    ins=cfg["ins"]; shots=[(s[0],s[1],s[2] if len(s)>2 else 0,s[3] if len(s)>3 else None) for s in cfg["shots"]]
    cuts=[0]+[t for t,_ in ins]+[D]; vids=[]; auds=[]; k=0
    for pi in range(len(cuts)-1):
        a,b=cuts[pi],cuts[pi+1]; pd=fr(b-a)
        aw=f"{w}/a{k:02d}.wav"
        run("-ss",str(a),"-t",f"{pd:.4f}","-i",vo_f,"-af",f"aformat=sample_rates=48000:channel_layouts=stereo,apad,atrim=end_sample={round(pd*48000)}","-c:a","pcm_s16le",aw)
        run("-i",aw,"-af",f"volume={-16-lufs(aw):.2f}dB","-c:a","pcm_s16le",aw+".g.wav"); auds.append(aw+".g.wav")
        seq=[s for s in shots if a-0.05<=s[0]<b-0.05]
        if not seq or seq[0][0]>a+0.05: raise SystemExit(f"CH{ch} gap at {a}")
        total=0
        for j,(s0,pid,off,txt) in enumerate(seq):
            sd=fr((seq[j+1][0] if j+1<len(seq) else b)-max(s0,a)) if j+1<len(seq) else fr(pd-total)
            o=f"{w}/v{k:02d}_{j:02d}.mp4"; shot(pid,off,sd,o,txt); vids.append(o); total+=sd
        k+=1
        if pi<len(ins):
            iv=make_insert(ins[pi][1],w); cd=fr(dur(iv)-0.03)
            o=f"{w}/v{k:02d}_ins.mp4"
            run("-i",iv,"-an","-vf",f"trim=duration={cd:.4f}","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18",o); vids.append(o)
            aw=f"{w}/a{k:02d}.wav"
            run("-i",iv,"-vn","-af",f"aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.08,afade=t=out:st={cd-0.15:.3f}:d=0.15,apad,atrim=end_sample={round(cd*48000)}","-c:a","pcm_s16le",aw)
            run("-i",aw,"-af",f"volume={-15-lufs(aw):.2f}dB","-c:a","pcm_s16le",aw+".g.wav"); auds.append(aw+".g.wav"); k+=1
    inp=sum([["-i",v] for v in vids],[])
    run(*inp,"-filter_complex","".join(f"[{i}:v]" for i in range(len(vids)))+f"concat=n={len(vids)}:v=1:a=0[v]","-map","[v]","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","17",f"{w}/vj.mp4")
    open(f"{w}/al.txt","w").write("".join(f"file '{os.path.basename(x)}'\n" for x in auds))
    run("-f","concat","-safe","0","-i",f"{w}/al.txt","-c","copy",f"{w}/aj.wav")
    T=dur(f"{w}/aj.wav"); br=int(min(5500,(26*8*1024/T)-200)); out=f"delphi_v2/Delphi_CH{ch:02d}.mp4"
    run("-i",f"{w}/vj.mp4","-i",f"{w}/aj.wav","-filter_complex","[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]","-map","0:v","-map","[a]","-fps_mode","passthrough",
        "-c:v","libx264","-preset","medium","-b:v",f"{br}k","-maxrate",f"{int(br*1.3)}k","-bufsize",f"{br*2}k","-c:a","aac","-b:a","160k","-movflags","+faststart","-shortest",out)
    print(ch,"v",round(dur(f"{w}/vj.mp4"),2),"a",round(T,2),round(os.path.getsize(out)/1e6,1),"MB",flush=True)
os.makedirs("delphi_v2",exist_ok=True)
for ch in sys.argv[1:]: build(int(ch))
