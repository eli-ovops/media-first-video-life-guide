from pathlib import Path
import subprocess,json,re,hashlib,time
import numpy as np
E=Path(__file__).resolve().parents[2];Q=E/'qa/pip-v2';F='/Users/USER/.local/bin/ffmpeg';target=E/'renders/人生指南-画中画-隐私修订-v2.mp4';master=E/'edit/master.mp4'
with (Q/'final-full-decode.log').open('w') as f:
 cmd=[F,'-hide_banner','-nostdin','-v','info','-i',str(target),'-vf','blackdetect=d=0.02:pic_th=0.98:pix_th=0.1','-af','astats=metadata=0:reset=0','-progress',str(Q/'final-decode-progress.txt'),'-f','null','-'];r=subprocess.run(cmd,stdout=f,stderr=f)
decode_exit=r.returncode
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
result={'target':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'specification_source':'当前AVFoundation元数据及真实FFmpeg完整解码；未调用会写evidence的ffprobe-adapter','metadata':av,'full_decode_command':cmd if False else '见qa/pip-v2/verify_final.py','full_decode_exit':decode_exit,'decoded_video_frames':int(frames[-1]),'black_events':re.findall(r'black_start:[^\n]+',log),'decode_error_lines':[l for l in log.splitlines() if re.search('Error|Invalid|Non-monoton',l)],'audio':{'decoded_master_seconds':len(a)/sr,'decoded_final_seconds':len(b)/sr,'native_sample_peak_linear':peak,'native_sample_peak_dbfs':20*np.log10(peak),'samples_abs_ge_0_99995':near,'samples_abs_gt_1':above,'rms_linear':rms,'nonempty':len(native)>0 and rms>0,'peak_limit':'只核解码样本峰值；未证明模拟true-peak/完整主观听音'},'audio_correlation':{'regions':checks,'excluded_sfx_windows':exclusions,'median_offset_seconds':shift/sr,'half_second_voiced_windows_tested':len(windows),'min_correlation':min(w['correlation'] for w in windows),'median_correlation':float(np.median([w['correlation'] for w in windows])),'windows_below_0_97':low,'min_gain':min(w['gain'] for w in windows),'max_gain':max(w['gain'] for w in windows),'method':'5段各2s±200ms偏移搜索＋全轨0.5s语音窗相关性（排除4个SFX窗和<-45dB静音）；对master，不重读原片','interpretation':'高相关性和稳定偏移支持同源原声、无可检测语音缺口；不等于逐字听音验收'},'actual_model_effort_speed':'UNKNOWN'}

# Top ROI is above all designed cards/bars. This is supporting evidence only.
roi_cmd=[F,'-hide_banner','-nostdin','-v','error','-i',str(target),'-an','-frames:v','525','-vf','crop=230:24:450:8','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
roi_run=subprocess.run(roi_cmd,capture_output=True)
(Q/'roi-decode.log').write_bytes(roi_run.stderr)
framebytes=230*24*3
assert len(roi_run.stdout)%framebytes==0
roi=np.frombuffer(roi_run.stdout,dtype=np.uint8).reshape(-1,24,230,3).astype(np.int16)
diffs=np.max(np.abs(roi-np.array([23,37,30])),axis=(1,2,3))
ranges=np.max(np.ptp(roi,axis=(1,2)),axis=1)
rows=[{'frame':i,'seconds':i/30,'max_rgb_difference':int(d),'max_channel_spatial_range':int(v)} for i,(d,v) in enumerate(zip(diffs,ranges))]
(Q/'roi-all-frames.json').write_text(json.dumps(rows,indent=2))
result['privacy_final_auxiliary_roi']={'rectangle':[450,8,230,24],'color':[23,37,30],'threshold_predeclared':8,'decode_exit':roi_run.returncode,'frames_checked':len(rows),'max_rgb_difference':int(diffs.max()),'max_channel_spatial_range':int(ranges.max()),'fail_frames_gt8':[x for x in rows if x['max_rgb_difference']>8 or x['max_channel_spatial_range']>8],'passes_525_frame_8_level_check':len(rows)==525 and int(diffs.max())<=8 and int(ranges.max())<=8,'scope':'顶部小ROI全帧检查，仅支持最终文件确有隐私背景；完整照片范围依赖母版全ROI核验及root画面核验，不是全人像识别'}
redacted=E/'edit/redaction-v2/master-redacted.mp4'
prior=json.loads((E/'edit/redaction-v2/verification.json').read_text())
hashes={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [master,redacted]}
result['source_hash_checks']={'sha256_current':hashes,'master_matches_prior':hashes[str(master)]==prior['source_sha256_after'],'redacted_matches_prior':hashes[str(redacted)]==prior['output_sha256']}
check=json.loads((E/'evidence/check-pip-final-report.json').read_text())
result['composition_check']={k:{z:v[z] for z in ['ok','errorCount','warningCount','infoCount','checked','passed'] if z in v} for k,v in check.items() if isinstance(v,dict) and 'ok' in v}
result['limitation']='机器解码/采样统计/音频相关性；非连续主观完整看听验收。解码样本无削波不证明true-peak。'
result['scope']='仅最终技术验收；root负责视觉/交付；未重读原片、未抽取未遮照片。'
result['status']='PASS' if decode_exit==0 and result['decoded_video_frames']==1770 and not result['decode_error_lines'] and result['audio']['nonempty'] and near==0 and above==0 and not low and all(c['best_offset_seconds']==0 for c in checks) and result['privacy_final_auxiliary_roi']['passes_525_frame_8_level_check'] and result['source_hash_checks']['master_matches_prior'] and result['source_hash_checks']['redacted_matches_prior'] else 'REVIEW_REQUIRED'
result['specification']={'width':1080,'height':1920,'fps':30,'video_frames':1770,'container_seconds':59.0,'video_codec':'H264 High','audio_codec':'AAC LC','audio_sample_rate':48000,'audio_channels':2,'source':'AVFoundation metadata and actual FFmpeg complete decode input stream log'}
(Q/'final-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({k:result[k] for k in ['status','bytes','full_decode_exit','decoded_video_frames','black_events','decode_error_lines','audio','audio_correlation','privacy_final_auxiliary_roi','source_hash_checks','composition_check']},ensure_ascii=False))
