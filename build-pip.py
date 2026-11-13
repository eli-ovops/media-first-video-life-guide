from pathlib import Path
import re, json, shutil

root=Path(__file__).resolve().parent
current=(root/'index.html').read_text()
backup=root/'evidence/before-pip';backup.mkdir(exist_ok=True)
if not (backup/'index.html.txt').exists():
    shutil.copyfile(root/'index.html',backup/'index.html.txt')
    shutil.copyfile(root/'design.md',backup/'design.md')
captions=re.findall(r'<div[^>]*class="clip caption"[^>]*>.*?</div>',current,re.S)
audios=re.findall(r'<audio\b[^>]*>.*?</audio>',current,re.S)
assert len(captions)==34, f'Existing subtitle count changed: {len(captions)}'
assert len(audios)==5, f'Existing audio count changed: {len(audios)}'

css='''
@font-face{font-family:GuideSans;src:url("assets/fonts/heiti.ttc")}@font-face{font-family:GuideSerif;src:url("assets/fonts/songti.ttc")}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:#17251e;font-family:GuideSans,sans-serif;color:#f5f1e8}#root{width:100%;height:100%;position:relative;overflow:hidden}.clip{position:absolute}.portrait{inset:0;width:1080px;height:1920px;object-fit:cover;z-index:0}
.caption{left:64px;top:1510px;width:920px;min-height:98px;display:flex;justify-content:center;align-items:center;z-index:40}.caption p{font-size:55px;line-height:1.25;max-width:920px;text-align:center;color:#f5f1e8;background:#17251ef2;border-radius:18px;padding:14px 24px;box-shadow:0 3px 10px #17251e40;font-weight:600}
.hook{left:72px;top:140px;width:936px;z-index:15}.hook-body{display:flex;align-items:center;gap:24px;border:3px solid #3f6852;background:#17251e;border-radius:24px;padding:24px 32px;min-height:170px}.num{font-size:40px;color:#dfed8a}.hook h2{font-size:73px;line-height:1.13}.hook p{font-size:34px;color:#dfed8a;margin-top:12px}.privacy-note{left:72px;top:80px;z-index:10;font-size:28px;letter-spacing:3px;color:#dfed8a}
.pip{left:72px;top:88px;width:936px;height:570px;z-index:20;overflow:hidden;border-radius:26px;box-shadow:0 18px 45px #10251a55}.pip-body{width:100%;height:100%;position:relative;padding:28px 34px 68px;background:#f5f1e8;color:#17251e;border:3px solid #d4dccd;border-radius:26px;overflow:hidden}.kicker{font-size:27px;letter-spacing:2px;color:#23563e;font-weight:600}.pip h1{font-family:GuideSerif,serif;font-size:74px;line-height:1.12;margin-top:14px;letter-spacing:-2px}.pip h2{font-size:58px;line-height:1.15;margin-top:12px}.pip p.sub{font-size:34px;line-height:1.3;margin-top:14px}.pip-credit{position:absolute;left:34px;bottom:16px;font-size:24px;line-height:1.3;color:#23563e}.paper{border:2px solid #d0d8c8;border-radius:17px;overflow:hidden;background:#fffdf7}.paper img{display:block;width:100%}.mini-bar{background:#e4e9dd;color:#23563e;font-size:25px;padding:11px 18px}.reveal-paper{margin-top:22px}.reveal-paper img{height:196px;object-fit:cover}.tagrow{display:flex;gap:15px;margin-top:16px}.tagrow span{font-size:29px;color:#17251e;background:#dfed8a;padding:8px 17px;border-radius:9px}
#pip-toc{height:650px}.toc-main{display:grid;grid-template-columns:360px 1fr;gap:28px;margin-top:20px}.toc-aperture{height:432px;border:2px solid #d0d8c8;background:#fafaf7;border-radius:18px;overflow:hidden}.toc-notes{display:flex;flex-direction:column;gap:16px}.toc-row{display:flex;align-items:center;gap:20px;padding:15px 0;border-bottom:2px solid #d5ddce}.toc-row b{font-size:49px;color:#23563e;font-family:GuideSerif,serif;min-width:65px}.toc-row p{font-size:40px;line-height:1.2}.toc-video-mask{position:absolute;left:109px;top:258px;width:356px;height:428px;overflow:hidden;border-radius:16px;z-index:23;pointer-events:none}.toc-vid{position:absolute;left:0;top:-95px;width:1000px;height:1778px;object-fit:fill}
.chapter-paper{margin-top:22px;height:335px;position:relative}.chapter-paper img{width:100%;object-fit:cover;object-position:top}.chapter-box{position:absolute;left:8px;top:48px;width:754px;height:73px;border:5px solid #23563e;border-radius:10px;background:#dfed8a18;transform-origin:left center}
.fields{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}.field{border:2px solid #23563e;border-radius:16px;padding:16px 22px;background:#fffdf7}.field p{font-size:27px;color:#23563e}.field h3{font-size:54px;line-height:1.18;margin-top:8px}.underline{height:6px;margin-top:10px;background:#c8db68;transform-origin:left center}.cost-paper{margin-top:18px;height:203px}.cost-paper img{width:100%;object-position:top;object-fit:cover}
.source-paper{margin-top:25px;border:3px solid #23563e;border-radius:18px;overflow:hidden}.source-paper img{width:100%;display:block}.doi{display:inline-block;font-size:31px;color:#17251e;background:#dfed8a;border-radius:10px;padding:12px 14px;margin-top:20px}.source-context{font-size:29px;line-height:1.35;margin-top:18px;color:#23563e}.small-banner{left:72px;top:130px;width:936px;z-index:16}.small-body{background:#17251ef2;border:3px solid #42684f;border-radius:24px;padding:26px 34px}.small-body h2{font-size:66px;line-height:1.2;color:#dfed8a}.small-body p{font-size:35px;color:#f5f1e8;margin-top:12px}.progress{position:absolute;left:0;bottom:0;width:1080px;height:6px;background:#dfed8a;transform-origin:left center;z-index:50}
'''
credit='<p class="pip-credit">原作 eternity4719 · CC BY 4.0 · 页面摘录/改编</p>'
parts=['<video id="a-roll" class="clip portrait" src="edit/redaction-v2/master-redacted.mp4" muted playsinline data-start="0" data-duration="59" data-track-index="0"></video>',*audios]
parts.append('<div id="privacy-note" class="clip privacy-note" data-start="0" data-duration="10.7" data-track-index="1">生活问题 / 先去哪查</div>')
for i,(start,dur,title,small) in enumerate([(0,3.1,'被裁员后','先处理什么？'),(3.1,3.2,'租房遇到纠纷','该去查哪些规定？'),(6.3,4.4,'想学一门技能','到底值不值得花钱？')]):
    parts.append(f'<section id="hook-{i}" class="clip hook" data-start="{start}" data-duration="{dur}" data-track-index="1"><div id="hook-body-{i}" class="hook-body"><span class="num">0{i+1}</span><div><h2>{title}</h2><p>{small}</p></div></div></section>')

