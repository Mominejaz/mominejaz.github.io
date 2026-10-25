"""Build the public resume and social image from reviewed local content."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'dist/assets'
styles = {
    'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=HexColor('#102842'), spaceAfter=9),
    'section': ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=HexColor('#176075'), spaceBefore=13, spaceAfter=6, keepWithNext=True),
    'role': ParagraphStyle('role', fontName='Helvetica-Bold', fontSize=10.5, leading=14, spaceBefore=9, spaceAfter=4, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13, spaceAfter=6, textColor=HexColor('#243447')),
    'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.5, leading=13, leftIndent=10, firstLineIndent=-8, spaceAfter=4, textColor=HexColor('#243447')),
}
def markup(text):
    text = escape(text.replace('\u2013', '-').replace('\u2014', '-').replace('\u2011', '-'))
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

story = []
for line in (ROOT / 'content/resume.md').read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith('### Pine Profiles'):
        story.extend([PageBreak(), Paragraph('EXPERIENCE / CONTINUED', styles['section'])])
    if line.startswith('# '):
        style, text = 'name', line[2:]
    elif line.startswith('## '):
        style, text = 'section', line[3:].upper()
    elif line.startswith('### '):
        style, text = 'role', line[4:]
    elif line.startswith('- '):
        style, text = 'bullet', '- ' + line[2:]
    else:
        style, text = 'body', line
    story.append(Paragraph(markup(text), styles[style]))

def footer(canvas, doc):
    canvas.setStrokeColor(HexColor('#cad4dc'))
    canvas.line(43, 40, 569, 40)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(HexColor('#526579'))
    canvas.drawString(43, 26, 'Momin Ejaz  |  momin_e@hotmail.com  |  mominejaz.github.io')
    canvas.drawRightString(569, 26, str(doc.page))
    canvas.linkURL('https://mominejaz.github.io/', (270, 22, 420, 36), relative=0)

pdf = ASSETS / 'Momin-Ejaz-Resume.pdf'
SimpleDocTemplate(str(pdf), pagesize=(612, 792), rightMargin=43, leftMargin=43,
                  topMargin=38, bottomMargin=55, title='Momin Ejaz - Software Developer',
                  author='Momin Ejaz').build(story, onFirstPage=footer, onLaterPages=footer)

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
