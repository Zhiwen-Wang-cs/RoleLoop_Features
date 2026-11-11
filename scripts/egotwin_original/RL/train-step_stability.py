"""train-step_stability：Qwen3.8-27B 上 MASC-v4 与四个 RL 基线的训练稳定性与开销（三联图，画法同 train-step_reward-length_overlay）。
(a) Gradient Norm：actor/grad_norm（裁剪前的策略梯度范数）；(b) Policy Entropy：actor/entropy（策略输出 token 的平均熵）；(a)(b) 不含 ReMax（其损失按序列求和，量纲不同）；
(c) Rollout Time per Step（s）：timing_s/gen（每步采样轨迹用时）。
粗线为 EMA（0.95），MASC-v4 的淡色带为 ±10 步滚动 SD 的一半；每种算法只训练一次。
数据：与 train-step_reward-length.py 相同的训练日志（复用其 RUNS / load / overlay）。
输出：paper_pdf/RL/train-step_stability.pdf 与 preview_png/RL/train-step_stability.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/train-step_stability.py"
"""
import sys,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("ts",Path(__file__).with_name("train-step_reward-length.py"));ts=importlib.util.module_from_spec(spec);spec.loader.exec_module(ts)
np=ts.np
# ReMax 的 actor 损失按序列求和聚合（日志 entropy≈60、grad_norm≈10^3），与其它算法的按 token 平均不在同一量纲，(a)(b) 不画 ReMax
PANELS=[("actor/grad_norm",1,"Gradient Norm",None,{"ReMax"}),("actor/entropy",1,"Policy Entropy",None,{"ReMax"}),
        ("timing_s/gen",1,"Rollout Time per Step (s)",None)]
# 未画 num_steps/mean（每条轨迹调用次数）：MASC-v4 全程均值 44.9 高于基线 39–41，不体现优势

if __name__=="__main__":
    V={n:ts.load(n,r,PANELS) for n,r in ts.RUNS.items()}
    for j,(k,_,t,*_) in enumerate(PANELS):
        print(f"{t:26s}","  ".join(f"{n}: 全程={V[n][:,j].mean():.3f} 后20步={V[n][-20:,j].mean():.3f}" for n in V))
    ts.overlay(V,PANELS,"train-step_stability")
