以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### train-step_stability
来源：同 train-step_reward-length 的 Qwen3.8-27B 训练日志；字段 `actor/grad_norm`、`actor/entropy`、`timing_s/gen`。表中为第 100 步 EMA(0.95) 值 / 后 20 步原始均值。ReMax 的 grad_norm、entropy 量纲不同（损失按序列求和），只列不比。；统计与画图脚本 statistics_script/RL/train-step_stability.py

| 算法 | Gradient Norm | Policy Entropy | Rollout Time per Step (s) |
|---|---|---|---|
| MASC-v4 | 0.128 / 0.120 | 0.138 / 0.130 | 357.1 / 323.8 |
| GRPO | 0.453 / 0.435 | 0.228 / 0.229 | 418.4 / 389.0 |
| RLOO | 0.275 / 0.311 | 0.228 / 0.229 | 534.5 / 544.0 |
| ReMax | （900.2 / 628.6，不可比） | （60.6 / 58.6，不可比） | 377.2 / 386.1 |
| REINFORCE++ | 0.944 / 0.913 | 0.218 / 0.211 | 412.2 / 410.5 |

未画：`num_steps/mean`（每条轨迹调用次数）全程均值 MASC-v4 44.87、GRPO 40.47、RLOO 40.38、ReMax 39.23、REINFORCE++ 41.36。
