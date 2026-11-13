from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np
P=Path(__file__).resolve().parents[2];Q=P/'qa/cover-v6';F='/Users/USER/.local/bin/ffmpeg'
V=P/'renders/人生指南-地球online攻略-中英双语-v6.mp4';R=P/'renders/人生指南-纯内容封面-中英双语-v5.mp4'
def run(a):
 r=subprocess.run(a,capture_output=True);assert r.returncode==0,r.stderr.decode(errors='replace');return r.stdout
with (Q/'decode.log').open('w') as f:
 r=subprocess.run([F,'-hide_banner','-nostdin','-i',str(V),'-vf','blackdetect=d=0.02:pic_th=0.98:pix_th=0.1','-progress',str(Q/'decode-progress.txt'),'-f','null','-'],stdout=f,stderr=f)
log=(Q/'decode.log').read_text();progress=(Q/'decode-progress.txt').read_text();frames=int(re.findall(r'^frame=(\d+)$',progress,re.M)[-1]);errors=[x for x in log.splitlines() if re.search(r'Error|Invalid|Non-monoton',x)]
def pcm(p):return run([F,'-v','error','-i',str(p),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1'])
a=pcm(V);b=pcm(R);av=np.frombuffer(a,dtype='<f4');bv=np.frombuffer(b,dtype='<f4');assert len(av)==len(bv)
audio_equal=a==b;corr=float(np.corrcoef(av[24000*2:],bv[24000*2:])[0,1]);peak=float(np.max(np.abs(av)));silence=float(np.max(np.abs(av[:24000*2])))
z=np.frombuffer(run([F,'-v','error','-i',str(V),'-an','-frames:v','16','-vf','scale=270:480','-pix_fmt','rgb24','-f','rawvideo','pipe:1']),dtype=np.uint8).reshape(16,480,270,3).astype(np.int16)
stable=max(float(np.mean(np.abs(z[i]-z[0]))) for i in range(15));boundary=float(np.mean(np.abs(z[15]-z[14])))
run([F,'-v','error','-i',str(V),'-vf','select=eq(n\\,14)','-frames:v','1',str(Q/'poster-frame14.png')])
for t in [0.5,16.5,25.5,59.3]:run([F,'-v','error','-ss',str(t),'-i',str(V),'-frames:v','1',str(Q/f'body-at-{t}.jpg')])
meta=json.loads(run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe',str(V)]).decode())
result={'video':str(V),'bytes':V.stat().st_size,'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'metadata':meta,'full_decode_exit':r.returncode,'frames':frames,'reached_end':'progress=end' in progress,'errors':errors,'black_events':re.findall(r'black_start:[^\n]+',log),'poster':{'static_frames':15,'stability_threshold':3,'max_mean_rgb_difference':stable,'boundary_frame':15,'boundary_seconds':0.5,'boundary_mean_rgb_difference':boundary,'passes':stable<=3 and boundary>3},'audio':{'reference':str(R),'same_decoded_float_samples':audio_equal,'correlation':corr,'peak':peak,'first_half_second_peak':silence,'silence_threshold':0.001,'clipping_samples':int(np.sum(np.abs(av)>=.99995))},'scope':'完整技术解码、音轨比较、首15帧统计和指定时点静态画面；不是完整连续动态看听'}
result['passed']=bool(r.returncode==0 and frames==1785 and result['reached_end'] and not errors and not result['black_events'] and stable<=3 and boundary>3 and corr>=.99 and silence<=.001 and peak<.99995)
(Q/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));assert result['passed']
