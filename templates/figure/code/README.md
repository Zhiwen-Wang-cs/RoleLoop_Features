# 数据处理与绘图代码

根据实际流程添加脚本，例如：

- `extract_data.py`：从原始结果提取 CSV；输入来源和提取规则见 `../docs/provenance.md`。
- `prepare_data.py`：读取 `../data/raw/`，生成 `../data/processed/`。
- `plot.py`：读取 CSV 和 `../config/`，导出 `../images/` 中的图件。

这些名称是约定示例，模板尚未提供上述脚本。可以合并不必要的步骤或使用其他语言，但要提供可从头执行的入口。路径基于仓库或本图目录解析，配置与实验数值分离，记录每条命令的工作目录。
