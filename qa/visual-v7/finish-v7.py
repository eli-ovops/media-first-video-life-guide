# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json,hashlib
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parents[2];Q=P/'qa/visual-v7';F=Q/'final'
stage=next(P.parent.glob('*/04-*'))
r=json.loads((F/'verification.json').read_text()); assert r['technical_passed']
manifest=json.loads((F/'frame-manifest.json').read_text())
sample=next(x for x in manifest if x['frame_index']==975)
im=np.array(Image.open(sample['path']).convert('RGB'));m=(abs(im[:,:,0].astype(int)-35)<18)&(abs(im[:,:,1].astype(int)-86)<18)&(abs(im[:,:,2].astype(int)-62)<18)
m[:280]=False;m[450:]=False;m[:,:120]=False;m[:,780:]=False
rows=np.where(m.sum(axis=1)>500)[0];cols=np.where(m.sum(axis=0)>70)[0]
c=json.loads((Q/'source-coordinates.json').read_text())
c['chapter']['stable_canvas_frame_rect_xywh']=[129,316,639,111]
c['chapter']['stable_canvas_title_rect_xywh']=[132,334,612,72]
c['chapter']['stable_canvas_image_origin']=[129,223]
c['chapter']['final_mapping']='canvas_x=129+3*source_x; canvas_y=223+3*source_y at settled chapter card; entry/exit applies one common parent transform'
c['chapter']['actual_export_border_pixel_detection']={'frame_index':975,'time':32.5,'detected_horizontal_border_rows':rows.tolist(),'detected_vertical_border_cols':cols.tolist(),'method':'RGB tolerance 18 around #23563e, restricted expected rectangle; rendered pixels support geometry, not OCR'}
c['chapter']['highlight_animation']='31.75—32.15秒：固定矩形opacity淡入，不再scaleX扫字；卡片退场时与原图同一父级变换'
c['status']='IMPLEMENTED_EXPORTED_SAMPLES_READ_PENDING_STAGE05'
(Q/'source-coordinates.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
def entry(p):return {'path':str(p),'bytes':p.stat().st_size,'mtime':datetime.fromtimestamp(p.stat().st_mtime,timezone(timedelta(hours=8))).isoformat(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
new_files=[x for x in Q.rglob('*') if x.is_file()]+[P/'revise-v7.py',P/'revise-highlight-v7.py',Path(r['video']),P/'renders/人生指南-视觉修订-中英双语-v7.mp4']
media=[x for x in new_files if x.suffix.lower() in ['.mp4','.jpg','.png','.wav']]
media_bytes=sum(x.stat().st_size for x in media); assert media_bytes<=200*1024*1024
record={
 'stage':'04','content_id':'first-video-life-guide-visual-fix-v7','owner_thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7',
 'updated_at':datetime.now(timezone(timedelta(hours=8))).isoformat(),'status':'SUBMITTED_FOR_PMO_AND_STAGE05_REVIEW','visual_pass':'NOT_DECLARED',
 'goal':'修复首条资料裁切和章节框选；同类成本/来源卡按同一标准检查',
 'gate':{'allowed':True,'reason':'current content/stage/Owner/RELEASED/upstream imported baselines/input frozen SHA match','formal_import':'01—03当前正式接入既有不变输入，不补造历史PASS','source':str(P.parent/'流程协作/首条v7既有输入接入审查.json')},
 'final_outputs':{'video':entry(Path(r['video'])),'working_index':entry(P/'index.html'),'versioned_index':entry(Q/'index-v7.html.txt'),'cover_reused_unchanged':entry(P/'renders/封面海报-地球online攻略-v6.png'),'bilingual_srt_reused_unchanged':entry(P/'data/中英双语字幕-v3.srt')},
 'changes':['资料图按自然比例完整显示，去掉固定高度cover裁切，揭晓卡650px','章节明确标注标题原图摘录；按660×590源图、3倍缩放及偏移准确定位标题框，并附一条完整原文句子','框从scaleX改为固定位置opacity淡入，避免强调过程右边线扫过标题','成本图完整显示，卡片735px；来源图保留全幅，DOI与来源内容已核样本'],
 'protected':r['protected_html_sections_unchanged'],
 'technical_verification':r,
 'evidence':{'source_coordinates':str(Q/'source-coordinates.json'),'original_source_images':[str(P/'assets'/x) for x in ['github-excerpt.jpg','chapter-excerpt.jpg','cost-excerpt.jpg','source-excerpt.jpg']], 'final_frame_manifest':str(F/'frame-manifest.json'),'exported_frames':str(F/'exported-frames'),'final_contact_sheets':[str(F/f'export-contact-{i}.jpg') for i in range(1,5)],'check':str(F/'check-report.json'),'render':str(Q/'render-final.log'),'decode':str(F/'decode.log'),'audio':str(F/'verification.json'),'before_engine':str(Q/'index-before-v7.html.txt')},
 'actual_review':{'final_exported_samples':len(manifest),'read_contact_sheets':4,'time_scope':'封面0/0.467/0.5；资料出现/持有/退出11.2—21.9；章节出现/强调/退出30.5—33.6；成本33.7—40.133；来源40.3—46.8；结尾59.3','limitation':'静态采样覆盖多个阶段，不是连续完整动态看听；人工逐字、语气、眼神和手机实屏可读性仍由05与用户核验','content_readability':'主标题、章节标题与完整摘录、成本/收益大字及DOI用于主要阅读；全幅原图同时保留作出处，原图密集正文未声称手机逐字验收'},
 'first_render':{'video':str(P/'renders/人生指南-视觉修订-中英双语-v7.mp4'),'technical_passed':True,'why_not_final':'最终过程帧发现scaleX框右线短暂扫字，保留作对照，采用第二版固定框淡入','evidence':str(Q/'frame-manifest.json')},
 'budget':{'full_render_count':2,'max_full_renders':2,'new_retained_media_bytes':media_bytes,'new_retained_media_mib':round(media_bytes/1024/1024,2),'max_media_mib':200,'max_minutes':90,'cache':'原渲染缓存复用；工具自行结束本轮工作目录，无人工清理','usage':'UNKNOWN（0.8.91不支持usage）'},
 'routing':{'read_version':'ROUTING-2026-09-30-v3','handoff_version':'HANDOFF-2026-10-06-v1','target_model':'user default','target_effort':'medium','actual_model':'UNKNOWN','actual_effort':'UNKNOWN','actual_speed':'UNKNOWN'},
 'tool_limits':['HyperFrames 0.8.91不支持usage；未升级工具，用量UNKNOWN','keyframes --shot无法静态解析经anim函数封装的WAAPI目标，输出no statically resolved animated element；无命中阻断记录。使用已成功的同工具runtime snapshot及最终导出过程帧作为像素证据，不声明静态关键帧诊断通过','open_in_codex预览仅返回queued；HTTP200单独已核，不冒充用户已看到预览','曾提前在第二版编码/组装完成前启动核验，MP4尚不存在导致帧数为空/IndexError；原日志保留在verify-final-run.log与premature-final-decode.log。之后真实渲染退出0并artifact validated才重新核验；失败不计通过，不增加完整渲染次数'],
 'boundary':['未改共享流程状态/登记、根README/AGENTS或其他岗位','未运行旧构建器、未还原未遮照片旧v1','无安装/升级/付费/上传/外发/发布/删除','未给其他会话发送消息，未恢复1000视频研究'],
 'remaining_required_work':['PMO审04交付并决定05释放','05独立读取最终MP4、源图坐标及实际导出出现/强调/退出帧，核完整性、手机可读性和声画','用户全片终审；发布仍未授权'],
 'file_record':{'new_or_versioned_files':[entry(x) for x in new_files],'generated_handoff_files':[str(stage/'首条v7交付.json'),str(stage/'首条v7交付.md'),str(P/'evidence/视觉修订-v7制作记录.md')],'modified_existing':[str(P/'index.html'),str(P/'README.md')],'creation_source':'本輪两次本地修订导出、CLI检查/snapshot以及本地技术核验脚本；用户附件与现有源图仅只读','purpose_and_dependency':'最终版供05/用户审片；首轮、过程图、冻结/版本源码与失败日志支撑修订对照、验收与恢复，仍有后续用途','risk':'源码、媒体和验收证据保护，不清理','releasable_bytes':0,'existing_cache':'项目.render-cache约775MiB，两次导出复用，未人工改动/删除','temporary_files':'render工具生成的本轮work目录已自行收尾；QA/首轮对照仍用于审查，全部保留；无人工删除'},
 'next_action':'待PMO转05；本Owner不自行PASS或推进下游。'
}
(stage/'首条v7交付.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
md=f'''# 首条v7制作交付（待PMO与05验收）

最终审查文件：[人生指南-视觉修订-定框淡入-中英双语-v7.mp4]({r['video']})。版本SHA256 `{r['sha256']}`；{r['bytes']:,}字节，59.5秒/1080×1920/30fps/1785帧。

资料图与成本图按原图比例完整显示；章节明确显示标题原图摘录和完整原文句子。源图标题矩形(1,37,204,24)，3倍缩放，静止卡片成片标题矩形(132,334,612,72)，框矩形(129,316,639,111)。透明框留内边距，下一段源文从y78开始、框止于y68，未包含下一段。强调改固定框淡入，避免scaleX右边线在过程帧扫字。

v6封面前0.5秒地球online攻略/无本人、原声顺序、中文字幕在上英文在下、PIP及隐私母版引用均保留。源码对应片段检查通过；原声解码样本与v6完全一致，相关性1.0。

最终文件完整解码1785帧、progress=end、退出0，无解码/时间戳错误或黑帧事件；首15帧稳定与0.5秒正文切换通过。check各层0error，46结构warning保留，对比度40/40通过。渲染为screenshot capture、hardware GPU；实际日志见工程qa/visual-v7/render-final.log。

已实际读最终MP4的37个采样帧（4张联系图）及重点单帧，覆盖资料、章节、成本、来源的出现/强调/退场。证据：[坐标]({Q/'source-coordinates.json'})｜[帧索引]({F/'frame-manifest.json'})｜[技术验证]({F/'verification.json'})。不是连续完整动态看听，不宣布视觉PASS；05独立质检和用户全片终审仍待进行。全幅原图的密集正文作为出处保留，手机逐字可读性尚未实屏验收；主要阅读信息以大标题、完整摘录、成本/收益字段和DOI呈现。

本轮2次完整渲染，新增保留媒体{media_bytes/1024/1024:.2f}MiB≤200MiB。首轮“视觉修订-中英双语-v7.mp4”保留作过程压字对照，不能误作本次最终审查版。工具复用，无安装/升级/上传/外发/发布/人工删除；共享状态、根文档、其他岗位未改。实际model/effort/speed与usage为UNKNOWN。

本轮门禁通过；01—03是当前正式导入不变既有输入，不补造历史验收。唯一Owner本会话，content_id=first-video-life-guide-visual-fix-v7。PMO审04交付后转05，不由本Owner自行PASS/放行。完整输入输出SHA、文件清单和边界见同目录首条v7交付.json。
'''
(stage/'首条v7交付.md').write_text(md)
(P/'evidence/视觉修订-v7制作记录.md').write_text(md)
readme=(P/'README.md').read_text()
header='''**当前修订交付（2026-10-08，v7待独立质检）：** [固定标题框淡入＋资料完整展示版](renders/人生指南-视觉修订-定框淡入-中英双语-v7.mp4)已本地导出并完成制作技术核验；源截图裁切、章节框选及成本截图裁切已调整。59.5秒/1080×1920/30fps/1785帧，保留地球online攻略无本人封面、本人原声、双语、PIP和隐私遮盖。[制作记录](evidence/视觉修订-v7制作记录.md)｜[源图坐标](qa/visual-v7/source-coordinates.json)。待05独立视觉质检与用户全片终审，未发布。首轮v7文件仅作修订对照，以下v6及更早记录为历史。

'''
assert header not in readme
(P/'README.md').write_text(readme.replace('# 第一条短视频：《高性价比人生指南》\n\n','# 第一条短视频：《高性价比人生指南》\n\n'+header,1))
assert json.loads((stage/'首条v7交付.json').read_text())['final_outputs']['video']['sha256']==r['sha256']
print(json.dumps({'submitted':str(stage/'首条v7交付.json'),'media_mib':round(media_bytes/1024/1024,2),'final_sha256':r['sha256']}))
