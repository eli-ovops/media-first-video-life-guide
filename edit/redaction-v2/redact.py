from pathlib import Path
import hashlib,json,subprocess
E=Path(__file__).resolve().parent;S=E.parent/'master.mp4';F='/Users/USER/.local/bin/ffmpeg';out=E/'master-redacted.mp4'
source_hash=hashlib.sha256(S.read_bytes()).hexdigest()
cmd=[F,'-hide_banner','-nostdin','-n','-i',str(S),'-map','0:v:0','-map','0:a:0','-vf',"drawbox=x=0:y=0:w=1080:h=480:color=0x17251e:t=fill:enable='lt(t,17.5)'",'-c:v','libx264','-crf','20','-preset','veryfast','-maxrate','10M','-bufsize','20M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','copy','-movflags','+faststart',str(out)]
with (E/'encode.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=f)
assert r.returncode==0
(E/'manifest.json').write_text(json.dumps({'source':str(S),'source_sha256_before':source_hash,'output':str(out),'rectangle':{'x':0,'y':0,'width':1080,'height':480},'color':'#17251e','opacity':1,'time_range':{'start':0,'end_exclusive':17.5,'frames':525},'command':cmd,'source_sampling':'0–17秒18个等距画面实际读过；照片/相框下沿估计低于452px，使用480px上部条带，不覆盖眼睛/鼻嘴；非连续人工看听','privacy':'source-contact-private.jpg含待遮照片仅供本地验收，不公开分发。原master/原片/旧版未改未删。','files':['redact.py','manifest.json','encode.log','source-contact-private.jpg','source-contact.log','master-redacted.mp4']},ensure_ascii=False,indent=2));print('redacted bytes',out.stat().st_size)
