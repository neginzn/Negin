import numpy as np, subprocess, math, random, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S='/tmp/claude-0/-home-user-Negin/d5288e51-5e9b-5613-adee-5159b473691a/scratchpad/reel/'
W,H,FPS=1080,1920,24
C1,C2=7.9167,7.9167
VEND=C1+C2                  # end of moving video
DUR=18.0; N=int(DUR*FPS)
random.seed(4); np.random.seed(4)

# ---------------- voice lines ----------------
LINES=[ # (file, start, caption, highlight words)
 ('v1.wav',0.20,"ALIENS JUST INVADED YOUR CITY!",{"INVADED"}),
 ('v2.wav',2.30,"THE GOVERNMENT? HAS NO PLAN.",{"NO","PLAN."}),
 ('v3.wav',4.15,"ANYONE THEY SPOT OUTSIDE... DISAPPEARS. IN SECONDS.",{"DISAPPEARS."}),
 ('v4.wav',8.25,"YOU HAVE WHAT'S IN YOUR HOME.",{"HOME."}),
 ('v5.wav',9.75,"AND 30 DAYS.",{"30","DAYS."}),
 ('v6.wav',11.05,"STAY INSIDE AND RATION EVERYTHING.",{"RATION"}),
 ('v7.wav',13.55,"OR GO OUT AND LOOK FOR FOOD.",{"FOOD."}),
]
def wav_read(p):
    with wave.open(p) as w:
        sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    return sr,a
durs=[]
for f,st,_,_ in LINES+[('v8.wav',16.05,'',set())]:
    sr,a=wav_read(S+f); durs.append(len(a)/sr)

# ---------------- fonts ----------------
FCAP=ImageFont.truetype(S+'mont900.ttf',84)
FBIG=ImageFont.truetype(S+'mont900.ttf',118)
FSM=ImageFont.truetype(S+'mont900.ttf',52)
JB='/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf'
FH1=ImageFont.truetype(JB,56); FH2=ImageFont.truetype(JB,36); FH3=ImageFont.truetype(JB,34)
GREEN=(124,255,107); WHITE=(255,255,255); RED=(255,60,60); DARK=(8,14,10)

