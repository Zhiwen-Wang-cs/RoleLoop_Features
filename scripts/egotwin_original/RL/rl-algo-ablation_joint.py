"""rl-algo-ablation_joint：fixed96 Joint 两列一张图——左列 RL 算法对比（MASC-v4 vs GRPO / RLOO / ReMax / REINFORCE++），
右列 MASC-v4 消融（完整版 vs 去 Oracle / 去角色信用 / 两者都去）；上行 Qwen3.8-27B，下行 Muse-Glimmer-30B。
run 组合与目录全部取自 /filesdir/data/zhiwen/消融平均表.md 的 <details> 记录（脚本直接解析该文件），
Joint = 各 run summary.json 的 evaluation_success_count/96；竖短线为单次 run，点为均值，横线为 ±1 SD（ddof=1），
浅蓝带为 MASC-v4 完整版均值 ±1 SD，标签括号内为与完整版的差。
输出：paper_pdf/RL/rl-algo-ablation_joint.pdf 与 preview_png/RL/rl-algo-ablation_joint.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/rl-algo-ablation_joint.py"
"""
import sys,re
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"frame"))
from _statistics import *
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
SRC=Path("/filesdir/data/zhiwen/消融平均表.md")
ALGO=[("MASC Full","MASC-v4"),("GRPO","GRPO"),("RLOO","RLOO"),("ReMax","ReMax"),("REINFORCE++","REINFORCE++")]
ABL=[("MASC Full","MASC-v4 (full)"),("MASC no-oracle","w/o Oracle"),("MASC no-role-credit","w/o Role credit"),("MASC double","w/o Oracle & Role credit")]
MODELS=[("Qwen","Qwen3.8-27B",(40,65)),("Muse","Muse-Glimmer-30B",(45,65))]

def run_dirs():
    """{'Qwen GRPO': [run 目录, ...], ...}，取自消融平均表各 <details>。"""
    text=SRC.read_text()
    return {name:[Path(d) for d in re.findall(r"^(/filesdir\S+/run-\d+)$",body,re.M)]
            for name,body in re.findall(r"<summary>((?:Qwen|Muse) [^：]+)：.*?</summary>(.*?)</details>",text,re.S)}

def runs():
    return {k:[read(d/"summary.json")["evaluation_success_count"]/len(TASKS)*100 for d in v] for k,v in run_dirs().items()}

def panel(ax,R,m,rows,title,xlim):
    """rows 第 0 行为 MASC Full（参考带）。"""
    V=[np.array(R[f"{m} {k}"]) for k,_ in rows];mu,sd=V[0].mean(),V[0].std(ddof=1)
    ax.axvspan(mu-sd,mu+sd,color="#dbe5f5",zorder=0);ax.axvline(mu,color=COLORS[2],ls=":",lw=.9,zorder=1)
    for i,x in enumerate(V):
        assert len(x)==3,(m,rows[i])
        c=COLORS[2] if i==0 else COLORS[0];xm,xs=x.mean(),x.std(ddof=1)
        ax.plot(x,np.full(3,i-.3),"|",ms=5,color=c,alpha=.75)
        ax.errorbar(xm,i,xerr=xs,fmt="o" if i==0 else "s",color=c,mec="white",mew=.6,ms=5,capsize=2,lw=1.2,zorder=3)
        r=xm+xs;r=mu+sd if i and mu-sd-1<r<mu+sd else r
        ax.text(r+.4,i,f"{xm:.1f}"+("" if i==0 else f" ({xm-mu:+.1f})".replace("-","−")),ha="left",va="center",fontsize=6.5,color="#333333",
                bbox=dict(boxstyle="square,pad=0.1",fc="white",ec="none",alpha=.85),zorder=4)
        print(f"{m:5s} {rows[i][1]:26s} runs={np.round(x,2).tolist()} Joint={xm:.2f} ± {xs:.2f}")
    style(ax,"x");ax.set_xlim(*xlim);ax.set_xticks(range((xlim[0]+4)//5*5,xlim[1]+1,5))
    ax.set_yticks(range(len(rows)),[l for _,l in rows]);ax.set_ylim(len(rows)-.4,-.7);ax.set_title(title,fontsize=8.5,pad=4)

def main():
    R=runs()
    fig,axs=plt.subplots(2,2,figsize=(6.875,3.9))
    for r,(m,name,xlim) in enumerate(MODELS):
        panel(axs[r,0],R,m,ALGO,f"({'ac'[r]}) RL algorithms · {name}",xlim)
        panel(axs[r,1],R,m,ABL,f"({'bd'[r]}) MASC-v4 ablations · {name}",xlim)
    for ax in axs[-1]: ax.set_xlabel("Joint success rate (%)")
    handles=[Line2D([],[],marker="|",ls="",color=COLORS[0],label="single run"),Line2D([],[],marker="s",ms=4.5,color=COLORS[0],label="mean ± 1 SD"),Patch(color="#dbe5f5",label="MASC-v4 (full) mean ± 1 SD")]
    fig.legend(handles=handles,loc="upper center",ncol=3,frameon=False,bbox_to_anchor=(.5,1.01))
    fig.tight_layout(rect=(0,0,1,.95),w_pad=1.2,h_pad=1.0);save(fig,"rl-algo-ablation_joint","RL")
if __name__=="__main__": main()
