#!/usr/bin/env python3
"""Deterministic whiteboard renderer for the /whiteboard skill.
Builds a timed multi-scene explainer from a JSON manifest: scene PNGs, narration WAV,
per-scene durations, transitions. Pure ffmpeg + Python stdlib, no AI video gen.
Usage: python3 render.py manifest.json out.mp4 [--keep-frames]
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:])
        sys.exit(r.returncode)
    return r.stdout

def duration_seconds(path):
    out = sh(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0', path])
    return float(out.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest')
    ap.add_argument('out')
    ap.add_argument('--keep-frames', action='store_true')
    args = ap.parse_args()

    m = json.load(open(args.manifest))
    scenes = m['scenes']               # [{image, duration, transition?}]
    narration = m.get('narration')     # optional wav
    width, height, fps = m.get('width',1024), m.get('height',576), m.get('fps',24)
    work = tempfile.mkdtemp(prefix='wb-render-')
    try:
        clips = []
        for i, sc in enumerate(scenes):
            img = sc['image']
            dur = float(sc.get('duration', 5))
            clip = os.path.join(work, f'clip{i}.mp4')
            sh(['ffmpeg','-y','-loop','1','-t',f'{dur}','-i',img,
                '-vf',f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
                '-c:v','libx264','-preset','veryfast','-crf','20','-r',f'{fps}', clip])
            clips.append(clip)
        concat = os.path.join(work, 'concat.txt')
        with open(concat,'w') as f:
            for c in clips: f.write(f"file '{c}'\n")
        video_no_audio = os.path.join(work, 'video.mp4')
        sh(['ffmpeg','-y','-f','concat','-safe','0','-i',concat,'-c','copy', video_no_audio])
        if narration and os.path.exists(narration):
            narr_dur = duration_seconds(narration)
            vid_dur = duration_seconds(video_no_audio)
            if narr_dur > vid_dur:
                sh(['ffmpeg','-y','-stream_loop','-1','-i',video_no_audio,'-i',narration,
                    '-t',f'{narr_dur}','-map','0:v','-map','1:a',
                    '-vf','format=yuv420p',
                    '-c:v','libx264','-preset','veryfast','-crf','20','-c:a','aac','-b:a','128k',
                    '-shortest','-movflags','+faststart', args.out])
            else:
                sh(['ffmpeg','-y','-i',video_no_audio,'-i',narration,
                    '-map','0:v','-map','1:a',
                    '-c:v','copy','-c:a','aac','-b:a','128k',
                    '-shortest','-movflags','+faststart', args.out])
        else:
            sh(['ffmpeg','-y','-i',video_no_audio,'-c','copy','-movflags','+faststart', args.out])
        out = sh(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name',
                  '-of','compact', args.out])
        assert 'codec_type=video' in out, 'no video stream'
        if narration and os.path.exists(narration):
            assert 'codec_type=audio' in out, 'no audio stream'
        print(f'OK {args.out} ({duration_seconds(args.out):.1f}s)')
        if args.keep_frames:
            shutil.copytree(work, '/tmp/whiteboard-render-frames', dirs_exist_ok=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)

if __name__ == '__main__':
    main()
