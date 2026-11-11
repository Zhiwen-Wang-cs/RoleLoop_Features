"""rl-paired_win-loss：fixed96 逐题配对胜负，MASC-v4 vs 每个 RL 基线（左 Qwen3.8-27B，右 Muse-Glimmer-30B）。
赢 = MASC-v4 成功且基线失败的题数，输 = 基线成功且 MASC-v4 失败的题数；对 MASC 的 3 个 run × 基线的 3 个 run 共 9 种配对取平均，误差线为 9 种配对的 ±1 SD。
右侧蓝条为赢、左侧灰条为输，条旁标数值，最右列为 赢/输 比。
数据：/filesdir/data/zhiwen/消融平均表.md 各算法的 3 个 run 目录（复用 rl-algo-ablation_joint.run_dirs），逐题 result.json 的 evaluation.success（缺文件计失败）。
输出：paper_pdf/RL/rl-paired_win-loss.pdf 与 preview_png/RL/rl-paired_win-loss.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/rl-paired_win-loss.py"
"""
import sys,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location("ab",Path(__file__).with_name("rl-algo-ablation_joint.py"));ab=importlib.util.module_from_spec(s);s.loader.exec_module(ab)
np,plt,COLORS=ab.np,ab.plt,ab.COLORS
BASES=["GRPO","RLOO","ReMax","REINFORCE++"]
MODELS=[("Qwen","Qwen3.8-27B"),("Muse","Muse-Glimmer-30B")]
LOSS="#9a9b9a"

def succ(dirs):
    return np.array([[ab.read(p)["evaluation"]["success"] if (p:=d/sc/f"task_{i}/result.json").exists() else False for sc,i in ab.TASKS] for d in dirs],bool)

def main():
    D=ab.run_dirs()
    fig,axs=plt.subplots(1,2,figsize=(6.875,1.9),sharey=True)
    for ax,(m,title) in zip(axs,MODELS):
        M=succ(D[f"{m} MASC Full"]);y=np.arange(len(BASES))
        for r,b in enumerate(BASES):
            B=succ(D[f"{m} {b}"])
            w=np.array([(x&~z).sum() for x in M for z in B]);l=np.array([(z&~x).sum() for x in M for z in B])
            print(f"{title:17s} vs {b:12s} 赢={w.mean():.2f}±{w.std(ddof=1):.2f} 输={l.mean():.2f}±{l.std(ddof=1):.2f} 比={w.mean()/l.mean():.2f}")
            ax.barh(r,w.mean(),.6,xerr=w.std(ddof=1),color=COLORS[2],error_kw=dict(lw=.6,capsize=1.5,ecolor="#333333"),zorder=3)
            ax.barh(r,-l.mean(),.6,xerr=l.std(ddof=1),color=LOSS,error_kw=dict(lw=.6,capsize=1.5,ecolor="#333333"),zorder=3)
            ax.text(w.mean()+w.std(ddof=1)+.6,r,f"{w.mean():.1f}",va="center",ha="left",fontsize=6.5,color="#1a1a1a",fontweight="bold")
            ax.text(-l.mean()-l.std(ddof=1)-.6,r,f"{l.mean():.1f}",va="center",ha="right",fontsize=6.5,color="#52514e")
            ax.text(30,r,f"{w.mean()/l.mean():.1f}×",va="center",ha="right",fontsize=6.5,color=COLORS[2],fontweight="bold")
        ax.axvline(0,color="#52514e",lw=.7,zorder=4);ab.style(ax,"x");ax.set_xlim(-20,30.5);ax.set_xticks(range(-15,26,5),[str(abs(v)) for v in range(-15,26,5)])
        ax.set_yticks(y,[f"vs {b}" for b in BASES]);ax.set_ylim(len(BASES)-.5,-.5);ax.set_title(title,fontsize=8.5,pad=4)
        ax.set_xlabel("Tasks (of 96)")
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=COLORS[2],label="MASC-v4 solves, baseline fails"),Patch(color=LOSS,label="baseline solves, MASC-v4 fails")],
               loc="upper center",ncol=2,frameon=False,bbox_to_anchor=(.5,1.03),handlelength=1.2,columnspacing=2)
    fig.tight_layout(rect=(0,0,1,.87),w_pad=1.5);ab.save(fig,"rl-paired_win-loss","RL")
if __name__=="__main__": main()
