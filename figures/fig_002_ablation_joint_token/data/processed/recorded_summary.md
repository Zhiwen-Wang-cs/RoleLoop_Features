以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### ablation_joint_token
来源：Ours/egolink_sage-ablation/results/qwen3.8-27b/<目录>/<run>/summary.json（Joint = evaluation_success_count/96，含协议失败判负）与各题 result.json 的 run.token_usage（不含 user_simulator）。；统计与画图脚本 statistics_script/frame/ablation_joint_token.py

| 变体 | 目录 | 运行 | Joint（%） | 均值 ± SD | token/题（k） | 均值 |
|---|---|---|---|---|---|---|
| SAGE (full) | full | run-0, run-2, run-3 | 41.67, 44.79, 43.75 | 43.40 ± 1.59 | 228.52, 250.96, 253.57 | 244.35 |
| w/o Visual decoupling | no_visual_decoupling-v5 | run-3, run-5, run-6 | 39.58, 33.33, 39.58 | 37.50 ± 3.61 | 176.87, 173.71, 174.87 | 175.15 |
| w/o Reporter | no_reporter | run-0, run-1, run-3 | 32.29, 37.50, 31.25 | 33.68 ± 3.35 | 202.95, 195.01, 204.24 | 200.74 |
| ReAct (no Planner/Executor) | react | run-0, run-2, run-3 | 34.38, 33.33, 30.21 | 32.64 ± 2.17 | 689.95, 762.71, 700.27 | 717.64 |

run 组合与 /filesdir/data/zhiwen/消融平均表.md「Qwen3.8-27B：SAGE框架消融」一致。no_visual_decoupling-v5 三次分别有 4/3/2 题视觉输出格式失败（仅 error.json）：Joint 按失败计（分母 96），token 只对有 result.json 的 92/93/94 题平均。
