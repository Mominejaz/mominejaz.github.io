"""Build a two-page resume from Markdown, without changing other site assets."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate


INK = HexColor('#15263b')
ACCENT = HexColor('#176075')
MUTED = HexColor('#40556a')


def styles() -> dict[str, ParagraphStyle]:
    base = dict(allowWidows=0, allowOrphans=0)
    return {
        'name': ParagraphStyle('name', **base, fontName='Helvetica-Bold', textColor=INK, fontSize=25, leading=29, spaceAfter=5),
        'headline': ParagraphStyle('headline', **base, fontName='Helvetica-Bold', textColor=INK, fontSize=10.2, leading=14, spaceAfter=5),
        'contact': ParagraphStyle('contact', **base, fontName='Helvetica', fontSize=9.4, leading=13, textColor=MUTED, spaceAfter=11),
        'section': ParagraphStyle('section', **base, fontName='Helvetica-Bold', fontSize=10.6, leading=14, textColor=ACCENT, spaceBefore=13, spaceAfter=6, keepWithNext=True),
        'role': ParagraphStyle('role', **base, fontName='Helvetica-Bold', textColor=INK, fontSize=10.0, leading=13.3, spaceBefore=10, spaceAfter=3, keepWithNext=True),
        'date': ParagraphStyle('date', **base, fontName='Helvetica', fontSize=9.1, leading=12, textColor=MUTED, spaceAfter=4, keepWithNext=True),
        'body': ParagraphStyle('body', **base, fontName='Helvetica', textColor=INK, fontSize=9.6, leading=13.5, spaceAfter=7),
        'bullet': ParagraphStyle('bullet', **base, fontName='Helvetica', textColor=INK, fontSize=9.5, leading=13.2, leftIndent=10, firstLineIndent=-7, spaceAfter=4),
    }


def markup(value: str) -> str:
    value = escape(value.replace('\u2013', '-').replace('\u2014', '-').replace('\u2011', '-'))
    value = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', value)
    return re.sub(r'\[([^]]+)\]\((https?://[^)]+|mailto:[^)]+)\)',
                  lambda match: f'<link href="{match.group(2)}" color="#176075"><u>{match.group(1)}</u></link>', value)


def build(source: Path, destination: Path) -> None:
    lines = [line.strip() for line in source.read_text(encoding='utf-8').splitlines() if line.strip()]
    sheet = styles()
    story = []
    in_role = False
    for index, line in enumerate(lines):
        if line == '<!-- pagebreak -->':
            story.append(PageBreak())
            in_role = False
            continue
        if line.startswith('# '):
            kind, value = 'name', line[2:]
        elif line.startswith('## '):
            kind, value = 'section', line[3:].upper(); in_role = False
        elif line.startswith('### '):
            kind, value = 'role', line[4:]; in_role = True
        elif line.startswith('- '):
            kind, value = 'bullet', '- ' + line[2:]
        elif index == 1:
            kind, value = 'headline', line
        elif index == 2:
            kind, value = 'contact', line
        elif in_role:
            kind, value = 'date', line; in_role = False
        else:
            kind, value = 'body', line
        story.append(Paragraph(markup(value), sheet[kind]))

    def footer(canvas, document):
        canvas.setStrokeColor(HexColor('#cad4dc'))
        canvas.line(43, 39, 569, 39)
        canvas.setFillColor(MUTED)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(43, 26, 'Momin Ejaz  |  momin_e@hotmail.com  |  mominejaz.github.io')
        canvas.drawRightString(569, 26, str(document.page))
        canvas.linkURL('mailto:momin_e@hotmail.com', (101, 23, 190, 35), relative=0)
        canvas.linkURL('https://mominejaz.github.io/', (194, 23, 286, 35), relative=0)

    destination.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(destination), pagesize=letter, leftMargin=43,
                                 rightMargin=43, topMargin=38, bottomMargin=52,
                                 title='Momin Ejaz - Software Developer', author='Momin Ejaz')
    document.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    build(args.source, args.destination)
