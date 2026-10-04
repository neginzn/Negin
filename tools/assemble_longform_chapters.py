import subprocess, json, os, re, glob, sys
FF="./ff"
def dur(f):
    o=subprocess.run([FF,"-i",f],capture_output=True,text=True).stderr
    h,m,s=re.search(r"Duration: (\d+):(\d+):([\d.]+)",o).groups(); return int(h)*3600+int(m)*60+float(s)
def F(n):  # final/ file by number
    if n=="045t": return "clip045_trim.mp4"
    return glob.glob("final/CH*_%03d_*.mp4"%int(n))[0]
fr=lambda t: round(t*30)/30
# chapter: inserts=[(vo_time, clipnum)], shots=[(vo_time, num, offset)]
C={
1:dict(ins=[(26.6,"004")],shots=[(0,"001",0),(8.4,"004",0),(11.2,"002",0),(15.5,"009",0),(17.7,"004",3),(23.1,"001",2),(27.0,"005",0),(32.4,"001",3),(35.3,"006",0)]),
2:dict(ins=[],shots=[(0,"007",0),(3.6,"008",0),(8.4,"009",0),(14.4,"010",0),(18.5,"011",0),(20.8,"012",0),(23.0,"013",0),(25.7,"014",0),(33.4,"015",0),(35.4,"016",0),(37.2,"017",0),(41.8,"018",0),(46.6,"019",0)]),
3:dict(ins=[(13.6,"021"),(43.5,"028")],shots=[(0,"020",0),(14.5,"022",0),(22.7,"023",0),(24.6,"024",0),(28.0,"025",0),(32.0,"026",0),(35.6,"027",0),(44.0,"029",0),(51.1,"030",0),(55.8,"031",0)]),
4:dict(ins=[(103.05,"040"),(108.3,"042")],shots=[(0,"032",0),(8.5,"033",0),(15.0,"011",0),(19.4,"013",0),(24.6,"012",3),(27.7,"034",0),(36.5,"035",0),(43.1,"036",0),(52.0,"012",0),(61.4,"037",0),(67.5,"022",0),(73.5,"038",0),(84.7,"039",0),(94.0,"017",0),(100.6,"035",0),(103.1,"041",0),(108.4,"043",0)]),
5:dict(ins=[(39.6,"045t"),(51.8,"046"),(66.7,"047")],shots=[(0,"044",0),(9.8,"048",0),(18.1,"044",0),(25.0,"048",3),(41.0,"043",0),(52.3,"035",0),(58.5,"048",0),(67.2,"041",0),(73.0,"048",4),(77.2,"039",0)]),
6:dict(ins=[],shots=[(0,"049",0),(9.7,"050",0),(12.7,"051",0),(21.2,"035",0),(23.5,"052",0)]),
7:dict(ins=[(25.9,"058")],shots=[(0,"053",0),(5.3,"054",0),(12.6,"055",0),(14.4,"056",0),(16.3,"057",0),(19.6,"043",0),(26.3,"059",0)]),
8:dict(ins=[(18.2,"061"),(29.9,"062")],shots=[(0,"060",0),(4.6,"050",0),(7.8,"044",0),(14.4,"052",0),(18.6,"004",0),(24.8,"048",0),(30.2,"044",2),(34.3,"033",0),(39.0,"039",0)]),
9:dict(ins=[(25.1,"065")],shots=[(0,"064",0),(5.4,"064",2),(8.9,"026",0),(14.0,"035",0),(17.6,"004",0),(25.6,"066",0)]),
10:dict(ins=[],shots=[(0,"067",0),(8.4,"068",0),(16.6,"069",0),(20.1,"070",0),(25.2,"006",0),(30.0,"071",0),(40.1,"072",0)]),
}
VID="fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709,settb=1/15360"
def lufs(f):
    o=subprocess.run([FF,"-i",f,"-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS",o)[-1])
