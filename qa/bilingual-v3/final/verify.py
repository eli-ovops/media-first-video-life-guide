from pathlib import Path
import subprocess,json,re,hashlib
import numpy as np
E=Path(__file__).resolve().parents[3];Q=E/'qa/bilingual-v3/final';F='/Users/USER/.local/bin/ffmpeg'
target=E/'renders/人生指南-中英双语-首帧海报-v3.mp4';reference=E/'renders/人生指南-画中画-隐私修订-v2.mp4'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def run(cmd):
 r=subprocess.run(cmd,capture_output=True);assert r.returncode==0,r.stderr.decode(errors='replace');return r.stdout
cmd=[F,'-hide_banner','-nostdin','-v','info','-i',str(target),'-vf','blackdetect=d=0.02:pic_th=0.98:pix_th=0.1','-af','astats=metadata=0:reset=0','-progress',str(Q/'decode-progress.txt'),'-f','null','-']
with (Q/'full-decode.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=f)
log=(Q/'full-decode.log').read_text();progress=(Q/'decode-progress.txt').read_text();decode_exit=r.returncode
frames=int(re.findall(r'^frame=(\d+)$',progress,re.M)[-1]);errors=[s for s in log.splitlines() if re.search('Error|Invalid|Non-monoton',s)]
meta=subprocess.run(['/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/bin/avprobe',str(target)],capture_output=True,text=True);assert meta.returncode==0,meta.stderr
av=json.loads(meta.stdout);(Q/'avfoundation-metadata.json').write_text(json.dumps(av,indent=2))
def pcm(p,rate=16000,mono=True):
 c=[F,'-hide_banner','-nostdin','-v','error','-i',str(p),'-map','0:a:0','-vn','-ar',str(rate)]
 if mono:c+=['-ac','1']
 c+=['-f','f32le','pipe:1'];return np.frombuffer(run(c),dtype='<f4')
a=pcm(reference);b=pcm(target);sr=16000
native=pcm(target,48000,False);peak=float(np.max(np.abs(native)));rms=float(np.sqrt(np.mean(native.astype(float)**2)));clip=int(np.sum(np.abs(native)>=.99995));over=int(np.sum(np.abs(native)>1))
# The actual log identifies stereo native audio. First 0.5 seconds = 24000 stereo frames.
silent=native[:24000*2];silentpeak=float(np.max(np.abs(silent)));silent_rms=float(np.sqrt(np.mean(silent.astype(float)**2)))
regions=[(11.5,13.5),(18.5,20.5),(29,31),(41,43),(53,55)];checks=[]
for i,(s,e) in enumerate(regions,1):
 x=a[round(s*sr):round(e*sr)].astype(float);x-=x.mean();nx=np.linalg.norm(x)
 def corr(k):
  y=b[round(s*sr)+k:round(e*sr)+k].astype(float);y-=y.mean();return float(np.dot(x,y)/(nx*np.linalg.norm(y)))
 coarse=max((corr(k),k) for k in range(4800,11201,16));fine=max((corr(k),k) for k in range(coarse[1]-16,coarse[1]+17))
 checks.append({'clip':i,'source_region_seconds':[s,e],'v3_offset_seconds':fine[1]/sr,'correlation':fine[0]})
shift=8000;windows=[]
for k in range(0,min(len(a),len(b)-shift)-8000,8000):
 x=a[k:k+8000].astype(float);y=b[k+shift:k+shift+8000].astype(float);energy=np.sqrt(np.mean(x*x))
 if energy<10**(-45/20):continue
 x-=x.mean();y-=y.mean();windows.append({'source_start_seconds':k/sr,'v3_start_seconds':(k+shift)/sr,'correlation':float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)))})
