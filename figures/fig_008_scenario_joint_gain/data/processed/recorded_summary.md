以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### scenario_joint-gain
来源：Base 为 baselines/Egolink2026/eval_result/<模型>/*_eval.json 的 joint_success；Summary_v2 为官方 evaluate_interaction.py --official96 重新评分（Qwen 缺 kitchen4/task_2 按失败计）；SAGE 为路径表结果的 evaluation.success。单元格为成功题数"Base / Summary_v2 / SAGE"；提升 = (SAGE − 基线)/n。；统计与画图脚本 statistics_script/frame/scenario_joint-gain.py

| 场景 | n | Muse | Qwen | GPT |
|---|---|---|---|---|
| kitchen4 | 18 | 3 / 4 / 6 | 2 / 6 / 7 | 7 / 9 / 11 |
| order2 | 20 | 5 / 5 / 8 | 2 / 5 / 11 | 4 / 10 / 11 |
| restaurant5 | 18 | 3 / 2 / 13 | 1 / 0 / 8 | 4 / 11 / 13 |
| retail6 | 20 | 3 / 5 / 10 | 1 / 5 / 8 | 6 / 13 / 14 |
| retail10 | 20 | 7 / 7 / 15 | 6 / 8 / 6 | 11 / 13 / 16 |
| All | 96 | 21 / 23 / 52 | 12 / 24 / 40 | 32 / 56 / 65 |
