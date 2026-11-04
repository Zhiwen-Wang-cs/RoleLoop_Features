# fig_001_interaction_efficiency — RoleLoop interaction and token costs

| 项目 | 内容 |
| --- | --- |
| 图件 ID | `fig_001_interaction_efficiency` |
| 论文位置 | 实验部分的交互 / token 开销分析；论文图号尚未分配 |
| 状态 | `data-ready`：CSV 与处理流程已齐备，绘图交由合作者；不是 `reproduced` 或 `paper-ready` |
| 数据提供者 | RoleLoop 论文作者；原始汇总表由作者在对话中提供 |
| 绘图负责人 | 由论文作者安排，尚未指定 GitHub 用户名 |
| 验证 | 已验证数据处理与算术；未复跑实验，未生成新图 |

## 合作者从这里开始

1. 阅读 [绘图需求](docs/plot_spec.md) 和 [统计口径 / 未决问题](docs/provenance.md)。
2. 直接读取 [四个面板的长表 CSV](data/processed/)。基础单位为 tokens 或 calls/task；token 的 `k` 单位仅在绘图时除以 1000。
3. 如需重新计算，在仓库根目录运行：

```bash
python figures/fig_001_interaction_efficiency/code/prepare_data.py
python figures/fig_001_interaction_efficiency/code/prepare_data.py --check
```

无需第三方 Python 依赖。完整输入、环境和核验步骤见 [reproduction.md](docs/reproduction.md)。

## 数据入口

- [原始汇总 CSV](data/raw/) / [可核对的人工转录快照](docs/source_snapshot.json)
- [来源清单](data/sources.csv) / [字段字典](docs/data_dictionary.csv) / [数据使用说明](data/LICENSE.md)
- [聚合配置](config/aggregation.json) / [绘图交接配置](config/plot_handoff.json)
- [工具视图算术审计](data/processed/tool_view_arithmetic_audit.csv)
- [所有五个骨干的原始 token 与耗时记录](data/raw/egolink_costs.csv)
- [修改记录](docs/CHANGELOG.md)

## 四栏内容

| 面板 | 内容 | 处理后 CSV | 行数 |
| --- | --- | --- | --- |
| a | 四数据集：ReAct 单次请求 vs RoleLoop P+E 组合的工具描述 tokens | `panel_a_tool_schema.csv` | 8 |
| b | 四数据集：平均日志调用次数 / task，RoleLoop 仅计 P/E | `panel_b_calls_per_task.csv` | 8 |
| c | EgoLink2026：ReAct / Summary / RoleLoop 平均 tokens / task | `panel_c_tokens_per_task.csv` | 3 |
| d | 四数据集：RoleLoop 无视图 vs 有视图的每题工具描述开销估算，含 Reporter | `panel_d_tool_views.csv` | 8 |

四栏均值统一使用 Qwen3.8-27B、Muse-Glimmer-30B、GPT-5.6-sol。两个 Qwen3.5 小模型的记录完整保留在 raw 与 companion CSV，但不进入这组三骨干均值。

## 图件与证据边界

遵照作者最新要求，本次不提供绘图程序、不生成或上传图件，也不把此前未获认可的图稿作为成品。预览待合作者生成；[图片生成清单](images/manifest.csv) 仅有表头。

原始日志、task IDs、run IDs、seeds、准确代码版本与任务级样本均未提供。`data-ready` 仅表示本次汇总数据交接就绪；实验复现、误差条、跨方法任务匹配与最终论文结论均未验收。
