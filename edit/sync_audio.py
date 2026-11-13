from pathlib import Path
import json,subprocess
E=Path(__file__).resolve().parent;p=json.loads((E/'cut-plan.json').read_text());F='/Users/USER/.local/bin/ffmpeg'
cmd=[F,'-hide_banner','-nostdin','-n','-copyts','-f','concat','-safe','0','-i',str(E/'concat.txt')]
for c in p['clips']:cmd+=['-i',c['source']]
filters=[]
for i,c in enumerate(p['clips'],1):filters.append(f"[{i}:a:0]atrim=start={c['source_start']}:end={c['source_end']},asetpts=PTS-STARTPTS[a{i}]")
filters.append(''.join(f'[a{i}]' for i in range(1,6))+'concat=n=5:v=0:a=1[aout]')
cmd+=['-filter_complex',';'.join(filters),'-map','0:v:0','-map','[aout]','-c:v','copy','-c:a','aac','-b:a','128k','-ar','48000','-ac','1','-movflags','+faststart',str(E/'master-original-audio.mp4')]
with (E/'original-audio-sync.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=log)
assert r.returncode==0
(E/'master.mp4').rename(E/'master-resample-draft.mp4');(E/'master-original-audio.mp4').rename(E/'master.mp4')
p['audio']='五个原片原始音轨直接atrim相同起止范围并concat，最终一次AAC128kbps编码；未用逐段编码后的AAC，消除priming累计。'
p['final_audio_command']=cmd
(E/'cut-plan.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
print('final original-audio master ready')