(Q/'audio-windows.json').write_text(json.dumps(windows,indent=2))
# Predeclared average delta threshold: stable <=3 RGB levels; boundary >3.
c=[F,'-hide_banner','-nostdin','-v','error','-i',str(target),'-an','-frames:v','16','-vf','scale=270:480','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
z=np.frombuffer(run(c),dtype=np.uint8).reshape(-1,480,270,3).astype(np.int16);assert len(z)==16
first=[float(np.mean(np.abs(z[i]-z[0]))) for i in range(15)];adj=[float(np.mean(np.abs(z[i]-z[i-1]))) for i in range(1,15)];boundary=float(np.mean(np.abs(z[15]-z[14])))
poster={'frames_checked':16,'poster_frame_indices':[0,14],'poster_frames':15,'boundary_frame_index':15,'boundary_seconds':.5,'downscaled_width':270,'downscaled_height':480,'stability_threshold_predeclared_rgb_levels':3,'mean_absolute_rgb_difference_vs_frame0':first,'mean_absolute_rgb_adjacent_difference':adj,'max_poster_difference_vs_first':max(first),'max_poster_adjacent_difference':max(adj),'boundary_mean_absolute_rgb_difference':boundary,'boundary_significant_threshold_predeclared_rgb_levels':3,'passes':max(first)<=3 and max(adj)<=3 and boundary>3,'scope':'实际MP4前16帧统计，非PNG替代；海报文字/内容由root看帧验收'}
(Q/'poster-frame-deltas.json').write_text(json.dumps(poster,ensure_ascii=False,indent=2))
# Supporting ROI only; full photo coverage comes from unchanged redacted master + visual acceptance.
c=[F,'-hide_banner','-nostdin','-v','error','-i',str(target),'-an','-frames:v','540','-vf','crop=230:24:450:8','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
r=subprocess.run(c,capture_output=True);(Q/'roi-decode.log').write_bytes(r.stderr);assert r.returncode==0
z=np.frombuffer(r.stdout,dtype=np.uint8).reshape(-1,24,230,3).astype(np.int16);diff=np.max(np.abs(z-np.array([23,37,30])),axis=(1,2,3));rng=np.max(np.ptp(z,axis=(1,2)),axis=1)
roirows=[{'frame':i,'seconds':i/30,'max_rgb_difference':int(d),'max_channel_spatial_range':int(v)} for i,(d,v) in enumerate(zip(diff,rng))]
(Q/'roi-all-frames.json').write_text(json.dumps(roirows,indent=2));roi={'rectangle':[450,8,230,24],'target_rgb':[23,37,30],'threshold_predeclared':8,'frames_checked':len(z),'max_rgb_difference':int(diff.max()),'max_channel_spatial_range':int(rng.max()),'failed_frames':[x for x in roirows if x['max_rgb_difference']>8 or x['max_channel_spatial_range']>8],'passes':bool(len(z)==540 and diff.max()<=8 and rng.max()<=8),'scope':'顶部小ROI全部540帧辅助证据；不宣称照片全区域识别或完整连续视觉验收'}
priorred=json.loads((E/'edit/redaction-v2/verification.json').read_text());priorv2=json.loads((E/'qa/pip-v2/final-verification.json').read_text());priorv1=json.loads((E/'qa/final-verification.json').read_text())
hashes=[]
for p,expected in [(E/'edit/master.mp4',priorred['source_sha256_after']),(E/'edit/redaction-v2/master-redacted.mp4',priorred['output_sha256']),(reference,priorv2['sha256']),(E/'renders/人生指南-首条-v1.mp4',priorv1['sha256'])]:
 current=sha(p);hashes.append({'path':str(p),'sha256':current,'matches_prior':current==expected})
check=json.loads((E/'evidence/check-bilingual-v3-report.json').read_text());layers={k:{n:v[n] for n in ['ok','errorCount','warningCount','infoCount','checked','passed'] if n in v} for k,v in check.items() if isinstance(v,dict) and 'ok' in v}
caps=json.loads((E/'data/captions-bilingual-v3.json').read_text());caption_summary={'count':len(caps['captions']),'poster_seconds':caps['poster_seconds'],'timing_offset':caps['source_timing_offset'],'last_caption':caps['captions'][-1],'source':'data/captions-bilingual-v3.json','translation_limit':'只读当前修订字幕，无回滚初稿，最终中上英下由root画面验收'}
res={'target':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'full_decode_exit':decode_exit,'decoded_video_frames':frames,'decode_reached_end':'progress=end' in progress,'black_events':re.findall('black_start:[^\n]+',log),'decode_error_lines':errors,'metadata':av,'stream_lines':[s for s in log.splitlines() if 'Stream #0:' in s and ('Video:' in s or 'Audio:' in s)],'audio':{'reference':str(reference),'sample_peak_linear':peak,'sample_peak_dbfs':20*np.log10(peak),'nonempty':len(native)>0 and rms>0,'rms_linear':rms,'samples_abs_ge_0_99995':clip,'samples_abs_gt1':over,'first_half_second_peak_linear':silentpeak,'first_half_second_rms_linear':silent_rms,'silence_threshold_predeclared_linear':.001,'first_half_second_silent':silentpeak<=.001,'five_regions':checks,'voiced_half_second_windows':len(windows),'min_correlation_at_plus_half_second':min(x['correlation'] for x in windows),'windows_below_0_97':[x for x in windows if x['correlation']<.97],'scope':'v3对v2单声道16kHz相关性/偏移；原生48kHz双声道峰值；未重读原片、不证明模拟true-peak或主观听音'},'poster':poster,'privacy_auxiliary_roi':roi,'unchanged_sources_and_older_versions':hashes,'composition_check':layers,'caption_data':caption_summary,'actual_model_effort_speed':'UNKNOWN','limits':'root负责实际画面文字/双语排版/PIP/隐私视觉验收；机器统计不是连续完整看听'}
res['status']='PASS' if decode_exit==0 and frames==1785 and not errors and poster['passes'] and roi['passes'] and clip==over==0 and rms>0 and silentpeak<=.001 and all(x['v3_offset_seconds']==.5 for x in checks) and min(x['correlation'] for x in windows)>=.97 and all(x['matches_prior'] for x in hashes) else 'REVIEW_REQUIRED'
(Q/'final-verification.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False),flush=True)
manifest={'scope':'only qa/bilingual-v3/final','files':[{'path':str(p.resolve()),'bytes':p.stat().st_size,'purpose':'可复核最终技术验收证据，保留'} for p in sorted(Q.iterdir()) if p.is_file()],'new_temporary_media':[],'cleanup':'无无用途一次性文件，未删除'}
manifest['files'].append({'path':str((Q/'manifest.json').resolve()),'purpose':'记录本任务新增证据路径'})
(Q/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
