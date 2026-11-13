from pathlib import Path
import numpy as np,subprocess,json
E=Path(__file__).resolve().parent;F='/Users/USER/.local/bin/ffmpeg';cmd=[F,'-hide_banner','-nostdin','-loglevel','error','-i',str(E/'master-redacted.mp4'),'-t','17.5','-vf','crop=1080:480:0:0','-pix_fmt','rgb24','-f','rawvideo','pipe:1'];p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);records=[]
while True:
 b=p.stdout.read(1080*480*3)
 if not b:break
 x=np.frombuffer(b,dtype=np.uint8).reshape(480,1080,3);d=np.max(np.abs(x.astype(np.int16)-np.array([23,37,30],dtype=np.int16)),axis=2);ys,xs=np.where(d>8);inner=x[:464];records.append({'frame':len(records),'outlier_count_rgb_difference_gt8':len(ys),'outlier_y_min':int(ys.min()) if len(ys) else None,'outlier_y_max':int(ys.max()) if len(ys) else None,'inner_y0_to463_max_requested_rgb_difference':int(np.max(np.abs(inner.astype(np.int16)-np.array([23,37,30],dtype=np.int16)))),'inner_channel_range':int(np.max(inner.max(axis=(0,1))-inner.min(axis=(0,1))))})
assert p.wait()==0
outliers=[r for r in records if r['outlier_count_rgb_difference_gt8']]
summary={'frames':len(records),'outlier_frames':len(outliers),'all_gt8_outliers_min_y':min(r['outlier_y_min'] for r in outliers) if outliers else None,'all_gt8_outliers_max_y':max(r['outlier_y_max'] for r in outliers) if outliers else None,'max_inner_rgb_difference':max(r['inner_y0_to463_max_requested_rgb_difference'] for r in records),'max_inner_channel_range':max(r['inner_channel_range'] for r in records),'frames_data':records,'scope':'全ROI仍完整检查；定位初轮严阈值超差是否只位于条带与下方未遮人像的编码交界，不扩大原要求容差'}
(E/'roi-edge-detail.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print({k:v for k,v in summary.items() if k!='frames_data'})
