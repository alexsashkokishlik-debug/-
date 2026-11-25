from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np, sys
src = Image.open('/root/.claude/uploads/15e9b8bd-6042-5d1d-b51f-045396c3a676/a920ac5d-image.jpg').convert('RGB').crop((2,0,874,1222))
def make(W,H,out):
    k = W/1280
    # background: blurred, darkened cover of the poster
    s = W/src.width
    bg = src.resize((W, round(src.height*s)), Image.LANCZOS)
    top = (bg.height-H)//2
    bg = bg.crop((0, top, W, top+H)).filter(ImageFilter.GaussianBlur(40*k))
    bg = ImageEnhance.Brightness(bg).enhance(0.8)
    tint = Image.new('RGB',(W,H),(60,18,34))
    bg = Image.blend(bg, tint, 0.5)
    # vignette
    yy,xx = np.mgrid[0:H,0:W]
    d = np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    v = np.clip(1-0.3*np.clip(d-0.4,0,None),0,1)[...,None]
    bg = Image.fromarray((np.asarray(bg)*v).astype(np.uint8))
    # grain
    rng = np.random.default_rng(1); n = rng.normal(0,5,(H,W,1))
    bg = Image.fromarray(np.clip(np.asarray(bg)+n,0,255).astype(np.uint8))
    # poster
    ph = round(664*k); pw = round(src.width*ph/src.height)
    p = src.resize((pw,ph), Image.LANCZOS)
    x = (W-pw)//2; y = (H-ph)//2
    sh = Image.new('L',(W,H),0); ImageDraw.Draw(sh).rectangle((x,y+round(8*k),x+pw,y+ph+round(8*k)),fill=170)
    sh = sh.filter(ImageFilter.GaussianBlur(18*k))
    bg = Image.composite(Image.new('RGB',(W,H),(10,2,5)), bg, sh)
    bg.paste(p,(x,y))
    bg.save(out, quality=95, optimize=True)
make(1280,720,'azbuka-opery-1280x720.jpg')
make(2560,1440,'azbuka-opery-2560x1440.jpg')
