from pathlib import Path
import subprocess, json, hashlib, wave, array, math, time
E=Path(__file__).resolve().parent
F='/Users/USER/.local/bin/ffmpeg'
ids=['c0cbfe9ad16458a5845756d9a3ae9fe3','76c971fb70d60bd7659b450b5e34d41f','e501701cdbd3b1495d7418788afc05cc','1c0ef867027711154271f3f4b44803db','076d5b70542c70c284911e8dac29a7b7']
evidence=['20261007-153539-a6666f','20261008-111128-e704b3','20261008-111122-18f7c6','20261008-111117-3dc47c','20261008-110911-0e437e']
ranges=[(1,18.5),(.6,11),(.7,12.6),(.8,12.7),(1.1,8.4)]
phrases=[
[(1.1,2.2,'被裁员以后'),(2.2,3.6,'哪些事情需要先处理'),(4.1,5.5,'租房遇到纠纷'),(5.5,6.7,'该去查哪些规定'),(7.3,8.6,'想学一门新技能'),(8.6,10.9,'怎么判断到底值不值得花钱呢'),(11.8,13.3,'这类生活问题在GitHub上'),(13.3,15.3,'已经有人整理成了一份'),(15.8,16.4,'免费的'),(16.8,18.3,'高性价比人生指南')],
[(.7,2.4,'这份免费的人生说明书'),(2.4,4.3,'我建议你可以先存下来'),(5,6.8,'租房、换工作、学技能'),(7,8.6,'碰到什么问题都可以'),(9,10.9,'翻对应的这个章节来看')],
[(.8,2.8,'比如想学一门新技能'),(3,4.3,'里面有一章就叫'),(4.3,5.6,'学什么技能划算'),(6,7.1,'要花多少钱'),(7.1,8.5,'或者说花多少时间'),(9.1,10.3,'可能换来什么'),(10.5,12.4,'它都会在这里放在一起讲')],
[(.9,2.4,'而且建议后面还列了'),(2.4,3.6,'资料的来源'),(3.7,5.1,'如果说你想往下查'),(5.1,7.1,'就可以顺着链接继续往下看'),(7.8,8.7,'我的建议是'),(8.7,10.5,'大家可以先把目录存下来'),(10.9,12.5,'到时候有需要的时候再翻')],
[(1.2,2.9,'这份高性价比人生指南'),(2.9,4.5,'我已经整理好文档了'),(4.8,5.7,'想要的朋友只是在'),(5.7,7.1,'评论区评论一下'),(7.4,8,'我发给你')]
]
clips=[]; captions=[];pos=0
for i,(sid,ev,(start,end),ph) in enumerate(zip(ids,evidence,ranges,phrases),1):
 source=Path('/Users/USER/Downloads')/(sid+'_raw.mp4'); out=E/f'clip-{i:02}.mp4'
 h=hashlib.sha256()
 with source.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 probe=subprocess.run([F,'-hide_banner','-i',str(source)],capture_output=True,text=True)
 (E/f'source-{i:02}-metadata.log').write_text(probe.stderr)
 cmd=[F,'-hide_banner','-nostdin','-n','-ss',str(start),'-i',str(source),'-t',str(end-start),'-map','0:v:0','-map','0:a:0','-vf','scale=1080:1920:flags=lanczos,fps=30,setsar=1','-c:v','libx264','-preset','veryfast','-crf','20','-maxrate','10M','-bufsize','20M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','128k','-ar','48000','-ac','1','-movflags','+faststart',str(out)]
 with (E/f'encode-{i:02}.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=log)
 if r.returncode:raise RuntimeError(f'clip {i} exit {r.returncode}')
 clips.append({'clip':i,'source':str(source),'source_sha256':h.hexdigest(),'source_bytes':source.stat().st_size,'source_start':start,'source_end':end,'start':round(pos,3),'end':round(pos+end-start,3),'duration':round(end-start,3),'evidence_dir':f'/Volumes/EXTERNAL/Tools/Whisper/transcripts/{ev}','intermediate':str(out),'reason':'RMS确认头尾准备静音；保留全部句内停顿，切点预留音素余量。','av_sync':'同一源、同一ss/t范围；不变速，不做重叠转场。','commands':cmd})
 for a,b,t in ph:captions.append({'start':round(pos+a-start,3),'end':round(pos+b-start,3),'text':t,'source_clip':i,'source_start':a,'source_end':b,'timing_method':'RMS句间边界加字数分配估计；非逐字强制对齐','needs_review':True,'estimated_timing_uncertainty_seconds':.6})
 pos+=end-start
(E/'concat.txt').write_text(''.join("file '"+str(E/f'clip-{i:02}.mp4')+"'\n" for i in range(1,6)))
cmd=[F,'-hide_banner','-nostdin','-n','-f','concat','-safe','0','-i',str(E/'concat.txt'),'-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-af','aresample=async=1:first_pts=0','-movflags','+faststart',str(E/'master.mp4')]
with (E/'concat.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=log)
if r.returncode:raise RuntimeError('concat failed')
(E/'cut-plan.json').write_text(json.dumps({'version':1,'expected_duration':round(pos,3),'width':1080,'height':1920,'fps':30,'audio':'源AAC解码后同源AAC128kbps/48kHz单声道；无替换、降噪、变速、音量处理','source_color':'全部BT.709 SDR，无HDR映射','transitions':'直接切换；无交叠吞词','clips':clips},ensure_ascii=False,indent=2))
(E/'captions.json').write_text(json.dumps({'version':1,'timebase':'剪后master秒','duration':round(pos,3),'language':'zh-CN','review_status':'口语复用现有ASR；专名上下文校正；未逐字听音核验，时间为估计','corrections':{'GateUp':'GitHub','高兴甲比人生只难/高兴价比人生只难':'高性价比人生指南','一张':'一章','木路':'目录'},'uncertain_wording':['clip5 想要的朋友只是在：保留ASR口语，需听音核对，未擅自改成私信。'],'captions':captions},ensure_ascii=False,indent=2))
print('BUILT',pos, (E/'master.mp4').stat().st_size,flush=True)
