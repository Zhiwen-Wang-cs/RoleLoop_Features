以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### train-step_reward-length（_all / _overlay）
来源：训练日志（非 fixed96 评测），前缀 `/filesdir/data/zhiwen/EgoTwin/data/agent-training/logs/egolink2026/`：MASC-v4 为 `masc-v4/qwen3.8-27b-masc-v4-100-ctx36864-w48/wandb/metrics-*.jsonl` + `recovery_driver/wandb/wandb/metrics-*.jsonl`（续训）；GRPO / RLOO / ReMax / REINFORCE++ 为 `grpo/qwen3.8-27b-grpo`、`rloo/qwen3.8-27b-rloo`、`remax/qwen3.8-27b-remax`、`reinforce_plus_plus/qwen3.8-27b-reinforce-plus-plus` 下的 `training.log`；均 1–100 步无缺。字段：Task Reward = `critic/score/trajectory/mean`×100；Trajectory Length = `response_length/trajectory/mean`；Tokens per Call = `response_length/mean`（定义见 `agent-training/agent-r1/agent_r1/trainer/ppo/metric_utils.py`）。表中为 EMA(0.95) 平滑后第 81–100 步的平均；“领先步数”为 100 步中 MASC-v4 平滑值更优（奖励更高 / 长度更短）的步数。；统计与画图脚本 statistics_script/RL/train-step_reward-length.py

| 对比 | Task Reward（%，MASC / 基线） | Trajectory Length（k，MASC / 基线） | Tokens per Call（MASC / 基线） |
|---|---|---|---|
| vs GRPO | 55.27 / 49.08（领先 73/100 步） | 6.64 / 7.70（更短 40/100 步） | 144.92 / 176.89（更短 83/100 步） |
| vs RLOO | 55.27 / 55.64（39/100） | 6.64 / 9.69（52/100） | 144.92 / 208.14（88/100） |
| vs ReMax | 55.27 / 49.92（39/100） | 6.64 / 8.15（63/100） | 144.92 / 202.27（89/100） |
| vs REINFORCE++ | 55.27 / 55.33（24/100） | 6.64 / 8.29（58/100） | 144.92 / 187.68（85/100） |

对照：fixed96 评测中每题平均输出 token 为 MASC-v4 run-0 5,899、GRPO run-0 5,831（输入约 25–28 万，框架图里的“每题 token”是输入+输出）。
