以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### sage-role_token-share
来源：SAGE 结果 telemetry 的 token_usage（planner/executor/reporter/选帧+识别），不含 user 与 corrector。单元格为"占比 / 每题 token / 每题调用数 / 单次输入"。；统计与画图脚本 statistics_script/frame/sage-role_token-share.py

| 模型 | Planner | Executor | Reporter | Visual | 每题合计 |
|---|---|---|---|---|---|
| Muse | 30.7% / 95k / 13.6 / 6.2k | 36.1% / 112k / 23.1 / 4.6k | 11.3% / 35k / 5.2 / 6.2k | 21.9% / 68k / 3.8 / 17.9k | 310k |
| Qwen3.8 | 33.5% / 81k / 12.9 / 6.1k | 31.5% / 76k / 18.2 / 4.0k | 14.1% / 34k / 5.6 / 5.9k | 20.8% / 50k / 3.5 / 14.2k | 241k |
| GPT | 35.6% / 77k / 13.0 / 5.7k | 24.1% / 52k / 13.7 / 3.7k | 13.4% / 29k / 5.1 / 5.5k | 26.9% / 58k / 3.9 / 14.8k | 217k |
