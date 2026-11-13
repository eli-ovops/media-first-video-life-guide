from pathlib import Path
import subprocess,json,hashlib,re
import numpy as np
E=Path(__file__).resolve().parent;S=E.parent/'master.mp4';T=E/'master-redacted.mp4';F='/Users/USER/.local/bin/ffmpeg'
with (E/'full-decode.log').open('w') as f:r=subprocess.run([F,'-hide_banner','-nostdin','-i',str(T),'-progress',str(E/'decode-progress.txt'),'-f','null','-'],stdout=f,stderr=f)
code=r.returncode;log=(E/'full-decode.log').read_text();counts=re.findall(r'^frame=(\d+)$',(E/'decode-progress.txt').read_text(),re.M)
def digest_decoded_audio(p):
 cmd=[F,'-hide_banner','-nostdin','-loglevel','error','-i',str(p),'-map','0:a:0','-f','f32le','pipe:1'];r=subprocess.run(cmd,capture_output=True);assert r.returncode==0;return {'sha256':hashlib.sha256(r.stdout).hexdigest(),'bytes':len(r.stdout)}
a=digest_decoded_audio(S);b=digest_decoded_audio(T)
with (E/'roi-decode.log').open('w') as err:
 p=subprocess.Popen([F,'-hide_banner','-nostdin','-loglevel','error','-i',str(T),'-t','17.5','-vf','crop=1080:480:0:0','-pix_fmt','rgb24','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE,stderr=err)
 expected=np.array([23,37,30],dtype=np.int16);rows=[];size=1080*480*3
 while True:
  data=p.stdout.read(size)
  if not data:break
  assert len(data)==size
  x=np.frombuffer(data,dtype=np.uint8).reshape(-1,3);mins=x.min(axis=0);maxs=x.max(axis=0);means=x.mean(axis=0);deviation=int(np.max(np.abs(x.astype(np.int16)-expected)));rows.append({'frame':len(rows),'time':len(rows)/30,'rgb_min':mins.tolist(),'rgb_max':maxs.tolist(),'rgb_mean':means.tolist(),'max_deviation_from_requested_rgb':deviation,'channel_range_max':int(np.max(maxs-mins))})
 rc=p.wait();assert rc==0
(E/'roi-all-frames.json').write_text(json.dumps({'roi':[0,0,1080,480],'expected_rgb':[23,37,30],'note':'H264/YUV→RGB允许少量色彩取整；逐像素检查整个ROI而非抽样','frames':rows},ensure_ascii=False,indent=2))
manifest=json.loads((E/'manifest.json').read_text());sh=hashlib.sha256(S.read_bytes()).hexdigest()
res={'source_sha256_before':manifest['source_sha256_before'],'source_sha256_after':sh,'source_unchanged':sh==manifest['source_sha256_before'],'output':str(T),'output_bytes':T.stat().st_size,'output_sha256':hashlib.sha256(T.read_bytes()).hexdigest(),'full_decode_exit':code,'decoded_video_frames':int(counts[-1]),'specification':{'width':1080,'height':1920,'fps':30,'video_seconds':59.0,'audio_sample_rate':48000,'audio_channels':1,'audio_codec':'AAC stream-copy'},'decode_error_lines':[l for l in log.splitlines() if re.search('Error|Invalid|Non-monoton',l)],'audio_source':a,'audio_redacted':b,'decoded_audio_identical':a==b,'roi':{'rectangle':[0,0,1080,480],'first_segment_frames_checked':len(rows),'all_525_frames_present':len(rows)==525,'max_rgb_deviation':max(x['max_deviation_from_requested_rgb'] for x in rows),'max_within_roi_channel_range':max(x['channel_range_max'] for x in rows),'passes_opaque_color_statistical_check':len(rows)==525 and all(x['max_deviation_from_requested_rgb']<=8 and x['channel_range_max']<=8 for x in rows),'threshold_note':'最大8级RGB容差适应颜色空间取整和有损编码；均匀色块检查支持遮盖ROI不显示照片，不是人工连续视觉验收。'},'actual_model_effort_speed':'UNKNOWN','scope':'只核本地隐私预处理技术；root负责画中画改版与完整成片审查'}
(E/'verification.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False))
