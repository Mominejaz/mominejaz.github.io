"""Build the public resume and social image from reviewed local content."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from build_resume import build

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'dist/assets'
pdf = ASSETS / 'Momin-Ejaz-Resume.pdf'
build(ROOT / 'content/resume.md', pdf)

# A code-drawn typographic preview matches the site's existing identity.
im = Image.new('RGB', (1200, 630)); px = im.load()
for y in range(630):
    for x in range(1200):
        glow = max(0, 1 - ((x-1010)**2+(y-120)**2)**.5/1050)
        px[x,y] = (int(6+5*glow), int(9+29*glow), int(15+67*glow))
d=ImageDraw.Draw(im)
font=lambda size,bold=False: ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',size)
d.rounded_rectangle((850,115,1128,490),radius=16,outline='#39516c',width=2)
for i,t in enumerate(['01  Source data','02  Validation','03  Human review','04  Trusted output']):
    y=165+i*76;d.text((880,y),t,font=font(21),fill='#d9e6f5')
    if i<3:d.line((880,y+48,1098,y+48),fill='#39516c',width=1)
d.text((64,62),'MOMIN EJAZ / SOFTWARE DEVELOPER',font=font(21,True),fill='#ff965a')
for i,t in enumerate(['Software for real','operational work.']):d.text((60,190+i*82),t,font=font(66,True),fill='#f6f1e8')
d.text((64,400),'Applications. Automation. Data & reporting.',font=font(27),fill='#b9cce2')
d.line((64,515,1136,515),fill='#39516c',width=2)
d.text((64,551),'mominejaz.github.io',font=font(25,True),fill='#f6f1e8')
d.text((860,551),'ALBERTA, CANADA',font=font(18),fill='#b9cce2')
im.save(ASSETS/'social-preview.png',optimize=True)
print(pdf)
