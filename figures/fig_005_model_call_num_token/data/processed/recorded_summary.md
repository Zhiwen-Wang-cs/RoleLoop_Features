以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### model-call-num_token
来源：96 题结果文件中的逐次调用 token 记录（telemetry 的 token_usage）。决策调用口径：Base/Summary_v2 为 role=service（不含 summarizer 摘要调用），SAGE 为 planner+executor+reporter（不含 corrector 与视觉选帧/识别）。Qwen SAGE 合并 egolink_sage-ablation/results/qwen3.8-27b/full/run-1~3（run-0 无逐次记录）。单位 k（保留两位小数），括号为样本数 n（仅列 n<100 的点）。；统计与画图脚本 statistics_script/frame/model-call-num_token.py

| 方法 | 1 | 2–5 | 6–10 | 11–20 | 21–30 | 31–50 | 51–100 | 101+ |
|---|---|---|---|---|---|---|---|---|
| Muse Base | 20.92 (96) | 21.37 | 22.82 | 23.46 | 24.49 (94) | 25.91 (32) | – | – |
| Muse Summary_v2 | 20.93 (96) | 21.30 | 22.29 | 21.93 | 20.12 | 26.04 (79) | 27.64 | 38.43 (70) |
| Muse SAGE | 4.52 (96) | 3.52 | 4.02 | 4.80 | 5.33 | 6.16 | 7.64 | 9.18 (36) |
| Qwen3.8 Base * | 19.12 (96) | 19.81 | 21.14 | 21.26 | 16.34 (2) | – | – | – |
| Qwen3.8 Summary_v2 | 18.90 (95) | 19.23 | 19.74 | 18.75 | 19.62 | 18.36 | 21.75 (50) | – |
| Qwen3.8 SAGE | 4.54 | 3.45 | 4.05 | 5.22 | 5.45 | 5.41 | 6.65 | 9.29 |
| GPT Base * | 18.87 (96) | 19.66 | 21.42 | 22.96 | 16.61 (11) | – | – | – |
| GPT Summary_v2 | 20.07 (96) | 14.46 | 17.20 | 16.87 | 16.94 (75) | – | – | – |
| GPT SAGE | 4.12 (96) | 3.14 | 3.83 | 4.97 | 4.86 | 5.28 | 8.83 (86) | 19.71 (34) |

* 交互记录反推（Qwen、GPT 的 Base 无逐次记录）：Base 为单智能体，第 k 次调用输入 = C + H_k；H_k 为前 k−1 次调用新增的消息（工具调用 JSON、`Tool execution result: …`、上一轮回复与本轮用户消息）的 token 累计（Qwen 用 Qwen3.8-27B 分词器，GPT 用 o200k_base），C 由每题记录的总输入反解：C = (input_tokens − ΣH_k)/调用数。在有真值的 Muse Base 上验证：96 题调用数全部对上，逐次相对误差中位 0.05%、P90 0.38%、最大 10.7%（换 o200k 分词器结果相同）。

每题决策调用数（均值/中位/最大）：Muse Base 18.0/17/45；Muse Summary_v2 22.5/18.5/167（3 题超过 50 次）；Qwen Summary_v2 18.7/16/80；GPT Summary_v2 17.9/18/29。Muse Summary_v2 每题摘要调用 4.4 次、约 12k token。
