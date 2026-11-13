#!/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
"""Project-only JSON metadata adapter; never claims to be official ffprobe."""
from pathlib import Path
import subprocess, sys, json, re, hashlib

root=Path(__file__).resolve().parent
avprobe='/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe'
ffmpeg='/Users/USER/.local/bin/ffmpeg'
if '-version' in sys.argv:
    print('Local AVFoundation + FFmpeg JSON adapter; not official ffprobe')
    raise SystemExit(0)
if len(sys.argv)<2:
    raise SystemExit('A media path is required')
source=Path(sys.argv[-1]).resolve()
if not source.is_file(): raise SystemExit('Media path does not exist')
key=hashlib.sha256(('metadata-v2:'+str(source)+':'+str(source.stat().st_size)+':'+str(source.stat().st_mtime_ns)).encode()).hexdigest()
cache=root/'evidence/probe-adapter-cache';cache.mkdir(exist_ok=True)
cached=cache/(key+'.json')
if cached.exists():
    result=json.loads(cached.read_text())
else:
    p=subprocess.run([avprobe,str(source)],capture_output=True,text=True)
    if p.returncode: raise SystemExit(p.stderr)
    result=json.loads(p.stdout)
    description=subprocess.run([ffmpeg,'-hide_banner','-nostdin','-i',str(source)],capture_output=True,text=True).stderr
    video=[s for s in result.get('streams',[]) if s.get('codec_type')=='video']
    if video:
        # FFmpeg returns the actual demuxed picture count; no duration×fps guess.
        counted=subprocess.run([ffmpeg,'-hide_banner','-nostdin','-v','error','-i',str(source),'-map','0:v:0','-an','-c:v','copy','-f','null','-progress','pipe:1','-'],capture_output=True,text=True)
        if counted.returncode: raise SystemExit(counted.stderr)
        counts=re.findall(r'^frame=(\d+)$',counted.stdout,re.M)
        if not counts: raise SystemExit('FFmpeg did not report a picture count')
        for s in video:
            s['nb_frames']=counts[-1];s['nb_read_frames']=counts[-1]
            s['duration']=result['format']['duration'];s['r_frame_rate']=s['avg_frame_rate']
    for i,s in enumerate(result.get('streams',[])):
        s['index']=i
        if s.get('codec_type')=='audio':
            m=re.search(r'Audio:.*?,\s*(\d+) Hz,\s*(mono|stereo)',description)
            if m: s['sample_rate']=m.group(1);s['channels']=1 if m.group(2)=='mono' else 2
            if m:
                decoded=subprocess.run([ffmpeg,'-hide_banner','-nostdin','-v','error','-i',str(source),'-map','0:a:0','-f','f32le','-'],capture_output=True)
                if decoded.returncode: raise SystemExit(decoded.stderr.decode(errors='replace'))
                s['duration']=str(len(decoded.stdout)/4/int(s['sample_rate'])/s['channels'])
    result['format']['filename']=str(source)
    cached.write_text(json.dumps(result,ensure_ascii=False,indent=2))
with (root/'evidence/probe-adapter-calls.jsonl').open('a') as f:
    f.write(json.dumps({'source':str(source),'args':sys.argv[1:],'metadata_cache':str(cached),'adapter':'AVFoundation metadata + FFmpeg actual picture count'},ensure_ascii=False)+'\n')
for s in result.get('streams',[]): s.pop('pix_fmt',None)
print(json.dumps(result,ensure_ascii=False))
