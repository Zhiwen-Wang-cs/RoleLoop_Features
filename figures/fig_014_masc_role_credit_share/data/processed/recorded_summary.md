以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### masc-role_credit-share
来源：同 train-step_reward-length 的 MASC-v4 训练日志，Qwen 为 qwen3.8-27b-masc-v4-100-ctx36864-w48、Muse 为 muse-glimmer-30b-masc-v4-100-ctx131072-w48；字段 `masc_v4/share_<角色>`（定义见 `agent-training/algorithms/masc-v4/train.py:608`）与 `masc_v4/<角色>_rows`；只统计四个角色 share 之和 > 0.99 的步。均值为步间平均，括号内为 95% 置信区间半宽。；统计与画图脚本 statistics_script/RL/masc-role_credit-share.py

| 模型（有信号步数） | 角色 | 信用占比（%） | 调用占比（%） | 倍数 |
|---|---|---|---|---|
| Qwen3.8-27B（93） | Planner | 53.44（±4.36） | 31.63（±0.66） | 1.69 |
| | Executor | 30.26（±4.38） | 42.53（±1.08） | 0.71 |
| | Reporter | 14.04（±2.75） | 13.71（±0.56） | 1.02 |
| Muse-Glimmer-30B（56） | Planner | 55.98（±7.89） | 30.32（±1.59） | 1.85 |
| | Executor | 31.67（±8.61） | 49.15（±1.98） | 0.64 |
| | Reporter | 8.17（±2.35） | 10.61（±0.58） | 0.77 |
