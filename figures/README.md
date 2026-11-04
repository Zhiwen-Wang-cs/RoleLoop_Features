# 图件索引

每张图占一行，标题链接到对应目录的 `README.md`，预览链接到实际存在的 PNG。目录编号保持稳定；论文中的图号另行维护。

当前已登记一个数据交接包，图件尚未生成。`templates/figure/` 仍是空白模板，不是论文结果。

| 图件 ID | 标题 / 论文位置 | 状态 | 负责人 | 说明 | 预览 | 最近验证版本 |
| --- | --- | --- | --- | --- | --- | --- |
| `fig_001_interaction_efficiency` | [RoleLoop interaction and token costs / 实验部分，论文图号待定](fig_001_interaction_efficiency/README.md) | `data-ready` | 数据：论文作者；绘图负责人待分配 | 3 张原始汇总表、4 栏均值 CSV、口径与算术审计；不含绘图 | 待合作者生成 | [数据处理核验](fig_001_interaction_efficiency/docs/validation.json)，无独立复现 |

新增图件时先运行仓库根目录的 `python scripts/new_figure.py fig_001_topic`，再将实际信息填写到本表。尚无预览或验证记录时写“待生成”或“未验证”，不要链接到不存在的文件。

状态定义和数据规范见 [项目 README](../README.md)。
