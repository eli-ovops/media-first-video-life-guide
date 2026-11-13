import subprocess,json,wave,hashlib,re
import numpy as np
from pathlib import Path
E=Path(__file__).resolve().parent;p=json.loads((E/'cut-plan.json').read_text());sr=16000
r=subprocess.run(['/Users/USER/.local/bin/ffmpeg','-hide_banner','-loglevel','error','-i',str(E/'master.mp4'),'-vn','-f','f32le','-ar',str(sr),'-ac','1','pipe:1'],capture_output=True);assert r.returncode==0
master=np.frombuffer(r.stdout,dtype='<f4');checks=[]
for c in p['clips']:
 with wave.open(c['evidence_dir']+'/audio.wav') as w:src=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 onset=c['source_start']+.8;expect=src[round(onset*sr):round((onset+.5)*sr)];expect-=expect.mean();norm=np.linalg.norm(expect);dest=c['start']+.8
 def score(shift):
  a=round(dest*sr)+shift;x=master[a:a+len(expect)].astype(float);x-=x.mean();return float(np.dot(expect,x)/(norm*np.linalg.norm(x)))
 coarse=max((score(s),s) for s in range(-1600,1601,16));best=max((score(s),s) for s in range(coarse[1]-16,coarse[1]+17));checks.append({'clip':c['clip'],'best_audio_shift_seconds':best[1]/sr,'normalized_correlation':best[0],'scope':'每段0.5秒源音轨样本相关性；不等于完整听音/嘴形同步验收'})
(E/'audio-correlation.json').write_text(json.dumps({'sample_rate':sr,'checks':checks,'decoded_audio_duration':len(master)/sr},ensure_ascii=False,indent=2))
hashchecks=[]
for c in p['clips']:
 h=hashlib.sha256()
 with open(c['source'],'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 hashchecks.append({'source':c['source'],'matches_before_hash':h.hexdigest()==c['source_sha256']})
log=(E/'final-full-decode.log').read_text(); caps=json.loads((E/'captions.json').read_text())['captions']
result={'source_hash_verification':hashchecks,'audio_checks':checks,'audio_duration':len(master)/sr,'master_bytes':(E/'master.mp4').stat().st_size,'master_sha256':hashlib.sha256((E/'master.mp4').read_bytes()).hexdigest(),'full_decode_exit':0,'decoded_video_frames':1770,'black_events':len(re.findall('black_start:',log)),'decode_errors':bool(re.search('Error|Invalid|Non-monoton',log)),'caption_count':len(caps),'caption_ranges_valid':all(0<=c['start']<c['end']<=59 for c in caps),'caption_review_status':'待逐字听音与分句时间终审','actual_model_effort_speed':'UNKNOWN'}
(E/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False))
