# -*- coding: utf-8 -*-
"""Bounded visual corrections; never execute historical build scripts."""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent
Q=P/'qa/visual-v7'
Q.mkdir(exist_ok=True)
html=(P/'index.html').read_text()
frozen=next(P.parent.glob('*/04-*/**/index-v6.html.txt')).read_text()
assert html==frozen, 'Working index differs from frozen baseline: stop'
(Q/'index-before-v7.html.txt').write_text(html)
css='''
/* v7: show whole source images; chapter excerpt explicitly names its scope. */
#pip-reveal{height:650px}
.reveal-paper img{width:100%;height:auto;object-fit:contain}
.chapter-paper{height:345px}
.chapter-image-window{position:relative;height:150px;overflow:hidden;background:#fff}
.chapter-image-window img{position:absolute;left:18px;top:-75px;width:1980px;height:1770px;max-width:none;object-fit:fill}
.chapter-image-window .chapter-box{left:18px;top:18px;width:639px;height:111px;border:4px solid #23563e;border-radius:10px;background:transparent}
.chapter-quote{padding:14px 20px 18px;font-size:32px;line-height:1.35;color:#17251e}
.chapter-quote-label{display:block;font-size:25px;color:#23563e;margin-bottom:8px}
#pip-cost{height:735px}
.cost-paper{height:auto}
.cost-paper img{height:auto;width:100%;object-fit:contain}
'''
html=html.replace('</style>',css+'</style>',1)
old='<div class="paper chapter-paper"><div class="mini-bar">真实章节 / 官方阅读页</div><img data-layout-allow-overflow src="assets/chapter-excerpt.jpg"><div id="chapter-box" class="chapter-box"></div></div>'
new='<div class="paper chapter-paper"><div class="mini-bar">官方阅读页 / 标题原图摘录</div><div class="chapter-image-window"><img data-layout-allow-overflow src="assets/chapter-excerpt.jpg"><div id="chapter-box" class="chapter-box"></div></div><p class="chapter-quote"><span class="chapter-quote-label">原文摘录</span>本节条目按主题分成下面几块，括号里是条号。</p></div>'
assert html.count(old)==1
html=html.replace(old,new)
(P/'index.html').write_text(html)
(Q/'index-v7.html.txt').write_text(html)
record={'source_dimensions':{'github-excerpt.jpg':[844,224],'chapter-excerpt.jpg':[660,590],'cost-excerpt.jpg':[654,244],'source-excerpt.jpg':[654,120]},'chapter':{'source_title_text':'23. 学什么技能划算','source_title_rect_xywh':[1,37,204,24],'source_frame_rect_xywh':[0,31,213,37],'source_display_region_xywh':[0,25,286,50],'scale':3,'image_offset_in_window':[18,-75],'title_rect_in_window_xywh':[21,36,612,72],'frame_rect_in_window_xywh':[18,18,639,111],'next_paragraph_first_text_y_source':78,'frame_bottom_source':68,'excerpt_sentence':'本节条目按主题分成下面几块，括号里是条号。','sentence_source_rect_xywh':[1,296,442,19],'mapping':'window_x=18+3*source_x; window_y=-75+3*source_y; scene/windowIn transform applies to title and frame together; stroke 4px, transparent fill','scope_label':'官方阅读页 / 标题原图摘录；原文摘录','note':'Coordinates visually measured from the actual source. Final DOM and exported frames are additional evidence, not OCR-perfect geometry.'},'whole_images':['github-excerpt.jpg','cost-excerpt.jpg','source-excerpt.jpg'],'protected_structure_unchanged':{'audio_and_video_tags':True,'caption_tags':True,'cover':True,'timing_and_animation_script':True},'before_sha256':hashlib.sha256(frozen.encode()).hexdigest(),'after_sha256':hashlib.sha256(html.encode()).hexdigest(),'status':'IMPLEMENTED_PENDING_EXPORTED_FRAME_REVIEW'}
(Q/'source-coordinates.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('v7 visual patch applied; protected timing/media/captions unchanged')
