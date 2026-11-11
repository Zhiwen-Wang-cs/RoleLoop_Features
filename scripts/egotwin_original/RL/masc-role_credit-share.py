"""masc-role_credit-share：MASC-v4 训练中信用（|advantage| 总量）分到各角色的比例（仿“信用落在回复哪一部分”分区柱状图）。
(a)(b) Qwen3.8-27B / Muse-Glimmer-30B：彩色柱 = masc_v4/share_<角色>（该角色行 |advantage| 之和 / 全部 |advantage|，见 agent-training/algorithms/masc-v4/train.py），
灰色柱 = 该角色调用行数占比（masc_v4/<角色>_rows / 总行数），即“每次调用分到同样多信用”的参照；柱上标注 信用占比/调用占比 的倍数。
误差线为有学习信号训练步上均值的 95% 置信区间（学生信用全为 0 的步剔除）。只展示 Planner/Executor/Reporter，占比分母含 Corrector。
注意：日志没有各角色 token 数，无法给出“按 token 均分”（GRPO）的参照，灰色是按调用次数的参照。
输出：paper_pdf/RL/masc-role_credit-share.pdf 与 preview_png/RL/masc-role_credit-share.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/masc-role_credit-share.py"
"""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"frame"))
from _statistics import *
LOG=DATA/"agent-training/logs/egolink2026/masc-v4"
RUNS={"Qwen3.8-27B":"qwen3.8-27b-masc-v4-100-ctx36864-w48","Muse-Glimmer-30B":"muse-glimmer-30b-masc-v4-100-ctx131072-w48"}
ALL=[("Planner","planner","planner"),("Executor","executor","executor"),("Reporter","reporter","reporter"),("Corrector","corrector","ego_corrector")]
ROLES=ALL[:3]  # Corrector 不展示；信号筛选与占比分母仍用全部角色

def load(run):
    steps={}
    for p in sorted((LOG/run).glob("wandb/metrics-*.jsonl"))+sorted((LOG/run).glob("recovery_driver/wandb/wandb/metrics-*.jsonl")):
        for line in p.read_text().splitlines():
            d=json.loads(line)
            if 1<=d["step"]<=100: steps[d["step"]]=d["metrics"]
    assert sorted(steps)==list(range(1,101)),(run,len(steps))
    return [steps[s] for s in range(1,101)]

def main():
    D={m:load(r) for m,r in RUNS.items()}
    fig,axs=plt.subplots(1,2,figsize=(6.875,1.75),sharey=True)
    y=np.arange(len(ROLES));h=.36
    for ax,(m,rows) in zip(axs,D.items()):
        # 学生信用全为 0 的步（无学习信号）各 share 记为 0，剔除，只统计有信号的步
        rows=[d for d in rows if sum(d[f"masc_v4/share_{k}"] for _,k,_ in ALL)>.99];print(m,"有信号步数=",len(rows))
        credit=100*np.array([[d[f"masc_v4/share_{k}"] for _,k,_ in ROLES] for d in rows])
        cnt=np.array([[d.get(f"masc_v4/{r}_rows",0) for _,_,r in ALL] for d in rows]);calls=(100*cnt/cnt.sum(1,keepdims=True))[:,:len(ROLES)]
        ci=lambda a:1.96*a.std(0,ddof=1)/np.sqrt(len(a))  # 步间均值的 95% 置信区间
        c,cs,u,us=credit.mean(0),ci(credit),calls.mean(0),ci(calls)
        ax.barh(y-h/2,u,h,xerr=us,color="#dcdddc",label="share of calls",error_kw=dict(lw=.6,capsize=1.2,ecolor="#8b8c8b"),zorder=3)
        ax.barh(y+h/2,c,h,xerr=cs,color=COLORS[2],label="share of credit",error_kw=dict(lw=.6,capsize=1.2,ecolor="#333333"),zorder=3)
        for i in range(len(ROLES)):
            ax.text(c[i]+cs[i]+1.5,y[i]+h/2,f"{c[i]/u[i]:.1f}×",va="center",fontsize=6.5,color="#333333")
            print(f"{m:17s} {ROLES[i][0]:9s} 信用={c[i]:.2f}% (95%CI ±{cs[i]:.2f})  调用={u[i]:.2f}% (±{us[i]:.2f})  倍数={c[i]/u[i]:.2f}")
        ax.set_yticks(y,[r for r,_,_ in ROLES]);ax.set_ylim(len(ROLES)-.4,-.6);ax.set_xlim(0,70);style(ax,"x")
        ax.set_xlabel("Share (%)");ax.set_title(f"({'ab'[list(D).index(m)]}) {m}",fontsize=8.5,pad=4)
    legend(fig,axs[0],2);fig.tight_layout(rect=(0,0,1,.86),w_pad=1.2)
    save(fig,"masc-role_credit-share","RL")
if __name__=="__main__": main()
