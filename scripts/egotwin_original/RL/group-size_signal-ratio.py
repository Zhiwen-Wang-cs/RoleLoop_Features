"""group-size_signal-ratio：从训练 rollout 抽取全部 k 元子集并统计有学习信号的比例。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/RL/group-size_signal-ratio.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/RL/group-size_signal-ratio.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/group-size_signal-ratio.py"
"""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"frame"))
from _statistics import *
RUNS=["muse-glimmer-30b-masc-v4-100-ctx131072-w48","qwen3.8-27b-masc-v4-100-ctx36864-w48"]
LABELS=["GRPO","MASC-v4 (oracle_min=0)","MASC-v4 (oracle_min=1)"]
C=["#666666","#5a82c4","#1f4e9c"]
import gzip
from itertools import combinations
from collections import defaultdict
from matplotlib.patches import Patch

def main():
    values=[]
    for run in RUNS:
        groups=defaultdict(list)
        root=DATA/"agent-training/results/egolink2026/masc-v4"/run/"rollout_traces"
        for p in sorted(root.glob("*.json.gz")):
            with gzip.open(p,"rt") as f:d=json.load(f)
            if d["trajectory_kind"]=="sampled":groups[d["task_uid"]].append(float(d["reward"]))
        incomplete = {k:len(g) for k,g in groups.items() if len(g)!=4}
        print("Excluded incomplete sampled groups:", incomplete, flush=True)
        groups = {k:g for k,g in groups.items() if len(g)==4}
        print(run,"groups=",len(groups));v=[]
        for k in (2,3,4):
            subsets=[c for g in groups.values() for c in combinations(g,k)]
            n=len(subsets);all_ok=sum(all(x==1 for x in s) for s in subsets);all_bad=sum(all(x==0 for x in s) for s in subsets)
            mixed=n-all_ok-all_bad;v.append([mixed/n,(n-all_ok)/n,1.])
            print(f"k={k}: all-success={all_ok}/{n}={all_ok/n:.3f}; all-fail={all_bad}/{n}={all_bad/n:.3f}; GRPO={mixed}/{n}={mixed/n:.3f}; oracle_min=0={n-all_ok}/{n}={(n-all_ok)/n:.3f}; oracle_min=1={n}/{n}=1.000")
        values.append(np.array(v))
    fig,axs=plt.subplots(1,2,figsize=(6.875,2.5),sharey=True)
    for m,ax in enumerate(axs):
        v=values[m];x=[2,3,4]
        ax.fill_between(x,v[:,0],v[:,1],color="#f0b271",alpha=.35)
        ax.fill_between(x,v[:,1],v[:,2],color="#b6c9e6",alpha=.55)
        for j in range(3):
            ax.plot(x,v[:,j],color=C[j],ls="-" if j==2 else "--",marker=MARKERS[j],mec="white",mew=.6,ms=4.5,lw=1.6,label=LABELS[j])
            for xx,y in zip(x,v[:,j]):ax.annotate(f"{y:.2f}",(xx,y),xytext=(0,5),textcoords="offset points",ha="center",fontsize=7,color="#444444")
        ax.set_xticks(x);ax.set_ylim(0,1.12);ax.set_xlim(1.85,4.15);ax.set_xlabel("Group size $k$");ax.set_title(f"({chr(97+m)}) {MODELS[m]}",fontsize=8.5);style(ax);ax.set_yticks(np.arange(0,1.01,.2))
    axs[0].set_ylabel("Fraction of groups\nwith learning signal")
    h,l=axs[0].get_legend_handles_labels()
    h += [Patch(color="#f0b271",alpha=.35),Patch(color="#b6c9e6",alpha=.55)]
    l += ["all-fail groups recovered (process credit + oracle)","all-success groups recovered (oracle_min)"]
    fig.legend(h,l,loc="upper center",ncol=3,frameon=False,columnspacing=1.4,handlelength=1.5)
    fig.tight_layout(rect=(0,0,1,.85),w_pad=.6);save(fig,"group-size_signal-ratio","RL")
if __name__=="__main__": main()