def ease(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def back(x,s=1.7): x=max(0,min(1,x))-1; return 1+(s+1)*x**3+s*x**2

def wrap(words,font,maxw):
    lines=[[]]
    for w in words:
        test=' '.join(lines[-1]+[w])
        if font.getlength(test)>maxw and lines[-1]: lines.append([w])
        else: lines[-1].append(w)
    return lines

def caption(img,text,hl,t0,t,y=1400,font=FCAP):
    k=(t-t0)/0.22
    if k<0: return
    sc=0.82+0.18*back(min(1,k)); al=ease(k*1.6)
    words=text.split(); ls=wrap(words,font,900)
    lh=font.size*1.12; tw=W; th=int(lh*len(ls))+40
    lay=Image.new('RGBA',(tw,th),(0,0,0,0)); d=ImageDraw.Draw(lay)
    for i,l in enumerate(ls):
        x=(tw-font.getlength(' '.join(l)))/2; yy=10+i*lh
        for w in l:
            col=GREEN if w in hl else WHITE
            d.text((x+4,yy+6),w,font=font,fill=(0,0,0,170))
            d.text((x,yy),w,font=font,fill=col,stroke_width=7,stroke_fill=(0,0,0))
            x+=font.getlength(w+' ')
    if sc!=1: lay=lay.resize((int(tw*sc),int(th*sc)),Image.LANCZOS)
    if al<1:
        a=np.asarray(lay.getchannel('A')).astype(np.float32)*al; lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(lay,(int((W-lay.width)/2),int(y-lay.height/2)))

# ---------------- HUD ----------------
HUD_T=9.75
def hud(img,t):
    if t<HUD_T: return
    k=t-HUD_T
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    x0,y0=50,150; w=440; h=250
    wk=ease(k/0.35)
    d.rectangle((x0,y0,x0+int(w*wk),y0+h),fill=(5,20,10,150))
    d.line((x0,y0,x0+int(w*wk),y0),fill=GREEN+(255,),width=4)
    d.line((x0,y0+h,x0+int(w*wk),y0+h),fill=GREEN+(160,),width=2)
    d.rectangle((x0,y0,x0+6,y0+h),fill=GREEN+(255,))
    if k>0.3:
        s="DAY 01/30"; n=min(len(s),int((k-0.3)/0.05)+1)
        d.text((x0+28,y0+22),s[:n],font=FH1,fill=GREEN+(255,))
        if n<len(s) or int(t*3)%2==0:
            cx=x0+28+FH1.getlength(s[:n])+4; d.rectangle((cx,y0+30,cx+22,y0+84),fill=GREEN+(220,))
    rows=[("WATER","180 L",GREEN),("FOOD","22",GREEN),("THREAT","EXTREME",RED)]
    for i,(a,b,c) in enumerate(rows):
        tk=k-0.9-i*0.22
        if tk<0: continue
        al=int(255*ease(tk/0.2)); yy=y0+104+i*46
        if a=="THREAT" and int(t*4)%2==0: al=int(al*0.45)
        d.text((x0+28,yy),f"{a:<7}",font=FH2,fill=(200,230,200,al))
        d.text((x0+210,yy),b,font=FH2,fill=c+(al,))
    img.alpha_composite(lay)

# ---------------- scan overlay ----------------
SCAN_T=12.7; LOCK_T=15.55
def scan(img,t):
    if t<SCAN_T: return
    k=t-SCAN_T; locked=t>=LOCK_T
    col=RED if locked else GREEN
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    # reticle brackets around face
    s=1.35-0.35*ease(k/0.45)
    cx,cy=540,860; bw,bh=320*s,330*s; L=90; lw=8
    for sx in (-1,1):
        for sy in (-1,1):
            px,py=cx+sx*bw,cy+sy*bh
            d.line((px,py,px-sx*L,py),fill=col+(255,),width=lw)
            d.line((px,py,px,py-sy*L),fill=col+(255,),width=lw)
    # center cross
    d.line((cx-26,cy,cx+26,cy),fill=col+(200,),width=3); d.line((cx,cy-26,cx,cy+26),fill=col+(200,),width=3)
    # sweeping scan line
    if not locked:
        p=(k*0.9)%1; yy=cy-bh+2*bh*p
        for j in range(18):
            d.line((cx-bw,yy-j*3,cx+bw,yy-j*3),fill=col+(int(110*(1-j/18)),),width=3)
    # data panel top-right
    rows=[(13.05,"SCANNING..."),(13.55,"SPECIES: HUMAN"),(14.05,"HEART RATE: {hr} BPM"),(14.55,"BODY TEMP: 36.9°C"),(15.05,"STATUS: ALIVE")]
    px,py=560,150
    vis=[r for r in rows if t>=r[0]]
    if vis:
        hh=40+len(vis)*48
        d.rectangle((px,py,px+470,py+hh),fill=(5,20,10,150)); d.rectangle((px+464,py,px+470,py+hh),fill=col+(255,))
        for i,(t0,txt) in enumerate(vis):
            if '{hr}' in txt:
                hr=int(72+min(1,(t-t0)/0.6)*56)
                txt=txt.format(hr=hr)
            n=min(len(txt),int((t-t0)/0.025)+1)
            d.text((px+22,py+22+i*48),txt[:n],font=FH3,fill=col+(255,))
    if locked:
        kk=t-LOCK_T
        a=255 if int(kk*6)%2==0 else 120
        tw=FBIG.getlength("TARGET LOCKED")*0.62
        f=ImageFont.truetype(S+'mont900.ttf',74)
        tw=f.getlength("TARGET LOCKED")
        d.rectangle((cx-tw/2-30,cy+bh+40,cx+tw/2+30,cy+bh+140),fill=(120,0,0,int(a*0.7)))
        d.text((cx-tw/2,cy+bh+52),"TARGET LOCKED",font=f,fill=(255,255,255,a))
    img.alpha_composite(lay)

# ---------------- base video frames ----------------
def frames(path):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',path,'-vf',f'scale={W}:{H}:flags=lanczos','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    out=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        out.append(np.frombuffer(b,np.uint8).reshape(H,W,3))
    return out
f1=frames(S+'c1.mp4'); f2=frames(S+'c2.mp4')
print(len(f1),len(f2))

def glitch(arr,amt):
    a=arr.copy()
    sh=int(30*amt)
    a[...,0]=np.roll(arr[...,0],sh,axis=1); a[...,2]=np.roll(arr[...,2],-sh,axis=1)
    for _ in range(int(14*amt)):
        y=random.randint(0,H-60); hh=random.randint(10,80); off=random.randint(-120,120)
        a[y:y+hh]=np.roll(a[y:y+hh],off,axis=1)
    noise=(np.random.rand(H//8,W//8)*255*amt*0.35).astype(np.uint8)
    noise=np.kron(noise,np.ones((8,8),np.uint8))[:H,:W]
    a=np.clip(a.astype(np.int16)+noise[...,None],0,255).astype(np.uint8)
    return a

def zoom(arr,z,dx=0,dy=0):
    if z<=1.0001 and dx==0 and dy==0: return arr
    im=Image.fromarray(arr); w2,h2=W/z,H/z
    x0=(W-w2)/2+dx; y0=(H-h2)/2+dy
    return np.asarray(im.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+w2,y0+h2)))

HITS=[0.05,C1,LOCK_T]
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p',S+'video_noaudio.mp4'],stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    if t<C1: base=f1[min(i,len(f1)-1)]; z=1.0+0.06*(t/C1)
    elif t<VEND: base=f2[min(i-len(f1),len(f2)-1)]; z=1.0
    else: base=f2[-1]; z=1.0+0.03*min(1,(t-VEND)/2)
    # shake on hits
    dx=dy=0
    for h in HITS:
        if 0<=t-h<0.35:
            a=(1-(t-h)/0.35)*14; dx+=random.uniform(-a,a); dy+=random.uniform(-a,a)
    arr=zoom(base,z+ (0.02 if dx or dy else 0),dx,dy)
    # glitch transition
    if abs(t-C1)<0.16: arr=glitch(arr,1-abs(t-C1)/0.16)
    if LOCK_T<=t<LOCK_T+0.12: arr=glitch(arr,0.6)
    img=Image.fromarray(arr).convert('RGBA')
    # flash in from black at start / white flash at transition
    ov=Image.new('RGBA',(W,H),(0,0,0,0))
    if t<0.25: ov=Image.new('RGBA',(W,H),(0,0,0,int(255*(1-t/0.25))))
    if 0<=t-C1<0.08: ov=Image.new('RGBA',(W,H),(255,255,255,170))
    if t>=VEND+0.1:   # end card darken
        ov=Image.new('RGBA',(W,H),(0,0,0,int(165*ease((t-VEND-0.1)/0.4))))
    img.alpha_composite(ov)
    if t>=SCAN_T and t<VEND+0.1:
        tint=Image.new('RGBA',(W,H),(0,255,60,18 if int(t*12)%5 else 34) if t<LOCK_T else (255,0,0,30)); img.alpha_composite(tint)
    hud(img,t)
    if t<VEND+0.1: scan(img,t)
    # captions
    for j,(f,st,txt,hl) in enumerate(LINES):
        nxt=LINES[j+1][1] if j+1<len(LINES) else VEND
        end=min(nxt-0.05, st+durs[j]+0.6)
        if st-0.05<=t<end: caption(img,txt,hl,st-0.05,t,y=(1580 if t>=SCAN_T else 1420))
    # end card
    if t>=16.0:
        caption(img,"WHAT WOULD",{"YOU"},16.0,t,y=740,font=FBIG)
        caption(img,"YOU DO?",{"YOU"},16.25,t,y=900,font=FBIG)
    if t>=16.9:
        k=t-16.9; bob=8*math.sin(k*6)
        caption(img,"FULL STORY: 30 DAYS",{"30","DAYS"},16.9,t,y=1250,font=FSM)
        d=ImageDraw.Draw(img); ax,ay=540,1345+bob
        d.polygon([(ax-34,ay),(ax+34,ay),(ax,ay+40)],fill=GREEN+(int(255*ease(k/0.3)),))
    enc.stdin.write(np.asarray(img.convert('RGB')).tobytes())
enc.stdin.close(); enc.wait()

# ---------------- audio ----------------
SR=48000; NS=int(DUR*SR); tt=np.arange(NS)/SR
mix=np.zeros(NS); music=np.zeros(NS)
def env(t0,a,d):
    e=np.zeros(NS); i0=int(t0*SR); n=int((a+d)*SR)
    x=np.arange(n)/SR; seg=np.where(x<a,x/max(a,1e-4),np.exp(-(x-a)/max(d/4,1e-4)))
    e[i0:i0+n]=seg[:max(0,min(n,NS-i0))]; return e
def lp(x,c=0.02):
    y=np.zeros_like(x); acc=0.0
    for i in range(0,len(x)): acc+=c*(x[i]-acc); y[i]=acc
    return y
# drone
swell=np.interp(tt,[0,1,7.9,9,12.7,15.5,16,17.4,18],[0,0.55,0.7,0.6,0.8,1.0,0.45,0.35,0])
dr=(np.sin(2*np.pi*41.2*tt)+0.5*np.sin(2*np.pi*61.7*tt)+0.25*np.sin(2*np.pi*82.4*tt))*(0.8+0.2*np.sin(2*np.pi*0.15*tt))
noise=np.random.randn(NS); nz=np.convolve(noise,np.ones(400)/400,mode='same')*6
music+=0.16*dr*swell
# ship hum during clip 1
hum=np.sin(2*np.pi*95*tt+2*np.sin(2*np.pi*0.7*tt))*(0.5+0.5*np.sin(2*np.pi*3.1*tt))
pass
# booms
def boom(t0,g=1.0):
    i0=int(t0*SR); n=int(1.8*SR); x=np.arange(n)/SR
    f=35+90*np.exp(-x*6); ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph)*np.exp(-x*2.2)+0.5*np.random.randn(n)*np.exp(-x*30)
    m=min(n,NS-i0); mix[i0:i0+m]+=g*0.55*s[:m]
