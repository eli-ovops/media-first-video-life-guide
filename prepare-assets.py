from pathlib import Path
import json, shutil, subprocess, hashlib, wave, struct, math

root = Path(__file__).resolve().parent
capture = root / 'assets/capture'
out = root / 'assets'
(out / 'fonts').mkdir(exist_ok=True)
(root / 'evidence').mkdir(exist_ok=True)
ffmpeg = '/Users/USER/.local/bin/ffmpeg'
records = []

def run(args, name):
    result = subprocess.run([ffmpeg, '-hide_banner', '-nostdin', *args], capture_output=True, text=True)
    (root / 'evidence' / (name + '.log')).write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(name + ' failed: ' + result.stderr[-1500:])

for src, dest in [('/System/Library/Fonts/STHeiti Medium.ttc','heiti.ttc'),('/System/Library/Fonts/Supplemental/Songti.ttc','songti.ttc')]:
    target=out/'fonts'/dest
    if not target.exists(): shutil.copyfile(src,target)
    records.append({'path':str(target),'source':src,'purpose':'本机私有渲染字体；不作为公开下载素材分发'})

crops = [
    ('github-title.jpg','github-excerpt.jpg','crop=844:225:34:42'),
    ('chapter-menu.jpg','toc-excerpt.jpg','crop=235:435:19:63'),
    ('skill-chapter.jpg','chapter-excerpt.jpg','crop=660:590:18:510'),
    ('skill-entry.jpg','cost-excerpt.jpg','crop=655:245:20:610'),
    ('skill-sources.jpg','source-excerpt.jpg','crop=655:120:20:960'),
]
for src,dest,filt in crops:
    target=out/dest
    if not target.exists(): run(['-i',str(capture/src),'-vf',filt,'-frames:v','1','-q:v','2',str(target)],dest)
    records.append({'path':str(target),'source':str(capture/src),'purpose':'真实页面的编辑裁切；未重写页面字段'})

for prefix, target_duration in [('toc',6.4),('source',6.4),('skill',7.0)]:
    record=json.loads((capture/f'{prefix}-scroll-record.json').read_text())
    frames=record['frames']
    # 压缩操作准备时的静止等待；各实际捕获帧顺序保持，未生成虚构滚动页面。
    stamps=[f['metadata']['timestamp'] for f in frames]
    durations=[max(1/30,min(0.7,stamps[i+1]-stamps[i])) for i in range(len(frames)-1)]+[0.5]
    ratio=target_duration/sum(durations)
    concat=capture/f'{prefix}-scroll.ffconcat'
    lines=['ffconcat version 1.0']
    for f,d in zip(frames,durations):
        lines += ["file '"+str(capture/f['file']).replace("'","'\\''")+"'",f'duration {d*ratio:.9f}']
    lines += ["file '"+str(capture/frames[-1]['file']).replace("'","'\\''")+"'"]
    concat.write_text('\n'.join(lines)+'\n')
    target=out/f'{prefix}-scroll.mp4'
    if not target.exists(): run(['-f','concat','-safe','0','-i',str(concat),'-vf','fps=30,scale=trunc(iw/2)*2:trunc(ih/2)*2','-t',str(target_duration),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],prefix+'-scroll-encode')
    records.append({'path':str(target),'source':str(capture/f'{prefix}-scroll-record.json'),'purpose':'实际CUA页面录屏，按捕获时间及剪辑节奏重排静止间隔','frames':len(frames),'duration':target_duration})

# 自制轻音效，只用于关键词/资料揭晓；无第三方音乐或生成服务。
for name,dur,freq in [('tap',0.075,950),('reveal',0.18,420)]:
    target=out/(name+'.wav');rate=48000; samples=[]
    for i in range(int(rate*dur)):
        t=i/rate; env=math.sin(math.pi*t/dur)**2*math.exp(-t*22)
        value=.22*env*(math.sin(2*math.pi*freq*t)+.24*math.sin(2*math.pi*freq*2.03*t))
        samples.append(struct.pack('<h',round(max(-1,min(1,value))*32767)))
    with wave.open(str(target),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(b''.join(samples))
    records.append({'path':str(target),'source':'prepare-assets.py确定性正弦波','purpose':'自制轻量关键词音效，不是配音或背景音乐'})

for f in capture.iterdir():
    if f.is_file(): records.append({'path':str(f),'source':'本轮CUA截图/实际screencast或其ffconcat','purpose':'真实页面素材及捕获证据，保留复核'})
for rec in records:
    path=Path(rec['path']);rec['bytes']=path.stat().st_size;rec['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
(root/'evidence'/'asset-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(json.dumps({'assets':len(records),'bytes':sum(x['bytes'] for x in records),'screen_recordings':['toc-scroll.mp4','source-scroll.mp4','skill-scroll.mp4']},ensure_ascii=False))
