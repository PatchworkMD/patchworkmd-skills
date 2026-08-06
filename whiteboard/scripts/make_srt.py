#!/usr/bin/env python3
"""Generate an SRT caption file from narration text + audio duration.
Simple deterministic timing: split text into lines, distribute proportionally.
Usage: python3 make_srt.py script.txt narration.wav out.srt [--max-len 90]
"""
import argparse, re, subprocess

def duration_seconds(path):
    out = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                          '-of','csv=p=0', path], capture_output=True, text=True)
    return float(out.stdout.strip())

def wrap(line, max_len):
    words, out, cur = line.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > max_len:
            out.append(cur); cur = w
        else:
            cur = f'{cur} {w}'.strip()
    if cur: out.append(cur)
    return out

def fmt(t):
    h, rem = divmod(t, 3600); m, s = divmod(rem, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'.replace('.', ',')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('script'); ap.add_argument('narration'); ap.add_argument('out')
    ap.add_argument('--max-len', type=int, default=90)
    args = ap.parse_args()

    text = open(args.script).read().strip()
    # drop blank lines, normalize whitespace
    paras = [re.sub(r'\s+', ' ', p).strip() for p in text.split('\n\n') if p.strip()]
    lines = []
    for p in paras:
        for piece in wrap(p, args.max_len):
            lines.append(piece)
    total = duration_seconds(args.narration)
    per = total / max(len(lines), 1)
    srt = []
    for i, line in enumerate(lines, 1):
        a, b = (i-1)*per, i*per
        srt.append(f'{i}\n{fmt(a)} --> {fmt(b)}\n{line}\n')
    open(args.out, 'w').write('\n'.join(srt))
    print(f'OK {args.out}: {len(lines)} captions over {total:.1f}s')

if __name__ == '__main__':
    main()
