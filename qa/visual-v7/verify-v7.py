# -*- coding: utf-8 -*-
from pathlib import Path
import json, subprocess, hashlib, re, sys
import numpy as np
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parents[2]; BASE=P/'qa/visual-v7'
Q=BASE/('final' if '--final' in sys.argv else '.')
Q.mkdir(exist_ok=True)
F='/Users/USER/.local/bin/ffmpeg'
V=P/('renders/人生指南-视觉修订-定框淡入-中英双语-v7.mp4' if '--final' in sys.argv else 'renders/人生指南-视觉修订-中英双语-v7.mp4')
R=P/'renders/人生指南-地球online攻略-中英双语-v6.mp4'
assert V.is_file() and V.stat().st_size>0, 'Wait for render completion before verification'
def run(a):
    p=subprocess.run(a,capture_output=True)
    assert p.returncode==0,p.stderr.decode(errors='replace')
    return p.stdout
with (Q/'decode.log').open('w') as f:
    p=subprocess.run([F,'-hide_banner','-nostdin','-i',str(V),'-vf','blackdetect=d=0.02:pic_th=0.98:pix_th=0.1','-progress',str(Q/'decode-progress.txt'),'-f','null','-'],stdout=f,stderr=f)
log=(Q/'decode.log').read_text(); progress=(Q/'decode-progress.txt').read_text()
assert p.returncode==0, log[-1000:]
frames=int(re.findall(r'^frame=(\d+)$',progress,re.M)[-1])
errors=[x for x in log.splitlines() if re.search(r'Error|Invalid|Non-monoton',x)]
def pcm(v):return run([F,'-v','error','-i',str(v),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1'])
a=pcm(V);b=pcm(R);av=np.frombuffer(a,dtype='<f4');bv=np.frombuffer(b,dtype='<f4')
assert len(av)==len(bv)
corr=float(np.corrcoef(av[48000:],bv[48000:])[0,1]);peak=float(np.max(np.abs(av)))
poster=np.frombuffer(run([F,'-v','error','-i',str(V),'-an','-frames:v','16','-vf','scale=270:480','-pix_fmt','rgb24','-f','rawvideo','pipe:1']),dtype=np.uint8).reshape(16,480,270,3).astype(np.int16)
stable=max(float(np.mean(np.abs(poster[i]-poster[0]))) for i in range(15)); boundary=float(np.mean(np.abs(poster[15]-poster[14])))
times=[0,14/30,0.5,11.2,11.35,11.55,12,13,16.5,21.55,21.75,21.9,30.5,30.65,30.9,31.75,31.9,32.2,32.5,33.35,33.5,33.6,33.7,34,35,37,38,39.9,40.15,40.3,40.6,41,42,46.45,46.7,46.8,59.3]
D=Q/'exported-frames';D.mkdir(exist_ok=True)
manifest=[]
for i,t in enumerate(times):
    n=round(t*30)
    path=D/f'frame-{i:02d}-n{n}-at-{n/30:.3f}s.jpg'
    run([F,'-v','error','-ss',str(n/30),'-i',str(V),'-frames:v','1','-q:v','2',str(path)])
    manifest.append({'path':str(path),'requested_seconds':t,'frame_index':n,'actual_seconds':n/30,'source':'actual exported v7 MP4'})
(Q/'frame-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for sheet,start in enumerate(range(0,len(manifest),12)):
    group=manifest[start:start+12]; w=360;h=640;head=26;rows=(len(group)+3)//4
    canvas=Image.new('RGB',(4*w,rows*(h+head)),(20,24,22));draw=ImageDraw.Draw(canvas)
    for j,item in enumerate(group):
        x=(j%4)*w;y=(j//4)*(h+head)
        draw.text((x+8,y+5),f"{start+j:02d} n={item['frame_index']} t={item['actual_seconds']:.3f}s",fill='white')
        canvas.paste(Image.open(item['path']).resize((w,h)),(x,y+head))
    canvas.save(Q/f'export-contact-{sheet+1}.jpg',quality=90)
meta=json.loads(run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe',str(V)]))
old=(BASE/'index-before-v7.html.txt').read_text();new=(P/'index.html').read_text()
old=old.replace('anim("chapter-box",[{transform:"scaleX(0)",opacity:0},{transform:"scaleX(1)",opacity:1}],31.25,.4);','anim("chapter-box",[{opacity:0},{opacity:1}],31.25,.4);') if '--final' in sys.argv else old
patterns={'placed_media':r'<(?:video|audio)\b[^>]*>','captions':r'<div data-hf-id="[^"]*" class="clip caption".*?</div></div>','cover':r'<section id="cover-v3".*?</section>','animation':r'<script>.*?</script>'}
if '--final' in sys.argv:
    patterns['animation_except_chapter_highlight']=patterns.pop('animation')
protected={k:re.findall(v,old,re.S)==re.findall(v,new,re.S) for k,v in patterns.items()}
check_text=(BASE/('check-final-raw.log' if '--final' in sys.argv else 'check-raw.log')).read_text();check=json.loads(check_text[check_text.index('{'):]);(Q/'check-report.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
result={'video':str(V),'bytes':V.stat().st_size,'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'metadata':meta,'full_decode_exit':p.returncode,'frames':frames,'reached_end':'progress=end' in progress,'errors':errors,'black_events':re.findall(r'black_start:[^\n]+',log),'audio':{'reference':str(R),'same_decoded_float_samples':a==b,'correlation':corr,'peak':peak,'first_half_second_peak':float(np.max(np.abs(av[:48000]))),'clipping_samples':int(np.sum(np.abs(av)>=.99995))},'cover':{'stable_frame_count':15,'max_mean_rgb_difference':stable,'boundary_at_seconds':0.5,'boundary_mean_rgb_difference':boundary},'protected_html_sections_unchanged':protected,'exported_frame_count':len(manifest),'check_summary':{k:{f:check[k].get(f) for f in ['ok','errorCount','warningCount','infoCount']} for k in ['lint','runtime','layout','motion','contrast']},'scope':'Full technical decode/audio comparison plus listed static exported samples; no claim of continuous dynamic viewing/hearing or independent visual PASS.'}
result['technical_passed']=bool(p.returncode==0 and frames==1785 and result['reached_end'] and not errors and not result['black_events'] and stable<=3 and boundary>3 and corr>=.99 and peak<.99995 and all(protected.values()))
(Q/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'technical_passed':result['technical_passed'],'frames':frames,'audio_correlation':corr,'same_audio_samples':a==b,'bytes':V.stat().st_size,'frame_samples':len(manifest)}))
assert result['technical_passed']
