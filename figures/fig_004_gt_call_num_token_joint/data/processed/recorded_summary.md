以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### gt-call-num_token-joint（三模型合并）
来源：Base `/filesdir/data/zhiwen/EgoTwin/data/baselines/Egolink2026/results/`；SAGE `/filesdir/data/zhiwen/EgoTwin/data/Ours/egolink_sage/results/`；统一用 `Ours/egolink_sage/evaluation/evaluator.py` 在固定 96 题上重新评分。成功率 / 每题 token(k)，三档为 GT 工具调用数 1–4 / 5–7 / 8+：；统计与画图脚本 statistics_script/frame/gt-call-num_token-joint.py

| 模型 | 方法 | 1–4 | 5–7 | 8+ |
|---|---|---|---|---|
| Muse-Glimmer-30B (n=38/32/26) | Base | 0.263 / 333 | 0.219 / 384 | 0.154 / 570 |
| | Summary_v2 | 0.237 / 522 | 0.250 / 520 | 0.231 / 543 |
| | SAGE | 0.658 / 302 | 0.531 / 316 | 0.385 / 316 |
| Qwen3.8-27B (n=38/32/26) | Base | 0.132 / 206 | 0.156 / 263 | 0.077 / 317 |
| | Summary_v2 | 0.289 / 363 | 0.219 / 330 | 0.231 / 424† |
| | SAGE | 0.368 / 235 | 0.438 / 235 | 0.462 / 211 |
| GPT-5.6-sol (n=38/32/26) | Base | 0.474 / 208 | 0.281 / 289 | 0.192 / 401 |
| | Summary_v2 | 0.632 / 227 | 0.594 / 288 | 0.500 / 422 |
| | SAGE | 0.789 / 178 | 0.688 / 191 | 0.500 / 307 |

† Qwen Summary_v2 缺 kitchen4/task_2（无结果文件，8+ 档）：成功率按失败计入（6/26，与论文表 25.00% 一致），token 按其余 25 题平均。
全部 96 题汇总与论文表一致：Qwen Base/Summary/SAGE = 12/24/40，GPT = 32/56/65，Muse = 21/23/52。