parts.append('<section id="pip-reveal" class="clip pip" data-start="10.7" data-duration="10.65" data-track-index="2"><div id="reveal-body" class="pip-body"><p class="kicker">GitHub / 免费资料</p><h1>高性价比人生指南</h1><div class="paper reveal-paper"><div class="mini-bar">真实项目页面 / HowToLiveBetter</div><img src="assets/github-excerpt.jpg"></div><div class="tagrow"><span>租房</span><span>换工作</span><span>学技能</span></div>'+credit+'</div></section>')
parts.append('<section id="pip-toc" class="clip pip" data-start="21.5" data-duration="6.3" data-track-index="3"><div id="toc-body" class="pip-body"><p class="kicker">按问题翻章节</p><h2>需要时，翻对应章节</h2><div class="toc-main"><div class="toc-aperture"></div><div class="toc-notes"><div id="toc-rent" class="toc-row"><b>15</b><p>租房与买房</p></div><div id="toc-work" class="toc-row"><b>19</b><p>在职、离职和工伤</p></div><div id="toc-skill" class="toc-row"><b>23</b><p>学什么技能划算</p></div></div></div>'+credit+'</div></section>')
parts.append('<div id="toc-mask" class="toc-video-mask"><video id="toc-recording" class="clip toc-vid" data-layout-allow-overflow src="assets/toc-scroll.mp4" muted playsinline data-start="21.82" data-duration="5.6" data-track-index="4"></video></div>')
parts.append('<section id="pip-chapter" class="clip pip" data-start="30.0" data-duration="3.1" data-track-index="2"><div id="chapter-body" class="pip-body"><p class="kicker">具体例子 / 第 23 章</p><h2>学什么技能划算</h2><div class="paper chapter-paper"><div class="mini-bar">真实章节 / 官方阅读页</div><img data-layout-allow-overflow src="assets/chapter-excerpt.jpg"><div id="chapter-box" class="chapter-box"></div></div>'+credit+'</div></section>')
parts.append('<section id="pip-cost" class="clip pip" data-start="33.2" data-duration="6.45" data-track-index="3"><div id="cost-body" class="pip-body"><p class="kicker">把成本和收益放一起</p><h2>花掉什么，换来什么？</h2><div class="fields"><div id="field-cost" class="field"><p>成本</p><h3>钱＋时间</h3><div id="cost-line" class="underline"></div></div><div id="field-return" class="field"><p>收益</p><h3>换来什么</h3><div id="return-line" class="underline"></div></div></div><div class="paper cost-paper"><img data-layout-allow-overflow src="assets/cost-excerpt.jpg"></div>'+credit+'</div></section>')
parts.append('<section id="pip-sources" class="clip pip" data-start="39.8" data-duration="6.45" data-track-index="2"><div id="sources-body" class="pip-body"><p class="kicker">顺着来源继续查</p><h2>来源链接，也列在后面</h2><div id="source-paper" class="source-paper"><img src="assets/source-excerpt.jpg"></div><p class="doi">doi.org/10.1016/j.techfore.2016.08.019</p><p class="source-context">示例条目展开的原始来源</p>'+credit+'</div></section>')
parts.append('<section id="save" class="clip small-banner" data-start="46.7" data-duration="5" data-track-index="1"><div id="save-body" class="small-body"><h2>先把目录存下来</h2><p>需要的时候，再翻对应章节。</p></div></section>')
parts.append('<section id="cta" class="clip small-banner" data-start="51.7" data-duration="7.3" data-track-index="1"><div id="cta-body" class="small-body"><h2>文档已整理</h2><p id="cta-action">想要的朋友，评论区留言。</p></div></section>')
parts += captions
parts.append('<div id="progress" class="progress" data-layout-ignore></div>')
js='''
const E="cubic-bezier(.2,0,0,1)";
function anim(id,k,start,d,easing=E){const el=document.getElementById(id);if(!el)return;const a=el.animate(k,{delay:start*1000,duration:d*1000,easing,fill:"both",iterations:1});a.pause();}
function enter(id,start,d=.35){anim(id,[{transform:"translateY(-18px) scale(.97)",opacity:0},{transform:"translateY(0px) scale(1)",opacity:1}],start,d);}
function windowIn(id,start,end){const d=end-start;anim(id,[{transform:"translateX(100px) scale(.97)",opacity:0,offset:0},{transform:"translateX(0px) scale(1)",opacity:1,offset:.32/d},{transform:"translateX(0px) scale(1)",opacity:1,offset:1-.28/d},{transform:"translateY(-16px) scale(.99)",opacity:0,offset:1}],start,d,"linear");}
enter("hook-body-0",0,.4);enter("hook-body-1",3.1);enter("hook-body-2",6.3);
windowIn("reveal-body",10.7,21.35);windowIn("toc-body",21.5,27.8);enter("toc-rent",21.95);enter("toc-work",22.15);enter("toc-skill",22.35);
windowIn("chapter-body",30,33.1);anim("chapter-box",[{transform:"scaleX(0)",opacity:0},{transform:"scaleX(1)",opacity:1}],31.25,.4);
windowIn("cost-body",33.2,39.65);enter("field-cost",33.5);enter("field-return",36);anim("cost-line",[{transform:"scaleX(0)"},{transform:"scaleX(1)"}],33.85,.4);anim("return-line",[{transform:"scaleX(0)"},{transform:"scaleX(1)"}],36.3,.4);
windowIn("sources-body",39.8,46.25);enter("source-paper",40.1,.45);enter("save-body",46.7);enter("cta-body",51.7);enter("cta-action",55.3);
anim("progress",[{transform:"scaleX(0)"},{transform:"scaleX(1)"}],0,59,"linear");
'''
css+='\n.chapter-box{top:96px;height:70px}.cost-paper{height:165px}\n'
doc='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><style>'+css+'</style></head><body><main id="root" data-composition-id="main" data-no-timeline data-start="0" data-duration="59" data-width="1080" data-height="1920" data-fps="30">'+''.join(parts)+'</main><script>'+js+'</script></body></html>'
(root/'index.html').write_text(doc)
(root/'index.motion.json').write_text(json.dumps({'duration':59,'assertions':[{'kind':'appearsBy','selector':'#hook-body-0','bySec':.5},{'kind':'staysInFrame','selector':'#progress','fromSec':0,'toSec':59}]},indent=2))
print(json.dumps({'style':'person-primary with upper inset windows','captions_preserved':len(captions),'audio_tracks_preserved':len(audios),'safe_video':'edit/redaction-v2/master-redacted.mp4','full_screen_document_panels':0},ensure_ascii=False))
