from pathlib import Path
import json, html, shutil
root=Path(__file__).resolve().parent
caption_data=json.loads((root/'edit/captions.json').read_text())
captions=[]
for i,c in enumerate(caption_data['captions']):
    text=c['text']
    # 屏幕字幕清理一个识别未确认的赘词，不改变领取动作，不声称逐字字幕。
    if text=='想要的朋友只是在': text='想要的朋友'
    captions.append(f'<div class="clip caption" id="cap-{i}" data-start="{c["start"]}" data-duration="{c["end"]-c["start"]:.3f}" data-track-index="8"><p>{html.escape(text)}</p></div>')

css='''
@font-face{font-family:GuideSans;src:url("assets/fonts/heiti.ttc")}@font-face{font-family:GuideSerif;src:url("assets/fonts/songti.ttc")}
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1920px;overflow:hidden;background:#17251e;font-family:GuideSans,sans-serif;color:#f5f1e8}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#17251e}.clip{position:absolute}.portrait{inset:0;width:1080px;height:1920px;object-fit:cover;z-index:0}
.caption{left:64px;top:1510px;width:920px;min-height:98px;display:flex;justify-content:center;align-items:center;z-index:40}.caption p{font-size:55px;line-height:1.25;max-width:920px;text-align:center;color:#f5f1e8;background:#17251ef2;border-radius:18px;padding:14px 24px;box-shadow:0 3px 10px #17251e40;font-weight:600}
.hook{left:72px;top:172px;width:936px;z-index:15}.hook-body{display:flex;align-items:center;gap:24px;background:#17251ef2;border-radius:24px;padding:24px 34px;min-height:160px}.hook .num{font-size:40px;color:#dfed8a;font-weight:700}.hook h2{font-size:74px;line-height:1.13;letter-spacing:-2px}.hook .small{font-size:34px;color:#dfed8a;margin-top:10px}
.sheet{inset:0;width:1080px;height:1920px;z-index:20;overflow:hidden}.sheet-body{position:absolute;inset:0;background:#f5f1e8;color:#17251e;overflow:hidden;padding:170px 72px 380px}.kicker{font-size:30px;letter-spacing:4px;color:#23563e;font-weight:600}.chapter-number{font-size:36px;display:inline-block;color:#f5f1e8;background:#23563e;border-radius:12px;padding:10px 18px}.sheet h1{font-family:GuideSerif,serif;font-weight:900;font-size:104px;line-height:1.14;letter-spacing:-3px;margin-top:48px}.sheet h2{font-size:70px;line-height:1.18;margin-top:24px}.sheet .desc{font-size:42px;line-height:1.4;margin-top:30px}.rule{height:4px;background:#23563e;width:936px;margin-top:32px;transform-origin:left center}.paper{background:#fffdf7;border:3px solid #d8dccc;border-radius:26px;overflow:hidden;box-shadow:12px 18px 0 #dde3d4}.browserbar{height:70px;background:#e6eadf;display:flex;align-items:center;padding:0 26px;gap:12px;font-size:27px;color:#17251e}.dots{display:flex;gap:9px;margin-right:12px}.dots i{display:block;width:12px;height:12px;background:#23563e;border-radius:50%}.paper-image{width:100%;display:block}.source-credit{position:absolute;left:72px;bottom:260px;width:936px;font-size:27px;line-height:1.45;color:#23563e;max-width:936px}.source-credit .url{font-size:26px;overflow-wrap:anywhere}
#reveal-paper{margin-top:70px;position:relative}.reveal-image{width:936px;height:249px;object-fit:cover}.resource-tags{display:flex;gap:14px;margin-top:36px}.tag{font-size:34px;background:#dfed8a;border-radius:11px;padding:14px 22px;color:#17251e}.book-corner{position:absolute;right:-72px;bottom:-160px;font-family:GuideSerif,serif;font-size:300px;color:#e6eadf;z-index:-1}
.toc-grid{display:grid;grid-template-columns:476px 420px;gap:40px;margin-top:45px}.toc-window{height:1090px;overflow:hidden;position:relative;background:#f8f8f7;border:3px solid #d8dccc;border-radius:24px}.toc-vid{width:1338px;height:2378px;position:absolute;left:0;top:-90px;object-fit:fill}.toc-note{padding-top:25px}.index-item{margin-bottom:55px;padding-bottom:35px;border-bottom:3px solid #d8dccc}.index-number{font-family:GuideSerif,serif;font-size:64px;color:#23563e;line-height:1.2}.index-item h3{font-size:45px;line-height:1.3;margin-top:10px}.index-item p{font-size:32px;line-height:1.45;margin-top:12px;color:#23563e}
#chapter-paper{margin-top:38px;position:relative;height:950px}.chapter-img{width:936px;display:block}.chapter-emphasis{position:absolute;left:17px;top:87px;width:720px;height:110px;border:6px solid #23563e;border-radius:12px;background:#dfed8a20;pointer-events:none;transform-origin:left center}
.field-pair{display:flex;gap:22px;margin-top:44px}.field{flex:1;border:3px solid #23563e;border-radius:22px;padding:28px;background:#fffdf7}.field .mini{font-size:32px;color:#23563e}.field h3{font-size:72px;margin-top:10px}.field p{font-size:37px;margin-top:16px;line-height:1.3}.cost-paper{margin-top:48px;overflow:hidden}.cost-paper img{display:block;width:936px}.field-under{height:8px;background:#dfed8a;width:100%;transform-origin:left}
.source-window{margin-top:32px;position:relative;height:760px;border:3px solid #d8dccc;border-radius:24px;overflow:hidden;background:#fafafa}.source-video{position:absolute;left:0;top:-85px;width:984px;height:1749px;object-fit:fill}.source-excerpt{margin-top:26px;padding:30px;background:#fffdf7;border:3px solid #23563e;border-radius:22px}.source-excerpt .title{font-size:38px;color:#23563e;margin-bottom:16px}.source-excerpt img{width:868px;display:block}.source-outline{position:absolute;left:45px;top:570px;width:845px;height:155px;border:6px solid #23563e;border-radius:12px;background:#dfed8a18}
.save-tag{left:72px;top:170px;width:936px;z-index:15}.save-body{border-radius:24px;padding:30px;background:#17251ef2}.save-tag h2{font-size:66px;line-height:1.2;color:#dfed8a}.save-tag p{font-size:35px;margin-top:18px;color:#f5f1e8}.cta{left:72px;top:175px;width:936px;z-index:16}.cta-body{border-radius:24px;padding:32px 40px;background:#17251ef2;border:3px solid #dfed8a}.cta h2{font-size:74px;line-height:1.2;color:#dfed8a}.cta p{font-size:39px;margin-top:18px;color:#f5f1e8}.progress{position:absolute;bottom:0;left:0;width:1080px;height:6px;background:#dfed8a;z-index:50;transform-origin:left center}
'''

