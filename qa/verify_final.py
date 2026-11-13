from pathlib import Path
import subprocess,json,re,hashlib,time
import numpy as np
E=Path(__file__).resolve().parent.parent;Q=E/'qa';F='/Users/USER/.local/bin/ffmpeg';target=E/'renders/人生指南-首条-v1.mp4';master=E/'edit/master.mp4'
with (Q/'final-full-decode.log').open('w') as f:
 cmd=[F,'-hide_banner','-nostdin','-v','info','-i',str(target),'-vf','blackdetect=d=0.02:pic_th=0.98:pix_th=0.1','-af','astats=metadata=0:reset=0','-progress',str(Q/'final-decode-progress.txt'),'-f','null','-'];r=subprocess.run(cmd,stdout=f,stderr=f)
log=(Q/'final-full-decode.log').read_text();progress=(Q/'final-decode-progress.txt').read_text();frames=re.findall(r'^frame=(\d+)$',progress,re.M)
meta=subprocess.run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe',str(target)],capture_output=True,text=True)
av=json.loads(meta.stdout) if meta.returncode==0 else {'error':meta.stderr};(Q/'final-avfoundation-metadata.json').write_text(json.dumps(av,ensure_ascii=False,indent=2))
# Read audio into memory only; no original clip reprocessing and no hidden cache writes.
def pcm(path,rate=16000,mono=True):
 cmd=[F,'-hide_banner','-nostdin','-loglevel','error','-i',str(path),'-map','0:a:0','-vn','-f','f32le','-ar',str(rate)]
 if mono:cmd+=['-ac','1']
 cmd+=['pipe:1'];r=subprocess.run(cmd,capture_output=True);assert r.returncode==0,r.stderr;return np.frombuffer(r.stdout,dtype='<f4')
a=pcm(master);b=pcm(target);sr=16000
native=pcm(target,48000,False);peak=float(np.max(np.abs(native)));near=int(np.sum(np.abs(native)>=.99995));above=int(np.sum(np.abs(native)>1));rms=float(np.sqrt(np.mean(native.astype(float)**2)))
exclusions=[(0,.6),(3.05,3.7),(6.25,6.9),(10.6,11.4)]
# Each clip samples a complete 2-second region away from short effects.
regions=[(11.5,13.5),(18.5,20.5),(29,31),(41,43),(53,55)];checks=[]
for idx,(s,e) in enumerate(regions,1):
 x=a[round(s*sr):round(e*sr)].astype(float);x-=x.mean();norm=np.linalg.norm(x)
 def corr(shift):
  y=b[round(s*sr)+shift:round(e*sr)+shift].astype(float);y-=y.mean();return float(np.dot(x,y)/(norm*np.linalg.norm(y)))
 coarse=max((corr(l),l) for l in range(-3200,3201,16));fine=max((corr(l),l) for l in range(coarse[1]-16,coarse[1]+17));checks.append({'clip':idx,'master_region':[s,e],'best_offset_seconds':fine[1]/sr,'normalized_correlation':fine[0]})
shift=round(float(np.median([c['best_offset_seconds'] for c in checks]))*sr);windows=[]
for k in range(0,min(len(a),len(b))-8000,8000):
 s=k/sr;e=(k+8000)/sr
 if any(s<ee and e>ss for ss,ee in exclusions):continue
 x=a[k:k+8000].astype(float);y=b[k+shift:k+8000+shift].astype(float)
 if len(y)!=len(x):continue
 energy=float(np.sqrt(np.mean(x*x)));db=20*np.log10(max(energy,1e-10))
 if db < -45:continue
 x-=x.mean();y-=y.mean();corr=float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)));gain=float(np.dot(x,y)/np.dot(x,x));windows.append({'start':s,'end':e,'rms_dbfs':db,'correlation':corr,'gain':gain})
(Q/'final-audio-windows.json').write_text(json.dumps({'sfx_excluded_windows':exclusions,'sample_rate':sr,'windows':windows},ensure_ascii=False,indent=2))
low=[w for w in windows if w['correlation']<.97]
result={'target':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'specification_source':'当前AVFoundation元数据及真实FFmpeg完整解码；未调用会写evidence的ffprobe-adapter','metadata':av,'full_decode_command':cmd if False else '见qa/verify_final.py','full_decode_exit':r.returncode,'decoded_video_frames':int(frames[-1]),'black_events':re.findall(r'black_start:[^\n]+',log),'decode_error_lines':[l for l in log.splitlines() if re.search('Error|Invalid|Non-monoton',l)],'audio':{'decoded_master_seconds':len(a)/sr,'decoded_final_seconds':len(b)/sr,'native_sample_peak_linear':peak,'native_sample_peak_dbfs':20*np.log10(peak),'samples_abs_ge_0_99995':near,'samples_abs_gt_1':above,'rms_linear':rms,'nonempty':len(native)>0 and rms>0,'peak_limit':'只核解码样本峰值；未证明模拟true-peak/完整主观听音'},'audio_correlation':{'regions':checks,'excluded_sfx_windows':exclusions,'median_offset_seconds':shift/sr,'half_second_voiced_windows_tested':len(windows),'min_correlation':min(w['correlation'] for w in windows),'median_correlation':float(np.median([w['correlation'] for w in windows])),'windows_below_0_97':low,'min_gain':min(w['gain'] for w in windows),'max_gain':max(w['gain'] for w in windows),'method':'5段各2s±200ms偏移搜索＋全轨0.5s语音窗相关性（排除4个SFX窗和<-45dB静音）；对master，不重读原片','interpretation':'高相关性和稳定偏移支持同源原声、无可检测语音缺口；不等于逐字听音验收'},'actual_model_effort_speed':'UNKNOWN'}
(Q/'final-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:result[k] for k in ['bytes','full_decode_exit','decoded_video_frames','black_events','decode_error_lines','audio','audio_correlation']},ensure_ascii=False))
