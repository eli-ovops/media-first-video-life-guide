# 第一条短视频：《高性价比人生指南》

**当前修订交付（2026-10-08，v7待独立质检）：** [固定标题框淡入＋资料完整展示版](renders/人生指南-视觉修订-定框淡入-中英双语-v7.mp4)已本地导出并完成制作技术核验；源截图裁切、章节框选及成本截图裁切已调整。59.5秒/1080×1920/30fps/1785帧，保留地球online攻略无本人封面、本人原声、双语、PIP和隐私遮盖。[制作记录](evidence/视觉修订-v7制作记录.md)｜[源图坐标](qa/visual-v7/source-coordinates.json)。待05独立视觉质检与用户全片终审，未发布。首轮v7文件仅作修订对照，以下v6及更早记录为历史。

**当前交付：地球online攻略首帧＋中英双语v6（2026-10-08，已完成）。** [观看/下载新版](renders/人生指南-地球online攻略-中英双语-v6.mp4)：59.5秒、1080×1920、30fps，约121.1MB。前0.5秒主标题改为“地球online攻略”，保留无本人画面的科技封面。正文、原声、双语字幕、画中画与隐私遮盖保留，未发布。

[封面PNG](renders/封面海报-地球online攻略-v6.png)｜[本轮验收](evidence/地球online攻略首帧验收-v6.md)｜[技术核验](qa/cover-v6/verification.json)。当前生成器`build-cover-v6.py`；以下为历史版本，用户在Studio手改后勿直接运行覆盖。

## 纯内容首帧v5历史记录

**历史交付：纯内容首帧＋中英双语v5（2026-10-08，已完成）。** [观看/下载新版](renders/人生指南-纯内容封面-中英双语-v5.mp4)：59.5秒、1080×1920、30fps，约83.2MB。前0.5秒封面已去掉本人，只保留大标题与放大的发光立体书；正文真人、双语字幕、画中画和结婚照遮盖保留。完整1785帧解码、海报15帧及音轨核验通过，没有发布。

[封面PNG](renders/封面海报-纯内容-v5.png)｜[本轮验收](evidence/纯内容首帧验收-v5.md)｜[原始核验](qa/cover-v5/verification.json)。当前可复建脚本`build-cover-v5.py`，用户在Studio手改后不要直接覆盖。下文均为历史，以本条为当前默认。

## 带真人封面v4历史记录

**历史交付：科技风首帧＋中英双语v4（2026-10-08，已完成）。** [观看/下载新版](renders/人生指南-科技封面-中英双语-v4.mp4)：59.5秒、1080×1920、30fps，约83.2MB。前0.5秒改为用户参照的蓝金科技风：发光立体书＋真人＋超大标题。正文、中英字幕、原声、画中画与结婚照遮盖保留。完整1785帧解码、首15帧海报及音轨核验通过，没有发布。

[封面PNG](renders/封面海报-科技风-v4.png)｜[制作验收](evidence/科技风首帧验收-v4.md)｜[生成提示/来源](evidence/cover-v4-generation.json)｜[双语SRT](data/中英双语字幕-v3.srt)。当前首帧生成器`build-cover-v4.py`；从保留v3备份恢复正文并替换封面，不要覆盖用户在Studio的手改。以下为历史交付，以此条为当前默认。

## 双语v3历史记录

**历史交付：中英双语＋0.5秒首帧海报v3（2026-10-08，已完成）。** [观看/下载成片](renders/人生指南-中英双语-首帧海报-v3.mp4)：59.5秒、1080×1920、30fps，83,071,706字节（约83.1MB）。中文字幕在上、英文在下；前15帧为静态封面，0.5秒接原片，原声和资料窗统一后移0.5秒。保留人像、画中画和已有结婚照遮盖，没有发布。

[独立封面PNG](renders/封面海报-v3.png)｜[双语SRT](data/中英双语字幕-v3.srt)｜[本轮验收](evidence/中英双语首帧海报验收.md)｜[原始技术核验](qa/bilingual-v3/final/final-verification.json)。当前生成器为`build-bilingual-v3.py`；它复用v2备份并重写HTML，用户在Studio手改后勿直接运行覆盖。`build-pip.py`会恢复v2，`build-composition.py`会恢复含未遮照片的v1，均不是当前生成入口。

## 画中画v2历史记录

**历史交付：画中画隐私修订v2（2026-10-08，已完成）。** [观看/下载新版](renders/人生指南-画中画-隐私修订-v2.mp4)：59秒、1080×1920、30fps，83,706,175字节（约83.7MB）。开头结婚照所在区域已在母版不透明遮盖；全程人像保留，真实资料以上方小窗穿插，眼睛/鼻嘴可见。原声和字幕保留。闪退后实核此前渲染已成功，直接完成成片核验，没有从头重做或重复渲染。

[新版封面](renders/封面-画中画-v2.jpg)｜[新版技术核验](qa/pip-v2/final-verification.json)｜[新版制作验收](evidence/画中画隐私修订验收.md)。原始母版及素材未改；下文v1为历史版本，它含未遮照片，只保留私有审稿，不作当前发布用片。

v2工程生成脚本为`build-pip.py`，引用隐私母版；`build-composition.py`是旧v1生成器，继续使用会恢复未遮照片与全屏资料板，不能用于当前版本。两者均会重写HTML，用户手改后先保留改动。当前工程文件记录总约1.26GiB，其中775MiB为可复用本项目渲染缓存；仍低于2GiB控制范围，留在移动硬盘，无本次待清理项。