markup='''
<video id="a-roll" class="clip portrait" src="edit/master.mp4" muted playsinline data-start="0" data-duration="59" data-track-index="0"></video>
<audio id="narration" src="edit/master.mp4" data-start="0" data-duration="59" data-track-index="9" data-volume="1"></audio>
'''
hooks=[(0.0,3.1,'01','被裁员后','先处理什么？'),(3.1,3.2,'02','租房遇到纠纷','该去查哪些规定？'),(6.3,4.4,'03','想学一门技能','到底值不值得花钱？')]
for i,(start,dur,num,title,small) in enumerate(hooks):
    markup+=f'<section id="hook-{i}" class="clip hook" data-start="{start}" data-duration="{dur}" data-track-index="1"><div class="hook-body" id="hook-body-{i}"><span class="num">{num}</span><div><h2>{title}</h2><p class="small">{small}</p></div></div></section>'

credit='<div class="source-credit"><p>原作 eternity4719 · CC BY 4.0 · 页面摘录/改编</p><p class="url">github.com/eternity4719/HowToLiveBetter</p></div>'
markup+='''
<section id="reveal" class="clip sheet" data-start="10.7" data-duration="11.15" data-track-index="2"><div id="reveal-body" class="sheet-body"><p class="kicker">GITHUB / 免费资料</p><h1 id="reveal-title">高性价比<br>人生指南</h1><div class="rule" id="reveal-rule"></div><p class="desc">遇到问题，先翻对应章节。</p><div id="reveal-paper" class="paper"><div class="browserbar"><span class="dots"><i></i><i></i><i></i></span>HowToLiveBetter / README</div><img id="repo-image" class="reveal-image" src="assets/github-excerpt.jpg"></div><div class="resource-tags"><span class="tag">租房</span><span class="tag">换工作</span><span class="tag">学技能</span></div>'''+credit+'''</div></section>
<section id="toc" class="clip sheet" data-start="21.5" data-duration="6.75" data-track-index="3"><div id="toc-body" class="sheet-body"><p class="kicker">01 / 按问题翻章节</p><h2>碰到什么问题<br>就翻哪一章</h2><div class="toc-grid"><div class="toc-window"><video id="toc-recording" class="clip toc-vid" src="assets/toc-scroll.mp4" muted playsinline data-start="21.6" data-duration="6.3" data-track-index="4"></video></div><div class="toc-note"><div id="toc-rent" class="index-item"><span class="index-number">15</span><h3>租房与买房</h3><p>租房的问题</p></div><div id="toc-work" class="index-item"><span class="index-number">19</span><h3>在职、离职<br>和工伤</h3><p>工作的问题</p></div><div id="toc-skill" class="index-item"><span class="index-number">23</span><h3>学什么<br>技能划算</h3><p>学习的问题</p></div></div></div>'''+credit+'''</div></section>
<section id="chapter" class="clip sheet" data-start="27.9" data-duration="5.65" data-track-index="2"><div id="chapter-body" class="sheet-body"><span class="chapter-number">第 23 章</span><h2>学什么技能划算</h2><p class="desc">先看这一章怎么组织信息。</p><div id="chapter-paper" class="paper"><div class="browserbar">真实章节 / 官方在线阅读页</div><img class="chapter-img" src="assets/chapter-excerpt.jpg"><div id="chapter-box" class="chapter-emphasis"></div></div>'''+credit+'''</div></section>
<section id="cost" class="clip sheet" data-start="33.2" data-duration="6.95" data-track-index="3"><div id="cost-body" class="sheet-body"><p class="kicker">02 / 把成本和收益放一起</p><h2>花掉什么？<br>可能换来什么？</h2><div class="field-pair"><div id="field-cost" class="field"><p class="mini">成本</p><h3>钱＋时间</h3><p>先看要投入什么</p><div id="cost-line" class="field-under"></div></div><div id="field-return" class="field"><p class="mini">收益</p><h3>换来什么</h3><p>再看资料怎么解释</p><div id="return-line" class="field-under"></div></div></div><div class="paper cost-paper"><div class="browserbar">示例条目的原页面字段</div><img src="assets/cost-excerpt.jpg"></div>'''+credit+'''</div></section>
<section id="sources" class="clip sheet" data-start="39.8" data-duration="7.25" data-track-index="2"><div id="sources-body" class="sheet-body"><p class="kicker">03 / 顺着来源继续查</p><h2>来源链接<br>也列在后面</h2><div class="source-window"><video id="source-recording" class="clip source-video" src="assets/source-scroll.mp4" muted playsinline data-start="39.95" data-duration="6.4" data-track-index="5"></video><div id="source-box" class="source-outline"></div></div><div id="source-link-card" class="source-excerpt"><p class="title">实际展开的来源</p><img src="assets/source-excerpt.jpg"></div>'''+credit+'''</div></section>
<section class="clip save-tag" data-start="46.7" data-duration="5" data-track-index="1"><div id="save-body" class="save-body"><h2>先把目录存下来</h2><p>需要的时候，再翻对应章节。</p></div></section>
<section class="clip cta" data-start="51.7" data-duration="7.3" data-track-index="1"><div id="cta-body" class="cta-body"><h2>文档已整理</h2><p id="cta-action">想要的朋友，评论区留言。</p></div></section>
<div id="progress" class="progress" data-layout-ignore></div>
'''
# 所有实际录像位于主composition直属层，避免timed plain wrapper嵌套video。
markup=markup.replace('<video id="toc-recording" class="clip toc-vid" src="assets/toc-scroll.mp4" muted playsinline data-start="21.6" data-duration="6.3" data-track-index="4"></video>','<div class="toc-placeholder"></div>')
markup=markup.replace('<video id="source-recording" class="clip source-video" src="assets/source-scroll.mp4" muted playsinline data-start="39.95" data-duration="6.4" data-track-index="5"></video>','<div class="source-placeholder"></div>')
# 静态裁切框的fixed geometry与所属纸面相同；视频仍为独立timed元素。
markup+='''<div class="toc-video-mask" style="position:absolute;left:72px;top:446px;width:476px;height:1090px;overflow:hidden;border-radius:24px;z-index:24;pointer-events:none"><video id="toc-recording" class="clip toc-vid" src="assets/toc-scroll.mp4" muted playsinline data-start="21.8" data-duration="6.1" data-track-index="4"></video></div>
<div class="source-video-mask" style="position:absolute;left:72px;top:390px;width:936px;height:760px;overflow:hidden;border-radius:24px;z-index:24;pointer-events:none"><video id="source-recording" class="clip source-video" src="assets/source-scroll.mp4" muted playsinline data-start="40.2" data-duration="6.4" data-track-index="5"></video></div>
'''
markup+=''.join(captions)
for i,t in enumerate([0.1,3.2,6.4]): markup+=f'<audio id="tap-{i}" src="assets/tap.wav" data-start="{t}" data-duration="0.075" data-track-index="10" data-volume="0.2"></audio>'
markup+='<audio id="reveal-sfx" src="assets/reveal.wav" data-start="10.75" data-duration="0.18" data-track-index="10" data-volume="0.16"></audio>'

