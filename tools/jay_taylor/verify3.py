import subprocess,re,sys,json
for ch in sys.argv[1:]:
    P=json.load(open(f'build/CH{ch}/cuts.json'))
    o=subprocess.run(['./ff','-i',f'final/JayTaylor_CH{ch}.mp4','-vf',"scale=320:-2,select='gt(scene,0.18)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr
    cuts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',o)]
    bad=[round(c,2) for c in cuts if min(abs(c-p) for p in P)>0.1]
    print(ch,'planned',len(P),'detected',len(cuts),'UNEXPECTED',bad,flush=True)
