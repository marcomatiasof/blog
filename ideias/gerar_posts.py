# -*- coding: utf-8 -*-
"""Gerador de imagens dos posts SPLINK — ilustração tech + headline.
Renderiza cada post em feed (4:5) e stories (9:16) com ilustração única do conceito."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC="imagens-posts"
FB="C:/Windows/Fonts/"
def font(n,s): return ImageFont.truetype(FB+n,s)

CY=(1,224,255); CY2=(0,150,210); RED=(255,82,82); GREEN=(37,211,102)
WHITE=(244,247,255); MUTE=(150,165,200); PAPER=(200,205,215)
BG_TOP=(8,12,24); BG_BOT=(16,26,54); INK=(4,7,16)

# ---- logo (recorte + keying do preto) ----
_raw=Image.open(os.path.join(SRC,"SPLINKAPP Logo.png")).convert("RGB"); _px=_raw.load()
_lw,_lh=_raw.size; LOGO=Image.new("RGBA",(_lw,_lh),(0,0,0,0)); _lp=LOGO.load()
for _y in range(_lh):
    for _x in range(_lw):
        r,g,b=_px[_x,_y]; lum=0.299*r+0.587*g+0.114*b
        a=0 if lum<=16 else 255 if lum>=55 else int((lum-16)/39*255)
        if a>0: _lp[_x,_y]=(r,g,b,a)
LOGO=LOGO.crop(LOGO.getbbox())

def gradient_bg(W,H):
    col=Image.new("RGB",(1,H))
    for y in range(H):
        t=(y/(H-1))**1.1
        col.putpixel((0,y),tuple(int(BG_TOP[i]+(BG_BOT[i]-BG_TOP[i])*t) for i in range(3)))
    base=col.resize((W,H)).convert("RGBA")
    glow=Image.new("L",(W,H),0); gd=ImageDraw.Draw(glow)
    gd.ellipse([W-650,-int(H*0.25),W+350,int(H*0.35)],fill=80)
    glow=glow.filter(ImageFilter.GaussianBlur(int(W*0.2)))
    base.alpha_composite(Image.composite(Image.new("RGBA",(W,H),CY+(255,)),
                         Image.new("RGBA",(W,H),(0,0,0,0)),glow.point(lambda v:int(v*0.45))))
    return base

def g_line(img,xy,color,w=8,blur=14,alpha=200):
    W,H=img.size; g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).line(xy,fill=color+(alpha,),width=w)
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).line(xy,fill=color+(255,),width=max(2,w-3))

def g_circle(img,box,color,alpha=120,blur=40):
    W,H=img.size; g=Image.new("L",(W,H),0); ImageDraw.Draw(g).ellipse(box,fill=alpha)
    img.alpha_composite(Image.composite(Image.new("RGBA",(W,H),color+(255,)),
                        Image.new("RGBA",(W,H),(0,0,0,0)),g.filter(ImageFilter.GaussianBlur(blur))))

def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        tt=(cur+" "+w).strip()
        if d.textlength(tt,font=f)<=mw:cur=tt
        else:
            if cur:out.append(cur)
            cur=w
    if cur:out.append(cur)
    return out

# ============ ILUSTRAÇÕES (desenham dentro de box=(x0,y0,x1,y1)) ============
def C(box): return ((box[0]+box[2])//2,(box[1]+box[3])//2)

def clock_cooling(img,d,box):
    cx,cy=C(box); r=min(box[2]-box[0],box[3]-box[1])//2-20
    g_circle(img,[cx-r,cy-r,cx+r,cy+r],CY,90,50)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=CY+(255,),width=9)
    for a in range(0,360,30):
        x1=cx+int((r-18)*math.cos(math.radians(a))); y1=cy+int((r-18)*math.sin(math.radians(a)))
        x2=cx+int((r-4)*math.cos(math.radians(a))); y2=cy+int((r-4)*math.sin(math.radians(a)))
        d.line([(x1,y1),(x2,y2)],fill=MUTE+(255,),width=4)
    g_line(img,[(cx,cy),(cx,cy-r+50)],RED,7,10,220)          # ponteiro
    g_line(img,[(cx,cy),(cx+r-90,cy+20)],RED,7,10,220)
    d.ellipse([cx-12,cy-12,cx+12,cy+12],fill=RED+(255,))

def hourglass_money(img,d,box):
    cx,cy=C(box); w=170; h=240; top=cy-h//2
    pts_top=[(cx-w//2,top),(cx+w//2,top),(cx+14,cy),(cx-14,cy)]
    pts_bot=[(cx-14,cy),(cx+14,cy),(cx+w//2,top+h),(cx-w//2,top+h)]
    g_line(img,[(cx-w//2-10,top),(cx+w//2+10,top)],CY,10,8,200)
    g_line(img,[(cx-w//2-10,top+h),(cx+w//2+10,top+h)],CY,10,8,200)
    d.line(pts_top+[pts_top[0]],fill=CY+(255,),width=7)
    d.line(pts_bot+[pts_bot[0]],fill=CY+(255,),width=7)
    d.polygon([(cx-w//2+18,top+14),(cx+w//2-18,top+14),(cx+10,cy-8),(cx-10,cy-8)],fill=CY+(120,))
    d.line([(cx,cy),(cx,cy+70)],fill=CY+(255,),width=4)  # areia caindo
    # moedas $ embaixo
    f=font("ariblk.ttf",54)
    for i,(dx,dy) in enumerate([(-60,90),(0,120),(70,95),(-10,170)]):
        d.text((cx+dx,top+h+dy),"$",font=f,fill=GREEN+(max(120,255-i*30),))

def split(img,d,box,red_left=True):
    x0,y0,x1,y1=box; mid=(x0+x1)//2
    ov=Image.new("RGBA",img.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rectangle([x0,y0,mid,y1],fill=(60,18,22,110)); img.alpha_composite(ov)
    random.seed(3)
    for _ in range(9):
        w=random.randint(90,150);h=random.randint(60,90)
        px=random.randint(x0+10,mid-w-10);py=random.randint(y0+10,y1-h-10)
        pap=Image.new("RGBA",(w,h),(*PAPER,70)).rotate(random.randint(-22,22),expand=True)
        img.alpha_composite(pap,(px,py))
    g_line(img,[(x0+30,y0+90),(mid-160,y0+170),(mid-90,y0+120),(mid-30,y1-90)],RED,9,10,220)
    base=y1-30; bw=46; gap=34; hs=[90,150,220,300]
    for i,bh in enumerate(hs):
        bx=mid+50+i*(bw+gap); d.rounded_rectangle([bx,base-bh,bx+bw,base],radius=8,fill=CY+(235,))
    g_line(img,[(mid,y0),(mid,y1)],CY,4,12,150)

def spreadsheet(img,d,box):
    x0,y0,x1,y1=box; cols=6; rows=7; cw=(x1-x0)//cols; rh=(y1-y0)//rows
    for c in range(cols+1): d.line([(x0+c*cw,y0),(x0+c*cw,y1)],fill=(70,85,120,255),width=2)
    for r in range(rows+1): d.line([(x0,y0+r*rh),(x1,y0+r*rh)],fill=(70,85,120,255),width=2)
    random.seed(9)
    for _ in range(16):
        c=random.randint(0,cols-1);r=random.randint(0,rows-1)
        d.rectangle([x0+c*cw+6,y0+r*rh+10,x0+c*cw+cw-8,y0+r*rh+rh-12],fill=(120,130,160,120))
    # X vermelho de erro
    g_line(img,[(x0+30,y0+30),(x1-30,y1-30)],RED,8,12,200)
    g_line(img,[(x1-30,y0+30),(x0+30,y1-30)],RED,8,12,200)

def dashboard(img,d,box):
    x0,y0,x1,y1=box
    d.rounded_rectangle([x0,y0,x1,y1],radius=22,fill=(18,30,60,235),outline=(50,70,120,255),width=2)
    px0,py1=x0+50,y1-60; px1,py0=x1-50,y0+90
    for gy in range(5):
        yy=py0+(py1-py0)*gy//4; d.line([(px0,yy),(px1,yy)],fill=(45,62,100,255),width=1)
    pts=[(px0,py1-30),(px0+170,py1-110),(px0+330,py1-90),(px0+470,py1-200),(px1,py1-300)]
    g_line(img,pts,CY,7,10,230)
    for p in pts: d.ellipse([p[0]-7,p[1]-7,p[0]+7,p[1]+7],fill=WHITE+(255,))
    d.text((x0+50,y0+30),"CONVERSÕES • TEMPO REAL",font=font("segoeuib.ttf",26),fill=MUTE)

def chairs_chip(img,d,box):
    x0,y0,x1,y1=box; cy=(y0+y1)//2
    for i in range(3):
        cx=x0+60+i*120
        d.rounded_rectangle([cx-34,cy-10,cx+34,cy+70],radius=10,outline=(110,125,160,255),width=6)
        d.line([(cx-34,cy-10),(cx-34,cy-70)],fill=(110,125,160,255),width=6)
        d.arc([cx-34,cy-90,cx+34,cy-10],180,360,fill=(110,125,160,255),width=6)
    ax=x0+390
    g_line(img,[(ax,cy+20),(ax+80,cy+20)],CY,7,8,220)
    d.polygon([(ax+80,cy+5),(ax+120,cy+20),(ax+80,cy+35)],fill=CY+(255,))
    chx=x1-120
    g_circle(img,[chx-90,cy-90,chx+90,cy+90],CY,120,40)
    d.rounded_rectangle([chx-60,cy-60,chx+60,cy+60],radius=12,fill=(10,30,50,255),outline=CY+(255,),width=6)
    for k in range(-2,3):
        d.line([(chx+k*24,cy-60),(chx+k*24,cy-82)],fill=CY+(255,),width=5)
        d.line([(chx+k*24,cy+60),(chx+k*24,cy+82)],fill=CY+(255,),width=5)
        d.line([(chx-60,cy+k*24),(chx-82,cy+k*24)],fill=CY+(255,),width=5)
        d.line([(chx+60,cy+k*24),(chx+82,cy+k*24)],fill=CY+(255,),width=5)
    d.text((chx-22,cy-26),"IA",font=font("ariblk.ttf",46),fill=CY+(255,))

def phone_down(img,d,box):
    cx,cy=C(box)
    d.rounded_rectangle([cx-70,cy-130,cx+70,cy+130],radius=24,fill=(16,24,44,255),outline=(80,95,130,255),width=6)
    d.line([(cx-30,cy+150),(cx+30,cy+150)],fill=(80,95,130,255),width=6)
    g_circle(img,[cx-180,cy-200,cx+40,cy+20],CY,70,60)  # calmo
    for i,rr in enumerate([60,110,160]):
        d.arc([cx-rr,cy-rr,cx+rr,cy+rr],300,360,fill=CY+(max(60,200-i*60),),width=5)
    d.text((cx-95,cy+185),"modo silencioso",font=font("segoeuii.ttf",30),fill=MUTE)

def percent(img,d,box,txt="40%"):
    x0,y0,x1,y1=box
    base=y1-20; bw=60; gap=40; hs=[120,200,300,420]
    for i,bh in enumerate(hs):
        bx=x1-260+i*(bw+gap)-120
        d.rounded_rectangle([bx,base-bh,bx+bw,base],radius=8,fill=(60,80,120,200) if i<3 else CY+(235,))
    g_circle(img,[x0,y0,x0+360,y0+360],CY,110,45)
    d.text((x0+20,y0+20),txt,font=font("ariblk.ttf",200),fill=WHITE+(255,))

def shield(img,d,box):
    cx,cy=C(box); w=190;h=240
    pts=[(cx,cy-h//2),(cx+w//2,cy-h//2+40),(cx+w//2,cy+30),(cx,cy+h//2),(cx-w//2,cy+30),(cx-w//2,cy-h//2+40)]
    g_circle(img,[cx-150,cy-150,cx+150,cy+150],CY,90,50)
    d.polygon(pts,outline=CY+(255,),width=8,fill=(10,30,50,180))
    # check
    g_line(img,[(cx-50,cy),(cx-10,cy+45),(cx+60,cy-50)],CY,12,8,230)
    # X vermelho saindo (bloqueio repelido)
    d.text((cx+w//2+30,cy-40),"BAN",font=font("ariblk.ttf",40),fill=RED+(150,))
    g_line(img,[(cx+w//2+20,cy-50),(cx+w//2+150,cy-90)],RED,6,8,120)

def scale10x(img,d,box):
    x0,y0,x1,y1=box
    g_line(img,[(x0+40,y1-40),(x1-200,y0+60)],CY,10,12,230)
    d.polygon([(x1-220,y0+90),(x1-160,y0+30),(x1-150,y0+110)],fill=CY+(255,))
    g_circle(img,[x0,y1-260,x0+360,y1+100],CY,90,45)
    d.text((x0+30,y1-260),"10x",font=font("ariblk.ttf",170),fill=WHITE+(255,))

def thermometer(img,d,box):
    cx,cy=C(box); top=cy-150; bot=cy+150
    d.rounded_rectangle([cx-26,top,cx+26,bot],radius=26,outline=(90,105,140,255),width=6)
    g_circle(img,[cx-70,bot-70,cx+70,bot+70],RED,120,40)
    d.ellipse([cx-46,bot-46,cx+46,bot+46],fill=RED+(255,))
    d.rounded_rectangle([cx-14,cy-20,cx+14,bot-10],radius=14,fill=RED+(255,))
    # gradiente quente->frio nas marcas
    for i in range(6):
        yy=top+20+i*((bot-top-40)//5)
        col=RED if i<2 else (CY if i>3 else MUTE)
        d.line([(cx+34,yy),(cx+64,yy)],fill=col+(255,),width=5)

def balance(img,d,box):
    cx,cy=C(box); top=cy-150
    d.line([(cx,top),(cx,cy+120)],fill=(110,125,160,255),width=8)
    d.line([(cx-180,top+20),(cx+180,top+20)],fill=(110,125,160,255),width=8)
    # prato esquerdo: crachá + $
    lx=cx-180
    d.line([(lx,top+20),(lx,top+90)],fill=(110,125,160,255),width=4)
    d.rounded_rectangle([lx-60,top+90,lx+60,top+170],radius=10,fill=(40,55,90,255),outline=MUTE+(255,),width=3)
    d.text((lx-46,top+108),"SDR",font=font("segoeuib.ttf",34),fill=MUTE)
    # prato direito: chip
    rx=cx+180
    d.line([(rx,top+20),(rx,top+90)],fill=(110,125,160,255),width=4)
    g_circle(img,[rx-80,top+80,rx+80,top+240],CY,100,40)
    d.rounded_rectangle([rx-55,top+95,rx+55,top+205],radius=10,fill=(10,30,50,255),outline=CY+(255,),width=5)
    d.text((rx-26,top+120),"IA",font=font("ariblk.ttf",40),fill=CY+(255,))

def chain_phone(img,d,box):
    cx,cy=C(box)
    d.rounded_rectangle([cx-70,cy-140,cx+70,cy+140],radius=24,fill=(16,24,44,255),outline=(90,105,140,255),width=6)
    d.text((cx-44,cy-30),"24/7",font=font("ariblk.ttf",48),fill=RED+(255,))
    # corrente
    for i in range(6):
        yy=cy+120+i*0;
    for i in range(5):
        ex=cx-200+i*40
        d.ellipse([ex,cy+150,ex+44,cy+186],outline=MUTE+(255,),width=7)
    d.ellipse([cx-90,cy+120,cx-50,cy+160],outline=RED+(255,),width=7)

def dead_chats(img,d,box):
    x0,y0,x1,y1=box; random.seed(5); cols=3
    for i in range(7):
        bx=x0+30+(i%cols)*((x1-x0-60)//cols); by=y0+20+(i//cols)*150
        w=(x1-x0-60)//cols-30; col=(70,80,105,200)
        d.rounded_rectangle([bx,by,bx+w,by+90],radius=16,fill=col)
        d.polygon([(bx+20,by+90),(bx+50,by+90),(bx+20,by+120)],fill=col)
    # um aceso ao fundo
    d.rounded_rectangle([x1-220,y1-130,x1-40,y1-40],radius=16,fill=CY+(235,))
    d.polygon([(x1-200,y1-40),(x1-170,y1-40),(x1-200,y1-12)],fill=CY+(235,))

def inbox_badge(img,d,box):
    cx,cy=C(box)
    d.rounded_rectangle([cx-150,cy-110,cx+150,cy+110],radius=20,fill=(16,26,50,255),outline=(70,90,130,255),width=5)
    d.polygon([(cx-150,cy-110),(cx,cy+10),(cx+150,cy-110)],outline=(70,90,130,255),width=5)
    g_circle(img,[cx+70,cy-180,cx+230,cy-20],RED,140,30)
    d.ellipse([cx+90,cy-160,cx+220,cy-30],fill=RED+(255,))
    d.text((cx+110,cy-150),"+347",font=font("ariblk.ttf",46),fill=WHITE+(255,))

def mechanism4(img,d,box):
    x0,y0,x1,y1=box; labels=["EXTRAIR","DISPARAR","QUALIFICAR","ORGANIZAR"]
    cy=(y0+y1)//2; bw=180; gap=((x1-x0)-2*bw)//1  # 2 por linha
    pos=[(x0+10,cy-150),(x1-bw-10,cy-150),(x0+10,cy+30),(x1-bw-10,cy+30)]
    for i,(bx,by) in enumerate(pos):
        g_circle(img,[bx-10,by-10,bx+bw+10,by+120+10],CY,60,30)
        d.rounded_rectangle([bx,by,bx+bw,by+120],radius=14,fill=(12,30,52,255),outline=CY+(255,),width=4)
        d.text((bx+20,by+44),labels[i],font=font("segoeuib.ttf",30),fill=CY+(255,))
    g_line(img,[(x0+bw+10,cy-90),(x1-bw-10,cy-90)],CY,5,8,180)
    g_line(img,[(x1-bw//2-10,cy-30),(x1-bw//2-10,cy+30)],CY,5,8,180)
    g_line(img,[(x1-bw-10,cy+90),(x0+bw+10,cy+90)],CY,5,8,180)

def crm_kanban(img,d,box):
    x0,y0,x1,y1=box; cols=4; cw=(x1-x0)//cols
    for c in range(cols):
        cx0=x0+c*cw+10
        d.rounded_rectangle([cx0,y0,cx0+cw-20,y1],radius=14,fill=(16,26,48,255),outline=(50,70,110,255),width=2)
        d.rectangle([cx0,y0,cx0+cw-20,y0+12],fill=CY+(255,))
        for k in range(random.randint(1,3)):
            cy0=y0+40+k*70
            d.rounded_rectangle([cx0+14,cy0,cx0+cw-34,cy0+50],radius=8,fill=(40,60,95,255))
    random.seed(2)

def chat_heart(img,d,box):
    cx,cy=C(box)
    d.rounded_rectangle([cx-160,cy-110,cx+160,cy+90],radius=28,fill=(16,28,52,255),outline=CY+(255,),width=5)
    d.polygon([(cx-60,cy+90),(cx-10,cy+90),(cx-60,cy+150)],fill=(16,28,52,255))
    # coração + circuito
    hx,hy=cx,cy-10
    d.pieslice([hx-70,hy-50,hx,hy+10],0,360,fill=RED+(230,))
    d.pieslice([hx,hy-50,hx+70,hy+10],0,360,fill=RED+(230,))
    d.polygon([(hx-66,hy-12),(hx+66,hy-12),(hx,hy+70)],fill=RED+(230,))
    g_line(img,[(hx-90,hy+20),(hx-50,hy+20),(hx-30,hy-10),(hx+10,hy+40),(hx+40,hy),(hx+90,hy)],CY,5,6,220)

def stopwatch(img,d,box,txt="00:03"):
    cx,cy=C(box); r=150
    g_circle(img,[cx-r,cy-r,cx+r,cy+r],CY,100,45)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=CY+(255,),width=10)
    d.line([(cx-30,cy-r-26),(cx+30,cy-r-26)],fill=CY+(255,),width=10)
    d.line([(cx,cy-r-26),(cx,cy-r)],fill=CY+(255,),width=8)
    d.text((cx-110,cy-44),txt,font=font("ariblk.ttf",84),fill=WHITE+(255,))

def many_shielded(img,d,box):
    x0,y0,x1,y1=box; random.seed(11)
    for _ in range(22):
        bx=random.randint(x0,x1-50);by=random.randint(y0,y1-40)
        d.rounded_rectangle([bx,by,bx+44,by+34],radius=8,fill=CY+(random.randint(120,235),))
        d.polygon([(bx+8,by+34),(bx+24,by+34),(bx+8,by+50)],fill=CY+(180,))
    cx,cy=C(box)
    g_circle(img,[cx-140,cy-140,cx+140,cy+140],CY,70,50)
    d.arc([cx-130,cy-150,cx+130,cy+150],150,390,fill=WHITE+(220,),width=8)

def caseline(img,d,box):
    x0,y0,x1,y1=box
    d.line([(x0+30,y0+30),(x0+30,y1-40)],fill=(60,80,120,255),width=3)
    d.line([(x0+30,y1-40),(x1-30,y1-40)],fill=(60,80,120,255),width=3)
    pts=[(x0+30,y1-80),(x0+180,y1-130),(x0+330,y1-110),(x0+470,y1-230),(x1-40,y1-330)]
    g_line(img,pts,CY,8,10,230)
    for p in pts: d.ellipse([p[0]-8,p[1]-8,p[0]+8,p[1]+8],fill=WHITE+(255,))
    d.text((x0+40,y0+10),"ANTES",font=font("segoeuib.ttf",26),fill=RED+(255,))
    d.text((x1-150,y1-380),"DEPOIS",font=font("segoeuib.ttf",26),fill=CY+(255,))

def grid1000(img,d,box):
    x0,y0,x1,y1=box; cols=14; rows=8; random.seed(4)
    cw=(x1-x0)//cols; rh=(y1-y0)//rows
    for r in range(rows):
        for c in range(cols):
            on=random.random()<0.18
            cx=x0+c*cw+cw//2; cy=y0+r*rh+rh//2
            col=CY+(235,) if on else (60,75,110,200)
            d.ellipse([cx-9,cy-9,cx+9,cy+9],fill=col)

def skyline(img,d,box):
    x0,y0,x1,y1=box; random.seed(8)
    g_circle(img,[x1-260,y0-40,x1-40,y0+180],CY,90,50)  # sol
    bx=x0+20
    while bx<x1-20:
        bw=random.randint(50,90); bh=random.randint(120,300)
        d.rectangle([bx,y1-bh,bx+bw,y1],fill=(20,34,62,255),outline=(45,65,105,255),width=2)
        for wy in range(y1-bh+20,y1-20,40):
            for wx in range(bx+12,bx+bw-12,28):
                if random.random()<0.5: d.rectangle([wx,wy,wx+10,wy+16],fill=CY+(120,))
        bx+=bw+18
    g_line(img,[(x0+30,y1-60),(x1-60,y0+120)],CY,6,10,200)
    d.polygon([(x1-90,y0+150),(x1-50,y0+105),(x1-40,y0+185)],fill=CY+(255,))

def funnel_hole(img,d,box):
    x0,y0,x1,y1=box; cx=(x0+x1)//2; topw=420; topy=y0+30; midy=y0+260; midw=120; stemy=y1-20
    d.polygon([(cx-topw//2,topy),(cx+topw//2,topy),(cx+midw//2,midy),(cx-midw//2,midy)],outline=CY+(255,),width=8)
    d.rectangle([cx-midw//2,midy,cx+midw//2,stemy],outline=CY+(255,),width=8)
    random.seed(7)
    for _ in range(20):
        x=random.randint(cx-topw//2+20,cx+topw//2-20);y=random.randint(topy-90,topy+30)
        d.ellipse([x,y,x+12,y+12],fill=WHITE+(200,))
    hx,hy=cx+midw//2,midy+90
    d.ellipse([hx-12,hy-22,hx+26,hy+22],fill=INK+(255,))
    d.arc([hx-12,hy-22,hx+26,hy+22],-90,90,fill=RED+(255,),width=7)
    f=font("ariblk.ttf",40)
    for i,(dx,dy) in enumerate([(50,30),(95,95),(150,170)]):
        d.text((hx+dx,hy+dy),"$",font=f,fill=RED+(max(70,230-i*55),))

def seed(img,d,box):
    cx,cy=C(box)
    d.line([(cx-120,cy+150),(cx+120,cy+150)],fill=(80,95,130,255),width=6)  # solo
    g_line(img,[(cx,cy+150),(cx,cy-60)],GREEN,7,8,200)                       # caule
    d.ellipse([cx-70,cy-110,cx-10,cy-50],fill=GREEN+(220,))                  # folhas
    d.ellipse([cx+10,cy-130,cx+80,cy-60],fill=GREEN+(220,))
    # seta de crescimento à direita
    g_line(img,[(cx+150,cy+120),(cx+150,cy-100)],CY,7,8,210)
    d.polygon([(cx+128,cy-70),(cx+150,cy-120),(cx+172,cy-70)],fill=CY+(255,))

def calendar_crumble(img,d,box):
    cx,cy=C(box); w=300;h=260; x0=cx-w//2;y0=cy-h//2
    d.rounded_rectangle([x0,y0,x0+w,y0+h],radius=18,fill=(16,28,52,255),outline=(70,90,130,255),width=5)
    d.rectangle([x0,y0,x0+w,y0+54],fill=CY+(255,))
    d.line([(x0+70,y0-24),(x0+70,y0+20)],fill=MUTE+(255,),width=8)
    d.line([(x0+w-70,y0-24),(x0+w-70,y0+20)],fill=MUTE+(255,),width=8)
    random.seed(6)
    for r in range(3):
        for c in range(5):
            bx=x0+30+c*52; by=y0+80+r*54
            if random.random()<0.4: continue  # dias "caindo"
            d.rounded_rectangle([bx,by,bx+38,by+38],radius=6,fill=(50,68,105,255))
    for _ in range(14):  # partículas caindo
        px=random.randint(x0,x0+w);py=random.randint(y0+h,y0+h+150)
        d.rectangle([px,py,px+12,py+12],fill=(50,68,105,180))

def magnifier(img,d,box):
    x0,y0,x1,y1=box
    d.rounded_rectangle([x0,y0,x1-40,y1-40],radius=18,fill=(16,28,52,235),outline=(50,70,110,255),width=2)
    pts=[(x0+60,y1-100),(x0+180,y1-160),(x0+300,y1-130),(x0+430,y1-220)]
    g_line(img,pts,CY,5,8,180)
    random.seed(12)
    for i in range(5):
        col=RED if i%2 else GREEN
        d.ellipse([x0+70+i*90,y0+70,x0+96+i*90,y0+96],fill=col+(255,))
    cx,cy=x1-150,y1-150; r=90
    g_circle(img,[cx-r,cy-r,cx+r,cy+r],CY,90,30)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=WHITE+(255,),width=10)
    d.line([(cx+int(r*0.7),cy+int(r*0.7)),(cx+r+60,cy+r+60)],fill=WHITE+(255,),width=14)

def portal(img,d,box):
    cx,cy=C(box)
    for i,rr in enumerate([200,150,100,55]):
        g_circle(img,[cx-rr,cy-rr,cx+rr,cy+rr],CY,60-i*8,40)
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=CY+(255-i*30,),width=8)
    d.polygon([(cx-26,cy-30),(cx+34,cy),(cx-26,cy+30)],fill=WHITE+(255,))  # play / avançar

CONCEPTS=dict(clock_cooling=clock_cooling,hourglass_money=hourglass_money,split=split,
 spreadsheet=spreadsheet,dashboard=dashboard,chairs_chip=chairs_chip,phone_down=phone_down,
 percent=percent,shield=shield,scale10x=scale10x,thermometer=thermometer,balance=balance,
 chain_phone=chain_phone,dead_chats=dead_chats,inbox_badge=inbox_badge,mechanism4=mechanism4,
 crm_kanban=crm_kanban,chat_heart=chat_heart,stopwatch=stopwatch,many_shielded=many_shielded,
 caseline=caseline,grid1000=grid1000,skyline=skyline,funnel_hole=funnel_hole,seed=seed,
 calendar_crumble=calendar_crumble,magnifier=magnifier,portal=portal)

# ============ COMPOSIÇÃO ============
def render(spec, fmt, outdir):
    concept,label,angle,headline=spec
    if fmt=="feed":
        W,H=1080,1350; art=(80,180,W-80,680); ky=720; tx0=80; t_top=772; cta_y=H-150; dom_y=H-66
    else:
        W,H=1080,1920; art=(80,330,W-80,1020); ky=1110; tx0=80; t_top=1166; cta_y=1560; dom_y=cta_y+118
    img=gradient_bg(W,H); d=ImageDraw.Draw(img,"RGBA")
    # ilustração
    CONCEPTS[concept](img,d,art); d=ImageDraw.Draw(img,"RGBA")
    # scrim para legibilidade do texto
    sc=Image.new("L",(W,H),0); sd=ImageDraw.Draw(sc); start=int(H*0.46)
    for y in range(start,H): sd.line([(0,y),(W,y)],fill=int(230*((y-start)/(H-start))))
    img.alpha_composite(Image.composite(Image.new("RGBA",(W,H),INK+(255,)),Image.new("RGBA",(W,H),(0,0,0,0)),sc))
    d=ImageDraw.Draw(img,"RGBA")
    # logo + label
    rr=58/LOGO.height; lg=LOGO.resize((int(LOGO.width*rr),58),Image.LANCZOS)
    img.alpha_composite(lg,(80,70 if fmt=="feed" else 200))
    f_num=font("segoeuib.ttf",30)
    d.text((W-80-d.textlength(label.upper(),font=f_num),(84 if fmt=="feed" else 214)),label.upper(),font=f_num,fill=MUTE)
    # kicker + headline (auto-fit no espaço disponível)
    d.text((tx0,ky),angle.upper(),font=font("segoeuib.ttf",34),fill=CY)
    avail=cta_y-40-t_top; max_w=W-2*tx0; size=86
    while size>42:
        f=font("ariblk.ttf",size); lines=wrap(d,headline,f,max_w); lh=int(size*1.13)
        if len(lines)*lh<=avail and len(lines)<=7: break
        size-=3
    y=t_top
    for ln in lines: d.text((tx0,y),ln,font=f,fill=WHITE); y+=lh
    # CTA
    f_cta=font("segoeuib.ttf",36); cta="FAÇA O DIAGNÓSTICO  ›  LINK NA BIO"
    tw=d.textlength(cta,font=f_cta); pad=34
    d.rounded_rectangle([tx0,cta_y,tx0+tw+pad*2,cta_y+88],radius=14,fill=CY)
    d.text((tx0+pad,cta_y+24),cta,font=f_cta,fill=INK)
    d.text((tx0,dom_y),"splinkapp.com.br",font=font("segoeui.ttf",30),fill=MUTE)
    img.convert("RGB").save(os.path.join(outdir,fmt and ""),"PNG") if False else None
    return img.convert("RGB")

POSTS={
 "post-01":("clock_cooling","Post 01","Problema invisível","Não é seu produto que não vende. É o tempo que seu lead espera resposta."),
 "post-02":("hourglass_money","Post 02","Tensão","Cada lead que espera 10 minutos por resposta já é dinheiro saindo da sua conta."),
 "post-03":("split","Post 03","Comparação","Um atende 8h por dia. O outro qualifica 1.000 leads enquanto você dorme."),
 "post-04":("spreadsheet","Post 04","Inimigo comum","O vilão da sua escala é a planilha que você ainda usa pra prospectar."),
 "post-05":("dashboard","Post 05","Autoridade","Enquanto você lê isso, esse painel fechou 3 conversas. Sem ninguém na cadeira."),
 "post-06":("chairs_chip","Post 06","Big idea","Contratar mais vendedor pra escalar é o conselho mais caro que já te deram."),
 "post-07":("phone_down","Post 07","Desejo","Tirei o WhatsApp da mão e as vendas subiram."),
 "post-08":("percent","Post 08","Prova","Perdíamos 40% dos leads por demora. Hoje a IA qualifica tudo em segundos."),
 "post-09":("shield","Post 09","Quebra de crença","Disparo em massa derruba o número de quem não tem o protocolo certo."),
 "post-10":("scale10x","Post 10","CTA","Sua operação aguenta 10x mais leads amanhã?"),
 "cal-01-S1-Seg":("thermometer","S1 · Seg","Problema invisível","Seu lead não some. Ele esfria — e você nem percebe a hora."),
 "cal-02-S1-Ter":("balance","S1 · Ter","Custo oculto","Você não paga só o salário do SDR. Paga tudo que ele não consegue fazer."),
 "cal-03-S1-Qua":("chain_phone","S1 · Qua","Inimigo comum","Estar sempre disponível não é compromisso. É a sua maior fraqueza."),
 "cal-04-S1-Qui":("dead_chats","S1 · Qui","Tensão","A maioria das suas vendas morre no follow-up que ninguém fez."),
 "cal-05-S1-Sex":("inbox_badge","S1 · Sex","Provocação","Quantos leads do mês passado você simplesmente nunca respondeu?"),
 "cal-06-S2-Seg":("mechanism4","S2 · Seg","Mecanismo","A anatomia de uma operação de vendas que não dorme."),
 "cal-07-S2-Ter":("crm_kanban","S2 · Ter","Autoridade","Se o seu funil mora na sua cabeça, ele já está vazando."),
 "cal-08-S2-Qua":("chat_heart","S2 · Qua","Quebra de crença","O cliente percebe a demora de quem não usa IA."),
 "cal-09-S2-Qui":("stopwatch","S2 · Qui","Bastidor","O que acontece nos 3 primeiros segundos define se o lead compra."),
 "cal-10-S2-Sex":("many_shielded","S2 · Sex","Escala segura","Falar com mil pessoas por dia não é sorte. É protocolo."),
 "cal-11-S3-Seg":("caseline","S3 · Seg","Estudo de caso","De 40% de leads perdidos para qualificação em segundos. Sem trocar o time."),
 "cal-12-S3-Ter":("split","S3 · Ter","Comparação","A mesma empresa, dois cenários. A diferença é a estrutura."),
 "cal-13-S3-Qua":("phone_down","S3 · Qua","Desejo","O domingo em que eu não toquei no WhatsApp foi o que mais vendeu."),
 "cal-14-S3-Qui":("grid1000","S3 · Qui","Prova de volume","Sua operação fala com 30 pessoas por dia. E se falasse com 1.000?"),
 "cal-15-S3-Sex":("skyline","S3 · Sex","Visão de futuro","Imagine sua operação daqui a 90 dias — atendendo sozinha, em escala."),
 "cal-16-S4-Seg":("funnel_hole","S4 · Seg","Big idea","Seu funil não tem furo de conversão. Tem furo de resposta."),
 "cal-17-S4-Ter":("seed","S4 · Ter","Objeção","Minha empresa é pequena demais pra automação? É o contrário."),
 "cal-18-S4-Qua":("calendar_crumble","S4 · Qua","Urgência","Cada semana sem estrutura é mais uma semana de leads vazando."),
 "cal-19-S4-Qui":("magnifier","S4 · Qui","Diagnóstico","O diagnóstico mostra onde sua operação quebraria sob 10x mais leads."),
 "cal-20-S4-Sex":("portal","S4 · Sex","Convite final","Sua operação está pronta pra escalar — ou só pra continuar como está?"),
}

if __name__=="__main__":
    os.makedirs("imagens-posts",exist_ok=True); os.makedirs("imagens-stories",exist_ok=True)
    n=0
    for key,spec in POSTS.items():
        render(spec,"feed","imagens-posts").save(f"imagens-posts/{key}.png","PNG")
        render(spec,"story","imagens-stories").save(f"imagens-stories/story-{key}.png","PNG")
        n+=1
    print("Renderizados:",n,"posts × 2 formatos =",n*2,"imagens")
