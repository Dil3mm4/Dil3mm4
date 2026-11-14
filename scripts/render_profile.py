#!/usr/bin/env python3
"""Build dependency-free GitHub README SVG cards. Only Python stdlib is required."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# Shared palette: change it once, both cards change together.
C = {
    "bg": "#0B1422",
    "bg2": "#112339",
    "card": "#13263B",
    "card2": "#102035",
    "border": "#30475E",
    "border_hi": "#45677A",
    "grid": "#B3CADC",
    "cyan": "#6DE4D7",
    "blue": "#91AFFF",
    "white": "#EFF6FF",
    "body": "#CCD8E6",
    "muted": "#8DA6BE",
    "dark": "#0B1422",
}
FONT = "Arial,Helvetica,sans-serif"
MONO = "Consolas,Menlo,monospace"


def shared_defs() -> str:
    return f'''<defs>
  <linearGradient id="base" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{C['bg']}"/>
    <stop offset="1" stop-color="{C['bg2']}"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{C['cyan']}"/>
    <stop offset="1" stop-color="{C['blue']}"/>
  </linearGradient>
  <radialGradient id="halo"><stop offset="0" stop-color="{C['cyan']}" stop-opacity=".12"/>
    <stop offset="1" stop-color="{C['cyan']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="mesh" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="{C['grid']}" stroke-opacity=".055" stroke-width="1"/>
  </pattern>
</defs>'''


def backdrop(w: int, h: int) -> str:
    return f'''<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="23" fill="url(#base)" stroke="{C['border']}" stroke-width="2"/>
<rect x="2.5" y="2.5" width="{w-5}" height="{h-5}" rx="22" fill="url(#mesh)"/>
<path d="M27 43V{h-42}" stroke="url(#accent)" stroke-width="3" stroke-linecap="round"/>
<path d="M{w-76} 18h47v19M35 {h-22}h45" fill="none" stroke="{C['cyan']}" stroke-opacity=".4" stroke-width="1.6"/>'''


def t(x: float, y: float, s: object, size: int, color: str, weight: int = 400,
      *, mono: bool = False, anchor: str = "start", extra: str = "") -> str:
    return (f'<text x="{x}" y="{y}" font-family="{MONO if mono else FONT}" '
            f'font-size="{size}" fill="{color}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{escape(str(s))}</text>')


def hero() -> str:
    w, h = 1200, 434
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="title desc">',
        '<title id="title">Francesco Dil3mm4 Manzo, Android platform engineer</title>',
        '<desc id="desc">Custom Android platforms, low-level engineering, technical direction and product architecture. From Linux kernel to production.</desc>',
        shared_defs(), backdrop(w,h),
        '<ellipse cx="964" cy="222" rx="330" ry="245" fill="url(#halo)"/>',
        '<path d="M718 46V387" stroke="#456A78" stroke-opacity=".4" stroke-width="1" stroke-dasharray="4 9"/>',
        f'<rect x="52" y="43" width="49" height="49" rx="13" fill="{C["cyan"]}"/>',
        t(76.5,74,'D/',22,C['dark'],800,mono=True,anchor='middle'),
        t(119,61,'FRANCESCO  "DIL3MM4"  MANZO',18,C['white'],700,extra='letter-spacing=".35"'),
        t(120,85,'ANDROID PLATFORM ENGINEER  /  TECHNICAL LEAD',11,C['muted'],700,mono=True,extra='letter-spacing=".7"'),
        t(54,172,'I build Android',46,C['white'],750,extra='letter-spacing="-1.3"'),
        t(54,225,'from the kernel up.',45,C['cyan'],750,extra='letter-spacing="-1.4"'),
        t(56,278,'Custom Android platforms, low-level engineering,',16,C['body'],400),
        t(56,303,'technical direction and product architecture.',16,C['body'],400),
    ]
    pills = [('AOSP',85), ('LINUX',85), ('HAL / VENDOR',138), ('SECURITY',112), ('DEVICE BRING-UP',162)]
    x=55
    for label,width in pills:
        chunks += [f'<rect x="{x}" y="345" width="{width}" height="32" rx="8" fill="{C["card"]}" stroke="{C["border"]}"/>',
                   t(x+width/2,366,label,10,C['body'],700,mono=True,anchor='middle',extra='letter-spacing=".4"')]
        x += width+11
    chunks += [
       f'<rect x="752" y="41" width="405" height="348" rx="17" fill="{C["card2"]}" stroke="{C["border_hi"]}"/>',
       f'<circle cx="777" cy="66" r="4.5" fill="{C["cyan"]}"/>',
       f'<circle cx="792" cy="66" r="4.5" fill="{C["blue"]}" opacity=".55"/>',
       f'<circle cx="807" cy="66" r="4.5" fill="{C["muted"]}" opacity=".4"/>',
       t(828,71,'ANDROID / STACK',12,C['body'],700,mono=True,extra='letter-spacing="1"'),
       t(1138,71,'TOP  >  DOWN',10,C['muted'],400,mono=True,anchor='end'),
       f'<path d="M778 86h351" stroke="{C["border"]}"/>',
       f'<path d="M794 116V371" stroke="{C["blue"]}" stroke-opacity=".65" stroke-width="2"/>',
       f'<path d="m789 365 5 7 5-7" fill="none" stroke="{C["blue"]}" stroke-width="2"/>',
    ]
    rows=[
        ('01','LINUX KERNEL'),
        ('02','HAL / VENDOR'),
        ('03','NATIVE / ART'),
        ('04','FRAMEWORK + SERVICES'),
        ('05','APPS / SYSTEM UI'),
        ('06','PRODUCTION'),
    ]
    for i,(number,label) in enumerate(rows):
        y=95+i*48
        is_kernel=i==0
        is_production=i==len(rows)-1
        fill = '#173047' if (is_kernel or is_production) else C['card']
        line=C['cyan'] if (is_kernel or is_production) else C['border']
        chunks += [
           f'<rect x="820" y="{y}" width="310" height="42" rx="9" fill="{fill}" stroke="{line}" stroke-opacity=".9"/>',
           f'<circle cx="794" cy="{y+21}" r="5" fill="{C["cyan"] if (is_kernel or is_production) else C["blue"]}" opacity="{1 if (is_kernel or is_production) else .7}"/>',
           t(839,y+27,number,13,C['cyan'] if (is_kernel or is_production) else C['muted'],700,mono=True),
           f'<path d="M879 {y+10}v23" stroke="{C["border_hi"]}" stroke-opacity=".65"/>',
           t(899,y+27,label,13,C['white'] if (is_kernel or is_production) else C['body'],700,mono=True),
        ]
    chunks.append('</svg>')
    return '\n'.join(chunks)+'\n'


def format_num(n: int | None) -> str:
    return f"{n:,}" if n is not None else '—'


def stats_card(stats: dict | None = None) -> str:
    stats=stats or {}
    today=stats.get('updated_utc')
    w,h=1200,260
    known=all(isinstance(stats.get(k), int) for k in ('commits','repositories','stars','merge_percent','reviews'))
    fields=[
        ('PUBLIC COMMITS', format_num(stats.get('commits')), 'Search-indexed'),
        ('PUBLIC REPOS', format_num(stats.get('repositories')), 'Owned repositories'),
        ('STARS RECEIVED', format_num(stats.get('stars')), 'Across public repos'),
        ('PR MERGE RATE', f"{stats.get('merge_percent')}%" if stats.get('merge_percent') is not None else '—', 'Authored pull requests'),
        ('PRS REVIEWED', format_num(stats.get('reviews')), 'Public contributions'),
    ]
    chunks=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="title desc">',
            '<title id="title">Public GitHub activity statistics</title>',
            '<desc id="desc">Static self-hosted vector statistics that are regenerated daily by a Python script in this repository.</desc>',
            shared_defs(),backdrop(w,h),
            t(53,53,'GITHUB / PUBLIC ACTIVITY',16,C['white'],750,mono=True,extra='letter-spacing="1.15"'),
            f'<circle cx="1093" cy="47" r="4" fill="{C["cyan"] if known else C["blue"]}"/>',
            t(1137,52,'DAILY SYNC' if known else 'FIRST SYNC',11,C['muted'],700,mono=True,anchor='end'),
            f'<path d="M54 72H1146" stroke="{C["border"]}"/>',
            ]
    x0,width,gap=53,208,14
    for i,(label,value,detail) in enumerate(fields):
        x=x0+i*(width+gap)
        chunks += [
           f'<rect x="{x}" y="89" width="{width}" height="112" rx="12" fill="{C["card"]}" stroke="{C["border"]}"/>',
           f'<rect x="{x+12}" y="103" width="2" height="13" rx="1" fill="{C["cyan"] if i in (0,3) else C["blue"]}"/>',
           t(x+23,114,label,10,C['muted'],700,mono=True,extra='letter-spacing=".3"'),
           t(x+17,159,value,32,C['white'] if known else C['muted'],750),
           t(x+17,184,detail,11,C['muted']),
        ]
    footer = ('UPDATED ' + today + ' UTC' if known and today else 'RUN THE INCLUDED WORKFLOW TO POPULATE NUMBERS')
    chunks += [t(55,232,'PUBLIC REPOSITORIES & SEARCH-INDEXED ACTIVITY',10,C['muted'],600,mono=True),
               t(1142,232,footer,10,C['cyan'] if known else C['blue'],600,mono=True,anchor='end'),
               '</svg>']
    return '\n'.join(chunks)+'\n'


def write_if_changed(path:Path,content:str)->bool:
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_text('utf-8') == content:
        return False
    path.write_text(content,encoding='utf-8')
    return True


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--hero-only',action='store_true')
    args=p.parse_args()
    write_if_changed(ASSETS/'android-platform-card.svg',hero())
    if not args.hero_only:
        write_if_changed(ASSETS/'github-stats.svg',stats_card())


if __name__=='__main__':
    main()
