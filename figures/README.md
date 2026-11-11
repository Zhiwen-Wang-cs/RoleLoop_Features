# 图件索引

每张图占一行，标题链接到对应目录的 `README.md`，预览链接到实际存在的 PNG。目录编号保持稳定；论文中的图号另行维护。

当前已登记一个数据交接包，图件尚未生成。`templates/figure/` 仍是空白模板，不是论文结果。

| 图件 ID | 标题 / 论文位置 | 状态 | 负责人 | 说明 | 预览 | 最近验证版本 |
| --- | --- | --- | --- | --- | --- | --- |
| `fig_001_interaction_efficiency` | [RoleLoop interaction and token costs / 实验部分，论文图号待定](fig_001_interaction_efficiency/README.md) | `data-ready` | 数据：论文作者；绘图负责人待分配 | 3 张原始汇总表、4 栏均值 CSV、口径与算术审计；不含绘图 | 待合作者生成 | [数据处理核验](fig_001_interaction_efficiency/docs/validation.json)，无独立复现 |

新增图件时先运行仓库根目录的 `python scripts/new_figure.py fig_001_topic`，再将实际信息填写到本表。尚无预览或验证记录时写“待生成”或“未验证”，不要链接到不存在的文件。

状态定义和数据规范见 [项目 README](../README.md)。

## EgoTwin 图件草稿

以下收录现有图片、汇总说明及原始脚本；完整精度输入和独立复现尚待完成。

| 图件 | 状态 | 预览 |
| --- | --- | --- |
| [ablation_joint_token](fig_002_ablation_joint_token/README.md) | `draft` | [PNG](fig_002_ablation_joint_token/images/ablation_joint_token.png) |
| [ecombench-visual-decision_target-task](fig_003_ecombench_visual_decision_target_task/README.md) | `draft` | [PNG](fig_003_ecombench_visual_decision_target_task/images/ecombench-visual-decision_target-task.png) |
| [gt-call-num_token-joint](fig_004_gt_call_num_token_joint/README.md) | `draft` | [PNG](fig_004_gt_call_num_token_joint/images/gt-call-num_token-joint.png) |
| [model-call-num_token](fig_005_model_call_num_token/README.md) | `draft` | [PNG](fig_005_model_call_num_token/images/model-call-num_token.png) |
| [sage-role_token-share](fig_006_sage_role_token_share/README.md) | `draft` | [PNG](fig_006_sage_role_token_share/images/sage-role_token-share.png) |
| [sage-visual_request-accuracy](fig_007_sage_visual_request_accuracy/README.md) | `draft` | [PNG](fig_007_sage_visual_request_accuracy/images/sage-visual_request-accuracy.png) |
| [scenario_joint-gain](fig_008_scenario_joint_gain/README.md) | `draft` | [PNG](fig_008_scenario_joint_gain/images/scenario_joint-gain.png) |
| [token_joint_pareto](fig_009_token_joint_pareto/README.md) | `draft` | [PNG](fig_009_token_joint_pareto/images/token_joint_pareto.png) |
| [turn_tool-progress](fig_010_turn_tool_progress/README.md) | `draft` | [PNG](fig_010_turn_tool_progress/images/turn_tool-progress.png) |
| [visual-recog_target-task](fig_011_visual_recog_target_task/README.md) | `draft` | [PNG](fig_011_visual_recog_target_task/images/visual-recog_target-task.png) |
| [visual-recog_target-task_qwen-scale](fig_012_visual_recog_target_task_qwen_scale/README.md) | `draft` | [PNG](fig_012_visual_recog_target_task_qwen_scale/images/visual-recog_target-task_qwen-scale.png) |
| [group-size_signal-ratio](fig_013_group_size_signal_ratio/README.md) | `draft` | [PNG](fig_013_group_size_signal_ratio/images/group-size_signal-ratio.png) |
| [masc-role_credit-share](fig_014_masc_role_credit_share/README.md) | `draft` | [PNG](fig_014_masc_role_credit_share/images/masc-role_credit-share.png) |
| [rl-algo-ablation_joint](fig_015_rl_algo_ablation_joint/README.md) | `draft` | [PNG](fig_015_rl_algo_ablation_joint/images/rl-algo-ablation_joint.png) |
| [rl-paired_win-loss](fig_016_rl_paired_win_loss/README.md) | `draft` | [PNG](fig_016_rl_paired_win_loss/images/rl-paired_win-loss.png) |
| [rl-passk_reliability](fig_017_rl_passk_reliability/README.md) | `draft` | [PNG](fig_017_rl_passk_reliability/images/rl-passk_reliability.png) |
| [train-step_reward-length_all](fig_018_train_step_reward_length_all/README.md) | `draft` | [PNG](fig_018_train_step_reward_length_all/images/train-step_reward-length_all.png) |
| [train-step_reward-length_overlay](fig_019_train_step_reward_length_overlay/README.md) | `draft` | [PNG](fig_019_train_step_reward_length_overlay/images/train-step_reward-length_overlay.png) |
| [train-step_stability](fig_020_train_step_stability/README.md) | `draft` | [PNG](fig_020_train_step_stability/images/train-step_stability.png) |
| [train-step_zero-signal-cum](fig_021_train_step_zero_signal_cum/README.md) | `draft` | [PNG](fig_021_train_step_zero_signal_cum/images/train-step_zero-signal-cum.png) |
