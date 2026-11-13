# 地球online攻略首帧v6验收

2026-10-08，root完成本地标题修改与导出，当前默认v6，未发布。

前0.5秒主标题“人生说明书”已换为“地球online攻略”（online小写），蓝金画风、无本人画面的封面、正文和双语字幕保持。正文HTML排除封面后与v5完全相同，见`cover-v6-change.json`。当前生成器`build-cover-v6.py`；用户手改后勿覆盖。

新版视频`renders/人生指南-地球online攻略-中英双语-v6.mp4`，121,101,021字节，SHA256 `ed62dd8f8883ea8e5c886ea8b4e51638cef218c7335401b993e888b1bdd5376c`。59.5秒、1080×1920、30fps、1785帧、H264/AAC；独立封面`renders/封面海报-地球online攻略-v6.png`。

工程check的lint/runtime/layout/motion/contrast均0error，46结构warning保留；原始与解析结果在evidence。封面由工程snapshot生成，复用v5成片，使用现有FFmpeg overlay enable=lt(t,0.5)替换首帧区间，VideoToolbox以16M重新编码画面，AAC直接复制；原视频保留，不宣称正文像素逐字节不变。导出日志`export-cover-v6.log`末尾1785帧，退出0。

`qa/cover-v6/verification.json`及decode原始日志：完整解码1785帧、progress=end、退出0，无错误或黑帧事件。实际前15帧稳定最大平均差1.35935/255≤3，0.5秒切回正文；音轨解码float样本与v5完全相同，相关性1.0，无削波。

root实际查看最终MP4第14帧新标题与16.5秒正文/双语字幕，确认标题正确和PIP保留；这是技术解码和静态画面验收，未冒称连续完整动态看听。本轮未生成新图、安装、升级、上传、外发、清理原片或修改其他项目。工程文件范围在production-files.json。