def run(*a): subprocess.run([FF,"-loglevel","error","-y",*a],check=True)
def build(ch):
    cfg=C[ch]; vo="vo/B%d.mp3"%ch; D=dur(vo)
    w=f"tmp{ch}"; os.makedirs(w,exist_ok=True)
    cuts=[0]+[t for t,_ in cfg["ins"]]+[D]
    vids=[]; auds=[]; k=0
    shots=cfg["shots"]
    for pi in range(len(cuts)-1):
        a,b=cuts[pi],cuts[pi+1]
        # narration piece audio
        pd=fr(b-a); aw=f"{w}/a{k:02d}.wav"
        run("-ss",str(a),"-t",f"{pd:.4f}","-i",vo,"-af",f"aformat=sample_rates=48000:channel_layouts=stereo,apad,atrim=end_sample={round(pd*48000)}","-c:a","pcm_s16le",aw)
        g=-16-lufs(aw); run("-i",aw,"-af",f"volume={g:.2f}dB","-c:a","pcm_s16le",aw+".g.wav"); auds.append(aw+".g.wav")
        # visuals: shots overlapping [a,b)
        st=[s for s in shots if s[0]<b-0.05]
        cur=[s for s in st if s[0]<=a+0.05]
        seq=([cur[-1]] if cur else [])+[s for s in st if s[0]>a+0.05]
        t=a; total=0
        for j,(s0,num,off) in enumerate(seq):
            s_start=max(s0,a); s_end=seq[j+1][0] if j+1<len(seq) else b
            # if shot began before this piece, continue from where it left off
            o=off+(s_start-s0)
            sd=fr(s_end-s_start) if j+1<len(seq) else fr(pd-total)
            if sd<=0: continue
            src=F(num); SD=dur(src)
            if off==0 and s_start==s0: o=max(0.0,(SD-sd)/2)
            avail=SD-o
            if avail<0.5: o=0; avail=dur(src)
            speed = 1.0 if avail>=sd else max(avail/sd,0.6)
            vf=f"setpts=PTS/{speed:.4f}," if speed<1 else ""
            out=f"{w}/v{k:02d}_{j:02d}.mp4"
            run("-stream_loop","-1","-ss",f"{o:.3f}","-i",src,"-an","-vf",vf+VID+f",tpad=stop_mode=clone:stop_duration=1,trim=duration={sd:.4f}","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18",out)
            vids.append(out); total+=sd
        k+=1
        if pi<len(cfg["ins"]):
            c=F(cfg["ins"][pi][1]); cd=fr(dur(c)-0.02)
            out=f"{w}/v{k:02d}_clip.mp4"
            run("-i",c,"-an","-vf",VID+f",trim=duration={cd:.4f}","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","18",out); vids.append(out)
            aw=f"{w}/a{k:02d}.wav"
            run("-i",c,"-vn","-af",f"aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.08,afade=t=out:st={cd-0.15:.3f}:d=0.15,apad,atrim=end_sample={round(cd*48000)}","-c:a","pcm_s16le",aw)
            g=-15-lufs(aw); run("-i",aw,"-af",f"volume={g:.2f}dB","-c:a","pcm_s16le",aw+".g.wav"); auds.append(aw+".g.wav")
            k+=1
    # concat video via filter
    inp=[]; fc=""
    for i,v in enumerate(vids): inp+=["-i",v]; fc+=f"[{i}:v]"
    fc+=f"concat=n={len(vids)}:v=1:a=0[v]"
    run(*inp,"-filter_complex",fc,"-map","[v]","-fps_mode","passthrough","-c:v","libx264","-preset","fast","-crf","17",f"{w}/vj.mp4")
    open(f"{w}/al.txt","w").write("".join(f"file '{os.path.basename(x)}'\n" for x in auds))
    run("-f","concat","-safe","0","-i",f"{w}/al.txt","-c","copy",f"{w}/aj.wav")
    T=dur(f"{w}/aj.wav"); br=int(min(5500,(26*8*1024/T)-200))
    out=f"delphi_out/Delphi_CH{ch:02d}.mp4"
    run("-i",f"{w}/vj.mp4","-i",f"{w}/aj.wav","-filter_complex","[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]","-map","0:v","-map","[a]","-fps_mode","passthrough",
        "-c:v","libx264","-preset","medium","-b:v",f"{br}k","-maxrate",f"{int(br*1.3)}k","-bufsize",f"{br*2}k","-c:a","aac","-b:a","160k","-movflags","+faststart","-shortest",out)
    print(ch,"video",round(dur(f"{w}/vj.mp4"),2),"audio",round(T,2),"->",out,round(os.path.getsize(out)/1e6,1),"MB")
os.makedirs("delphi_out",exist_ok=True)
for ch in [int(x) for x in sys.argv[1:]] or range(1,11): build(ch)
