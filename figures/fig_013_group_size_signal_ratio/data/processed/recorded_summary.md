以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### group-size_signal-ratio
来源：`/filesdir/data/zhiwen/EgoTwin/data/agent-training/results/egolink2026/masc-v4/` 下 muse-glimmer-30b-masc-v4-100-ctx131072-w48（104 组）与 qwen3.8-27b-masc-v4-100-ctx36864-w48（101 组）的 rollout_traces；oracle_min 规则见 `agent-training/algorithms/masc-v4/train.py:505`。；统计与画图脚本 statistics_script/RL/group-size_signal-ratio.py

| 模型 | k | 全对 | 全错 | GRPO | oracle_min=0 | oracle_min=1 |
|---|---|---|---|---|---|---|
| Muse | 2 | 0.614 | 0.244 | 0.143 | 0.386 | 1.000 |
| Muse | 3 | 0.572 | 0.214 | 0.214 | 0.428 | 1.000 |
| Muse | 4 | 0.548 | 0.202 | 0.250 | 0.452 | 1.000 |
| Qwen | 2 | 0.351 | 0.272 | 0.376 | 0.649 | 1.000 |
| Qwen | 3 | 0.238 | 0.198 | 0.564 | 0.762 | 1.000 |
| Qwen | 4 | 0.168 | 0.168 | 0.663 | 0.832 | 1.000 |
