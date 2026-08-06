#!/usr/bin/env python3
"""Burn SRT captions onto scene images using PIL (no libass/drawtext needed).
Reads a manifest + SRT, finds which caption falls in each scene, and writes one
PNG per caption (scene background + caption text). Emits a new manifest where
each caption is its own scene with the caption's duration.

Usage: python3 burn_captions.py manifest.json captions.srt out_manifest.json [out_dir]
"""
import argparse, json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

def parse_srt(path):
    txt = open(path, encoding='utf-8').read()
    blocks = re.split(r'\n\s*\n', txt.strip())
    caps = []
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        if len(lines) < 3: continue
        m = re.match(r'(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)', lines[1])
        if not m: continue
        g = [int(x) for x in m.groups()]
        start = g[0]*3600 + g[1]*60 + g[2] + g[3]/1000.0
        end   = g[4]*3600 + g[5]*60 + g[6] + g[7]/1000.0
        caps.append({'start': start, 'end': end, 'text': ' '.join(lines[2:])})
    return caps

def font(size):
    for p in ['/System/Library/Fonts/Helvetica.ttc',
              '/System/Library/Fonts/Supplemental/Arial.ttf']:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def burn(scene_img, text, width, height):
    img = Image.open(scene_img).convert('RGB').resize((width, height))
    d = ImageDraw.Draw(img)
    f = font(30)
    # wrap to ~46 chars
    words, lines, cur = text.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > 46: lines.append(cur); cur = w
        else: cur = f'{cur} {w}'.strip()
    if cur: lines.append(cur)
    line_h = 40
    y0 = height - 30 - line_h*len(lines)
    for i, ln in enumerate(lines):
        x = (width - d.textlength(ln, font=f)) / 2
        y = y0 + i*line_h
        for dx in (-2,-1,0,1,2):
            for dy in (-2,-1,0,1,2):
                d.text((x+dx, y+dy), ln, font=f, fill=(0,0,0))
        d.text((x, y), ln, font=f, fill=(255,255,255))
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest'); ap.add_argument('srt'); ap.add_argument('out_manifest')
    ap.add_argument('--out-dir', default='/tmp/wb-captions')
    args = ap.parse_args()

    m = json.load(open(args.manifest))
    caps = parse_srt(args.srt)
    scenes = m['scenes']
    W, H = m.get('width',1024), m.get('height',576)
    os.makedirs(args.out_dir, exist_ok=True)

    # cumulative scene times
    cum, new_scenes = 0.0, []
    si = 0
    for cap in caps:
        while si < len(scenes)-1 and cum + scenes[si].get('duration',5) <= cap['start'] + 0.05:
            cum += scenes[si].get('duration',5); si += 1
        img = burn(scenes[si]['image'], cap['text'], W, H)
        name = f'cap{len(new_scenes):03d}.png'
        img.save(os.path.join(args.out_dir, name))
        new_scenes.append({'image': os.path.join(args.out_dir, name),
                           'duration': round(cap['end']-cap['start'], 3)})

    m2 = dict(m); m2['scenes'] = new_scenes
    json.dump(m2, open(args.out_manifest,'w'), indent=2)
    print(f'OK {args.out_manifest}: {len(new_scenes)} caption frames over {sum(s["duration"] for s in new_scenes):.1f}s')

if __name__ == '__main__':
    main()
