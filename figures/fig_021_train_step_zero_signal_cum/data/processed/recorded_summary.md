以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### train-step_zero-signal-cum
来源：`/filesdir/data/zhiwen/EgoTwin/data/agent-training/logs/egolink2026/masc-v4/<同上两个 run>/` 下 `wandb/metrics-*.jsonl` 与 `recovery_driver/wandb/wandb/metrics-*.jsonl`（断点续训：Qwen 88–100 步、Muse 63–100 步在 recovery_driver 下），合并后 1–100 步无缺无重。判定：GRPO = `masc_v4/reward ∈ {0,1}`；oracle_min=0 = `masc_v4/gain_mean == 0`；oracle_min=1 = gain_mean==0 且 oracle_rows==0（每步 oracle_rows ≥ 13，故恒为 0）。；统计与画图脚本 statistics_script/RL/train-step_zero-signal-cum.py

| 训练步 | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| Muse GRPO | 6 | 12 | 20 | 28 | 34 | 43 | 51 | 57 | 66 | 76 |
| Muse oracle_min=0 | 5 | 11 | 18 | 24 | 29 | 34 | 40 | 44 | 48 | 56 |
| Qwen GRPO | 1 | 8 | 11 | 13 | 17 | 23 | 25 | 29 | 31 | 34 |
| Qwen oracle_min=0 | 0 | 3 | 5 | 6 | 8 | 11 | 11 | 13 | 15 | 17 |
