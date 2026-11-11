以下为原始说明中的汇总表，数值可能已四舍五入；并非完整绘图输入。

### visual-recog_target-task
来源：同 readme 路径表的 fixed96 轨迹 + Ours/egolink_sage-ablation/visual-GT.jsonl；统计与画图脚本 statistics_script/frame/visual-recog_target-task.py，枚举审计 statistics_script/frame/visual-recog_target-task_audit.py。单元格为“百分比 (分子/分母)”；“剔除枚举”为泄露前查过但因枚举被剔除的目标数。

| 模型 | 模式 | Joint | 目标识别率 | 整题视觉全对 | 剔除枚举 |
|---|---|---|---|---|---|
| Muse-Glimmer-30B | Base | 21.88 | 40.00 (62/155) | 27.08 (26/96) | 33 |
| | Summary_v2 | 23.96 | 27.74 (43/155) | 18.75 (18/96) | 40 |
| | SAGE | 54.17 | 72.26 (112/155) | 61.46 (59/96) | – |
| Qwen3.8-27B | Base | 12.50 | 16.77 (26/155) | 11.46 (11/96) | 16 |
| | Summary_v2 | 25.00 | 25.16 (39/155) | 17.71 (17/96) | 26 |
| | SAGE | 41.67 | 66.45 (103/155) | 55.21 (53/96) | – |
| GPT-5.6-sol | Base | 33.33 | 30.32 (47/155) | 15.62 (15/96) | 16 |
| | Summary_v2 | 58.33 | 43.23 (67/155) | 29.17 (28/96) | 22 |
| | SAGE | 67.71 | 76.13 (118/155) | 65.62 (63/96) | – |

口径：
- 查询：单实体查询参数（product_name/dish_name/recipe_name/ingredient_name）中的名字，排除增删改与计算类工具。名字只忽略大小写与标点后精确匹配。
- 泄露：名字出现在用户消息或筛选类工具结果中；类别清单类工具（find_products_by_category、find_dishes_by_category、list_all_dishes、get_all_recipe_names、get_all_ingredient_names、get_ingredients_by_category）结果不算泄露。
- 目标识别率：SAGE 为 observe_visual 在泄露前返回了标准名；Base/Summary_v2 为泄露前用标准名查询，且命中所在轮（按用户消息分轮）同一工具未查过其他候选名（候选不含已泄露的名字和本题其他视觉目标的标准名）。目标有多个标准名时须全部满足。
- 整题视觉全对：该题所有视觉目标都识别成功。
- Qwen Summary_v2 缺 1 题轨迹，按未识别计。
