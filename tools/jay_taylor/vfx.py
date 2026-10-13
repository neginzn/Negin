import json,subprocess,os,sys,shutil
from plan2 import PLAN,REAL
from PIL import Image,ImageDraw,ImageFont,ImageFilter
P=json.load(open('lib/pieces.json')); C={int(k):v for k,v in json.load(open('lib/clean.json')).items()}
NTL='raw/251118_ntl_crime_1_1239.mp4'; NC='iw*0.80:ih*0.73:iw*0.10:0'
def run(*a): subprocess.run(['./ff','-v','error','-y',*a],check=True)
def VF(crop,pre=""):
    return (f"[0:v]{pre}crop={crop},setsar=1,split[a][b];[b]scale=1920:864:force_original_aspect_ratio=increase,crop=1920:864,gblur=sigma=28,eq=brightness=-0.3[bg];"
     "[a]scale=1920:864:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,pad=1920:1080:0:108:black,setsar=1,fps=30,format=yuv420p")
FONT=ImageFont.truetype("lib/SpecialElite.ttf",78)
def typer(text,sd,d):
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
def seg(spec,out,cap):
    if spec=="BLACK":
        run('-f','lavfi','-i','color=black:s=1920x1080:r=30','-t','4','-pix_fmt','yuv420p','-c:v','libx264','-crf','20',out); return 4
    if isinstance(spec,str):
        _,src,a,b=spec.split(':'); a,b=float(a),float(b); crop='iw:ih:0:0'
    else:
        p=P[spec]; a,b=C.get(spec,(p['a'],p['b'])); src=p['src']; crop=p['crop']
        if src.startswith('stock') and b-a>cap+2: a+=1.0
    rem=b-a; d=min(rem,cap); sp=1.0
    if d<2.5: sp=max(d/2.5,0.6)
    pre=f"setpts=PTS/{sp:.4f}," if sp<1 else ""
    sd=max(d/sp,min(2.5,d/0.6))
    run('-ss',f'{a:.3f}','-t',f'{d:.3f}','-i',src,'-filter_complex',VF(crop,pre)+f",tpad=stop_mode=clone:stop_duration=2,trim=duration={sd:.3f}[v]",'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','20',out)
    return sd