boom(0.03,1.0); boom(C1,0.9); boom(LOCK_T,1.1); boom(16.0,0.6); boom(12.7,0.5)
# whoosh into transition
i0=int((C1-0.7)*SR); n=int(0.75*SR); w=np.random.randn(n); w=np.convolve(w,np.ones(30)/30,'same')
mix[i0:i0+n]+=0.3*np.convolve(w,np.ones(60)/60,'same')*np.linspace(0,1,n)**2
# glitch bursts
for tg in (C1-0.08,C1+0.02,LOCK_T):
    i0=int(tg*SR); n=int(0.14*SR); g=np.sign(np.random.randn(n))*(np.random.rand(n)>0.4)
    g=np.repeat(g[::12],12)[:n]; g=np.convolve(g,np.ones(24)/24,'same'); mix[i0:i0+n]+=0.06*g*np.hanning(n)
# scan sound: pulsed tone
sc=np.sin(2*np.pi*620*tt)*(np.sin(2*np.pi*9*tt)>0.6)*0.05*((tt>SCAN_T)&(tt<LOCK_T))
# heartbeat pulse during scan
for hb in np.arange(SCAN_T,LOCK_T,0.62):
    for o,g in ((0,1.0),(0.16,0.6)):
        i0=int((hb+o)*SR); n=int(0.25*SR); x=np.arange(n)/SR
        mix[i0:i0+n]+=0.35*g*np.sin(2*np.pi*(55+25*np.exp(-x*30))*x)*np.exp(-x*14)