js='''
const E="cubic-bezier(.2,0,0,1)";
function anim(id,keyframes,start,duration,easing=E){const el=document.getElementById(id);if(!el)return;const a=el.animate(keyframes,{delay:start*1000,duration:duration*1000,easing,fill:"both",iterations:1});a.pause();}
function enter(id,start,duration=.38){anim(id,[{transform:"translateY(24px) scale(.96)",opacity:0},{transform:"translateY(0px) scale(1)",opacity:1}],start,duration);}
function paper(id,start,end,dir=1){const dur=end-start;const inD=.32;const outD=.32;anim(id,[{transform:`translateX(${dir*1080}px)`,opacity:1,offset:0},{transform:"translateX(0px)",opacity:1,offset:inD/dur},{transform:"translateX(0px)",opacity:1,offset:1-outD/dur},{transform:`translateX(${-dir*80}px)`,opacity:0,offset:1}],start,dur,"linear");}
enter("hook-body-0",0,.4);enter("hook-body-1",3.1,.36);enter("hook-body-2",6.3,.36);
paper("reveal-body",10.7,21.85);enter("reveal-title",10.8,.5);anim("reveal-rule",[{transform:"scaleX(0)"},{transform:"scaleX(1)"}],11.1,.55);enter("reveal-paper",11.15,.45);
anim("repo-image",[{transform:"scale(1)"},{transform:"scale(1.035)"}],13,6.8,"linear");
paper("toc-body",21.5,28.25);enter("toc-rent",21.9,.4);enter("toc-work",22.2,.4);enter("toc-skill",22.5,.4);
paper("chapter-body",27.9,33.55);anim("chapter-box",[{transform:"scaleX(0)",opacity:0},{transform:"scaleX(1)",opacity:1}],30.9,.5);
paper("cost-body",33.2,40.15);enter("field-cost",33.35,.4);enter("field-return",36.0,.4);anim("cost-line",[{transform:"scaleX(0)"},{transform:"scaleX(1)"}],33.7,.4);anim("return-line",[{transform:"scaleX(0)"},{transform:"scaleX(1)"}],36.3,.4);
paper("sources-body",39.8,47.05);enter("source-link-card",41,.5);anim("source-box",[{transform:"scaleY(0)",opacity:0},{transform:"scaleY(1)",opacity:1}],42,.4);
enter("save-body",46.7,.4);enter("cta-body",51.7,.4);enter("cta-action",55.3,.35);
anim("progress",[{transform:"scaleX(0)"},{transform:"scaleX(1)"}],0,59,"linear");
'''
css=css.replace('z-index:-1','z-index:0')
css+='\n.source-credit{top:1400px;bottom:auto;font-size:27px}.source-credit .url{font-size:27px}.toc-window{height:910px}.source-window{height:620px}.chapter-img,.cost-paper img{width:100%}\n'
markup=markup.replace('class="clip save-tag"','id="save" class="clip save-tag"').replace('class="clip cta"','id="cta" class="clip cta"').replace('top:446px;width:476px;height:1090px','top:446px;width:476px;height:910px').replace('top:390px;width:936px;height:760px','top:427px;width:936px;height:620px')
markup=markup.replace('id="toc-recording" class=','id="toc-recording" data-layout-allow-overflow class=').replace('id="source-recording" class=','id="source-recording" data-layout-allow-overflow class=').replace('id="repo-image" class=','id="repo-image" data-layout-allow-overflow class=')
document='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><style>'+css+'</style></head><body><main id="root" data-composition-id="main" data-no-timeline data-start="0" data-duration="59" data-width="1080" data-height="1920" data-fps="30">'+markup+'</main><script>'+js+'</script></body></html>'
(root/'index.html').write_text(document)
(root/'index.motion.json').write_text(json.dumps({'duration':59,'assertions':[{'kind':'appearsBy','selector':'#hook-body-0','bySec':0.5},{'kind':'staysInFrame','selector':'#progress','fromSec':0,'toSec':59}]},indent=2))
(root/'STORYBOARD.md').write_text('''# 首条人生指南视频
用户自主制作授权；storyboard:no，无需逐阶段问卷。实际口播59秒。

## Frame 1
status: animated
src: index.html#hook-0
beat: 真人三类生活问题；spring-pop-entrance，短关键词到位。
## Frame 2
status: animated
src: index.html#reveal
beat: GitHub真实截图揭晓；spring-pop-entrance、coordinate-target-zoom原则、css-push。
## Frame 3
status: animated
src: index.html#toc
beat: 真实目录录屏及章节索引；css-push，三个索引依次出现。
## Frame 4
status: animated
src: index.html#chapter
beat: 第23章原页与标题重点框；svg-path-draw强调原则。
## Frame 5
status: animated
src: index.html#cost
beat: 成本/收益两个信息层与真实字段；spring-pop-entrance，scaleX描线。
## Frame 6
status: animated
src: index.html#sources
beat: 真实滚动和展开来源，链接大图；css-push、spring-pop-entrance。
## Frame 7
status: animated
src: index.html#save-body
beat: 回真人收藏建议；短淡入。
## Frame 8
status: animated
src: index.html#cta-body
beat: 真人评论领取；spring-pop-entrance，不加入私信/FDE。

全部原生WAAPI暂停、有限动画、确定性seek；原声不换。字幕来自已记录ASR分句校正，非人工听音逐字定稿。真实页面日期2026-10-08；演示结构，不口播条目收益数值。
''')
print(json.dumps({'composition':str(root/'index.html'),'duration':59,'captions':len(captions),'runtime':'WAAPI','network_assets':0}))
