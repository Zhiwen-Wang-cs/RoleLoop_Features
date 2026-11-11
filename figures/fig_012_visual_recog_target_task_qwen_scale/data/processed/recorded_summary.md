以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### visual-recog_target-task_qwen-scale
来源：见 readme 同名节；统计与画图脚本 statistics_script/frame/visual-recog_target-task_qwen-scale.py。单元格为“百分比 (分子/分母)”。

| 模型 | 模式 | 目标识别率 | 整题视觉全对 |
|---|---|---|---|
| Qwen3.5-4B | Base | 13.55 (21/155) | 11.46 (11/96) |
| | Summary_v2 | 19.35 (30/155) | 14.58 (14/96) |
| | SAGE | 45.16 (70/155) | 30.21 (29/96) |
| Qwen3.5-9B | Base | 21.94 (34/155) | 16.67 (16/96) |
| | Summary_v2 | 19.35 (30/155) | 10.42 (10/96) |
| | SAGE | 44.52 (69/155) | 27.08 (26/96) |
| Qwen3.8-27B | Base | 16.77 (26/155) | 11.46 (11/96) |
| | Summary_v2 | 25.16 (39/155) | 17.71 (17/96) |
| | SAGE | 66.45 (103/155) | 55.21 (53/96) |

缺轨迹按未识别计：Qwen3.5-4B Summary_v2 缺 2 题，Qwen3.5-9B Summary_v2 缺 1 题，Qwen3.8-27B Summary_v2 缺 1 题。注：4B SAGE 采用独立 96 题复评 base-local96-online（未微调基线），官方 rescore_sage_results 复评 Joint 4/96 = 4.17、Tool 6.25、Result 9.38，与成绩表一致。
