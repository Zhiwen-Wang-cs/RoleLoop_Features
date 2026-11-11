以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### rl-passk_reliability
来源：消融平均表各算法的 3 个 run 目录（同 rl-algo-ablation_joint），逐题 `result.json` 的 `evaluation.success`（缺文件计失败）；pass^k = mean_task C(c,k)/C(3,k)，c 为该题 3 次 run 的成功次数。单位 %。；统计与画图脚本 statistics_script/RL/rl-passk_reliability.py

| 模型 | 方法 | pass^1 | pass^2 | pass^3 |
|---|---|---|---|---|
| Qwen3.8-27B | MASC-v4 | 53.12 | 38.89 | 31.25 |
| | GRPO | 46.53 | 28.82 | 18.75 |
| | RLOO | 46.18 | 29.51 | 21.88 |
| | ReMax | 47.57 | 33.68 | 27.08 |
| | REINFORCE++ | 45.14 | 31.25 | 25.00 |
| Muse-Glimmer-30B | MASC-v4 | 60.76 | 52.43 | 48.96 |
| | GRPO | 53.47 | 44.44 | 39.58 |
| | RLOO | 57.29 | 47.92 | 43.75 |
| | ReMax | 54.17 | 40.97 | 34.38 |
| | REINFORCE++ | 56.60 | 45.83 | 40.62 |