for tb in (13.05,13.55,14.05,14.55,15.05):
    i0=int(tb*SR); n=int(0.09*SR); x=np.arange(n)/SR
    mix[i0:i0+n]+=0.22*np.sin(2*np.pi*1850*x)*np.exp(-x*25)
# riser
m_=(tt>14.4)&(tt<LOCK_T); fr=300+1500*np.clip((tt-14.4)/(LOCK_T-14.4),0,1)**2
mix+=0.08*np.sin(2*np.pi*np.cumsum(fr)/SR)*m_*np.clip((tt-14.4)/1.1,0,1)
# lock alarm
for j in range(4):
    i0=int((LOCK_T+0.05+j*0.12)*SR); n=int(0.1*SR); x=np.arange(n)/SR
    mix[i0:i0+n]+=0.22*np.sin(2*np.pi*(880 if j%2==0 else 660)*x)*np.exp(-x*8)*np.minimum(1,x*400)
# voice
voice=np.zeros(NS)
for f,st in [(l[0],l[1]) for l in LINES]+[('v8.wav',16.05)]:
    sr,a=wav_read(S+f)
    a=np.interp(np.arange(0,len(a),sr/SR),np.arange(len(a)),a)
    a=a/ (np.max(np.abs(a))+1e-6)*0.9
    i0=int(st*SR); m=min(len(a),NS-i0); voice[i0:i0+m]+=a[:m]
# duck music under voice
venv=np.convolve(np.abs(voice),np.ones(4800)/4800,'same'); duck=1-0.55*np.clip(venv*6,0,1)
out=(music*duck+mix)*0.8+voice*0.95
out=out/ max(1.0,np.max(np.abs(out))/0.95)
st=np.stack([out,out],1)
st[:,0]+=0.0
pcm=(np.clip(st,-1,1)*32767).astype(np.int16)
with wave.open(S+'audio.wav','w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',S+'video_noaudio.mp4','-i',S+'audio.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart',S+'reel_alien_invasion.mp4'],check=True)
print('ok')
