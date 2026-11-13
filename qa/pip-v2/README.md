# 画中画隐私修订v2最终技术核验

2026-10-08，结果PASS（技术层）。目标gpt-6.1-sol/medium，实际model/effort/速度UNKNOWN。仅写本目录，未安装、上传、发布、删除、修改工程/原片/母版。

成片83706175字节，59秒、1080×1920、30fps、H264 High/AAC LC 48000Hz双声道。FFmpeg实际完整解码退出0、1770帧，进度progress=end；无解码/时间戳错误、无blackdetect事件。规格来源为AVFoundation元数据及实际FFmpeg输入流日志。

解码音轨非空；48kHz原生采样峰值0.559322（-5.047dBFS），≥0.99995和>1样本均0。5段各2秒与master在±200ms搜索中最佳偏移均0；排除4个短音效窗及低于-45dB静音的107个0.5秒语音窗，最小相关性0.998587、无低于0.97窗，支持同源原声且无可检测语音缺口。master为单声道、成片为双声道，核验使用16kHz单声道混合，因此增益约1.405—1.414；不把混合后的音量比例解释为音频逐样本相同。此项没有重读五个原片。

前525帧顶部小ROI x450/y8/w230/h24全部检查：与深墨绿[23,37,30]最大偏差5级，逐帧空间通道范围0，初设8级检查通过，无失败帧。它只支持顶部有隐私背景、未误用未遮母版的辅助证据；完整照片区域依据已有隐私母版全ROI核验以及root最终画面审查，不宣称人像识别或完整连续看听。

当前源master SHA256与隐私预处理记录一致；master-redacted SHA256也一致。原母版未改。最终SHA256见final-verification.json。

evidence/check-pip-final-report.json原始报告读取：lint/runtime/layout/motion/contrast均0error；lint仍45warning（结构建议），本报告info均0，contrast 29/29。保留warning与error区别，不以退出0冒称零finding。旧v1的info数不迁移为本版本事实。

限制：不证明模拟true-peak；不替代人工逐字听音、语气/眼神或完整连续动态审片；root负责画中画视觉验收与交付，用户决定发布。

具体新增文件及用途见manifest.json；日志/脚本/JSON均保留以供复核，无抽取原照片或新增临时媒体。可使用已有Python运行verify_final.py重新生成机器核验，不调用会写其他目录的ffprobe-adapter。
