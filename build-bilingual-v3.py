from pathlib import Path
import re,json,html,shutil

root=Path(__file__).resolve().parent
backup=root/'evidence/before-bilingual';backup.mkdir(exist_ok=True)
baseline=backup/'index.html.txt'
if not baseline.exists():
    shutil.copyfile(root/'index.html',baseline)
    shutil.copyfile(root/'design.md',backup/'design.md')
source=baseline.read_text()
rows=json.loads((root/'qa/bilingual-v3/translations.json').read_text())
assert len(rows)==34
translations={r['id']:dict(r) for r in rows}
translations['cap-11']['en']="I'd recommend saving it for later."
translations['cap-22']['en']='The suggestions also include'
translations['cap-23']['en']='their sources.'
translations['cap-33']['en']="I'll send it to you."
caption_records=[]
pattern=re.compile(r'(<div\b[^>]*\bid="(cap-\d+)"[^>]*>)(.*?)(</div>)',re.S)
def add_english(m):
    opening,id,body,closing=m.groups()
    r=translations[id]
    match=re.search(r'<p\b[^>]*>(.*?)</p>',body,re.S)
    assert match and html.unescape(re.sub('<[^>]+>','',match.group(1)))==r['zh'],id
    start=float(re.search(r'data-start="([^"]+)"',opening).group(1))+.5
    duration=float(re.search(r'data-duration="([^"]+)"',opening).group(1))
    if id=='cap-33':
        duration=1.0
        opening=re.sub(r'data-duration="[^"]+"','data-duration="1.0"',opening)
    caption_records.append({'id':id,'zh':r['zh'],'en':r['en'],'start':start,'end':round(start+duration,6)})
    newbody='<div class="caption-box"><p class="zh">'+html.escape(r['zh'])+'</p><p class="en" lang="en">'+html.escape(r['en'])+'</p></div>'
    return opening+newbody+closing
source=pattern.sub(add_english,source)
assert len(caption_records)==34
# Shift placement and every WAAPI cue by the inserted 15-frame silent poster.
source=re.sub(r'data-start="([\d.]+)"',lambda m:f'data-start="{float(m.group(1))+.5:.6f}"',source)
source=re.sub(r'<main\b[^>]*>',lambda m:re.sub('data-start="[^"]+"','data-start="0"',re.sub('data-duration="59"','data-duration="59.5"',m.group(0))),source,count=1)
assert 'delay:start*1000' in source
source=source.replace('delay:start*1000','delay:(start+.5)*1000')
source=re.sub(r'(<video\b[^>]*id="a-roll"[^>]*)(>)',r'\1 data-media-start="0"\2',source,count=1)
css='''
.caption{left:80px;top:1455px;width:920px;min-height:150px;align-items:flex-start}
.caption-box{display:flex;flex-direction:column;align-items:center;gap:9px;max-width:920px;padding:13px 22px;background:#17251ef2;border-radius:18px;box-shadow:0 3px 10px #17251e40}
.caption .caption-box p{background:none;padding:0;box-shadow:none;border-radius:0;text-align:center;max-width:876px;text-wrap:balance;line-height:1.23;font-weight:600}
.caption .caption-box p.zh{font-size:50px;color:#f5f1e8}
.caption .caption-box p.en{font-size:34px;color:#e3ebdc;font-weight:500;line-height:1.23}
#cover-v3{position:absolute;inset:0;width:1080px;height:1920px;z-index:60;overflow:hidden;background:#17251e}
.cover-photo{width:1080px;height:1920px;object-fit:cover;position:absolute;inset:0}
.cover-head{position:absolute;left:0;top:0;width:1080px;height:480px;background:#17251e;padding:65px 80px 25px;color:#f5f1e8}
.cover-kicker{font-size:38px;letter-spacing:3px;color:#dfed8a;line-height:1.3}
.cover-line{font-size:124px;font-weight:800;line-height:1.05;letter-spacing:-3px;margin-top:22px}
.cover-title{font-size:146px;font-weight:800;line-height:1.06;color:#dfed8a;letter-spacing:-6px;margin-top:10px}
.cover-footer{position:absolute;left:72px;right:72px;bottom:190px;background:#17251ef5;border:3px solid #435c43;border-radius:24px;padding:28px 30px;color:#f5f1e8}
.cover-footer h2{font-size:62px;line-height:1.2}
.cover-tags{display:flex;gap:16px;margin-top:24px}
.cover-tags span{font-size:36px;color:#17251e;background:#dfed8a;border-radius:10px;padding:11px 19px}
'''
source=source.replace('</style>',css+'</style>',1)
cover='''<section id="cover-v3" class="clip" data-start="0" data-duration="0.5" data-track-index="20"><img class="cover-photo" src="assets/poster-portrait-safe-v3.jpg"><div class="cover-head"><p class="cover-kicker">GitHub / 免费资料</p><p class="cover-line">免费的</p><h1 class="cover-title">人生说明书</h1></div><div class="cover-footer"><h2>高性价比人生指南</h2><div class="cover-tags"><span>租房</span><span>换工作</span><span>学技能</span></div></div></section>'''
source=source.replace('</main>',cover+'</main>',1)
(root/'index.html').write_text(source)
(root/'data').mkdir(exist_ok=True)
(root/'data/captions-bilingual-v3.json').write_text(json.dumps({'version':3,'duration':59.5,'poster_seconds':.5,'source_timing_offset':.5,'captions':caption_records,'notes':'英文自然译文，中文沿用接受的v2显示；书名为本视频译名，非官方译名；末条留到片尾以便阅读。'},ensure_ascii=False,indent=2))
def srt_time(t):
    ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
srt='\n\n'.join(f'{i+1}\n{srt_time(r["start"])} --> {srt_time(r["end"])}\n{r["zh"]}\n{r["en"]}' for i,r in enumerate(caption_records))+'\n'
(root/'data/中英双语字幕-v3.srt').write_text(srt)
(root/'index.motion.json').write_text(json.dumps({'duration':59.5,'assertions':[{'kind':'appearsBy','selector':'#cover-v3','bySec':0},{'kind':'appearsBy','selector':'#hook-body-0','bySec':1},{'kind':'staysInFrame','selector':'#progress','fromSec':.5,'toSec':59.5}]},indent=2))
(root/'evidence/bilingual-v3-build.json').write_text(json.dumps({'duration':59.5,'poster_frames':15,'fps':30,'all_existing_cues_offset_seconds':.5,'unchanged_original_voice':True,'bilingual_count':34,'last_caption_duration':1.0,'source_snapshot':str(baseline),'new_asset':str(root/'assets/poster-portrait-safe-v3.jpg'),'generated_files':[str(root/'index.html'),str(root/'data/captions-bilingual-v3.json'),str(root/'data/中英双语字幕-v3.srt')],'poster_portrait_origin':'8秒时点，来自已遮照片的隐私母版，非原片未处理帧'},ensure_ascii=False,indent=2))
print(json.dumps({'duration':59.5,'bilingual_groups':34,'poster_frames':15,'source_offset':.5},ensure_ascii=False))