## 首版v1历史记录

2026-10-08。**首版制作及内部技术核验完成，供用户审片。** [观看/下载成片](renders/人生指南-首条-v1.mp4)：59秒、1080×1920、30fps、H264/AAC，54,770,734字节（约54.8MB）。五段本人原声、真实指南截图、目录实际滚动、来源展开、字幕、关键词/重点框与资料板转场均进入最终文件。用户决定是否发布；没有发布、发送资料或操作社交平台。

[封面](renders/封面-首版.jpg)｜[可编辑预览](http://localhost:3027/#project/first-video-life-guide-20261008)｜[发布文字草稿](发布草稿.md)｜[领取资料说明](领取资料/先看这个.md)｜[制作验收](evidence/制作验收.md)。预览服务实核仅监听127.0.0.1:3027；本机可播放、编辑，服务关闭后链接失效。成片文件独立可用。

## 当前入口

- 制作范围与授权：[BRIEF.md](BRIEF.md)
- 视觉与声画顺序：[design.md](design.md)、[STORYBOARD.md](STORYBOARD.md)
- 工程：`index.html`，复用现有HyperFrames0.8.91，以原生WAAPI动效，不下载GSAP或安装依赖。
- 原声母版：[edit/master.mp4](edit/master.mp4)，59秒，1080×1920、30fps；[切点/验证](edit/README.md)。原片未改。
- 页面素材：`assets/capture/`。真实CUA手动浏览：GitHub README → 官方在线阅读页 → 第23章 → 实际成本/收益字段 → 展开来源；菜单目录有实际滚动，source录屏主要为来源展开，不称正文滑动。desktop skill录屏另保留实际正文滚动证据。
- [领取资料](领取资料/先看这个.md)：原作者PDF（2026-10-07冻结快照）＋查阅入口，保留原作来源和CC BY 4.0；没有擅自发给任何人。
- 检查原始输出和截图：`evidence/check-v*.json`、`snapshots/`；保留未经修改的CLI输出。工具0.8.91会在JSON前打印诊断行，解析版另存，不能把stdout第一行当JSON。
- 子agent只写`edit/`、`qa/`，root负责主工程与页面捕获、渲染及验收；研究Owner目录未修改，未恢复1000视频研究。

## 当前验收边界

最终MP4完整解码1770帧，无黑帧检测事件/解码或时间戳错误；五段原声相对母版偏移均0，排除音效窗后107个语音窗最小相关性0.998587，音轨非空且无削波样本，见[独立核验](qa/final-verification.json)。根Owner实际读取最终成片24个场景/转场采样图（两张联系图），目录内容区23→25秒像素变化与原录屏对应；这不是连续完整看听。工程v2 runtime/layout/motion/contrast均0error、对比度28/28通过；45个结构建议warning、8个转场/重叠瞬间info保留，不称零finding。

字幕34段采用现有ASR＋句间RMS校正，专名经资料核对；末尾“只是在”识别不可靠，显示字幕省略为“想要的朋友”，完整原声保留。人工逐字听音、语气/眼神和发布后的效果仍由实际审片/数据判断，不冒称已通过；它们不被包装成播放或咨询成效。

## 文件与资源

新建/截图/录屏、媒体派生、字体来源及sha记录在`evidence/asset-records.json`；原片剪接与子agent临时文件记录在`edit/`；PDF复制见`evidence/giveaway-record.json`；本次文件范围见`evidence/production-files.json`。工程约0.77GiB，包括可复用渲染缓存429MiB、assets141MiB、edit146MiB，低于2GiB控制范围；均在移动硬盘。系统盘约12GiB可用，渲染缓存已放本工程，不清理旧缓存/原素材/其他项目。两个本任务音轨草稿、中文路径编码错误造成的四个本轮空目录已按既有清理授权处理并有记录，其他证据/素材保留。领取包不包含本机字体或本人原视频。

第一次渲染在末尾音轨规范化失败，原媒体适配器缺总帧数；工程内`ffprobe-adapter.py`用既有AVFoundation及实际FFmpeg图片包计数/音轨样本补齐此JSON子集，不冒充官方ffprobe，不替换全局工具。第二次渲染成功：`evidence/render-v2.log`，screenshot capture、hardware GPU，1分55秒。原始失败日志仍保留。

重渲染复用已安装CLI，在本工程执行（会创建新版本，保留首版）：
```bash
HYPERFRAMES_FFPROBE_PATH="$PWD/ffprobe-adapter.py" HYPERFRAMES_EXTRACT_CACHE_DIR="$PWD/.render-cache" hyperframes render --quality delivery --crf 18 --workers 2 --no-best-effort --sdr --output renders/人生指南-修改版.mp4
```
不要为此安装或升级；用户实际编辑之后按修改范围重新检查。`build-composition.py`是初版生成脚本，重新运行会重写工程HTML；用户在Studio编辑后不要直接运行它覆盖手改。

直接用户本地制作授权优先于Skill的新增逐阶段审批，渲染在当前授权内执行。未授权安装、更新、付费或云端生成，因此使用已安装工具，不执行Skill的更新建议、公开反馈或外发。HyperFrames usage子命令不支持，使用量UNKNOWN；实际model/effort/速度值UNKNOWN。单子agent目标gpt-6.1-sol/medium，已记录读取ROUTING版本，未把自述当运行态证明。
