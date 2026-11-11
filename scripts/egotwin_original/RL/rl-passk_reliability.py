"""rl-passk_reliability：fixed96 可靠性曲线 pass^k（k=1,2,3），MASC-v4 vs 四个 RL 基线（左 Qwen3.8-27B，右 Muse-Glimmer-30B）。
pass^k = 一道题在 k 次独立评测中全部成功的概率，用每题 3 次 run 的成功次数 c 做无偏估计：mean_task C(c,k)/C(3,k)（τ-bench 定义）；k=1 即 Joint。
线条颜色、线型、标记与 train-step_reward-length_overlay 一致；线末标注 pass^3。
数据：/filesdir/data/zhiwen/消融平均表.md 各算法的 3 个 run 目录（复用 rl-algo-ablation_joint.run_dirs），逐题 result.json 的 evaluation.success（缺文件计失败）。
输出：paper_pdf/RL/rl-passk_reliability.pdf 与 preview_png/RL/rl-passk_reliability.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/rl-passk_reliability.py"
"""
import sys,importlib.util
from math import comb
from pathlib import Path
sys.dont_write_bytecode=True
def mod(name,f):
    s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(f));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ab=mod("ab","rl-algo-ablation_joint.py");ts=mod("ts","train-step_reward-length.py")
np,plt=ts.np,ts.plt
ALGOS=[("MASC Full","MASC-v4"),("GRPO","GRPO"),("RLOO","RLOO"),("ReMax","ReMax"),("REINFORCE++","REINFORCE++")]
MODELS=[("Qwen","Qwen3.8-27B"),("Muse","Muse-Glimmer-30B")]

def successes(dirs):
    """每题在各 run 中的成功次数。"""
    return np.sum([[ab.read(p)["evaluation"]["success"] if (p:=d/sc/f"task_{i}/result.json").exists() else False for sc,i in ab.TASKS] for d in dirs],0)

def main():
    D=ab.run_dirs();K=[1,2,3]
    fig,axs=plt.subplots(1,2,figsize=(6.875,2.2),sharey=False)
    for ax,(m,title) in zip(axs,MODELS):
        ends=[]
        for key,lab in ALGOS[::-1]:
            c=successes(D[f"{m} {key}"]);n=len(D[f"{m} {key}"]);assert n==3
            y=[100*np.mean([comb(x,k)/comb(n,k) for x in c]) for k in K];me=lab=="MASC-v4"
            print(f"{title:17s} {lab:12s}"," ".join(f"pass^{k}={v:.2f}" for k,v in zip(K,y)))
            if me: ax.plot(K,y,color=ts.OCOL[lab],lw=2.6,marker="o",ms=6,mec="white",mew=.8,label=lab,zorder=5)
            else: ax.plot(K,y,color=ts.OCOL[lab],ls=ts.OLS[lab],lw=1.3,marker=ts.OMK[lab],ms=4.5,mec="white",mew=.5,alpha=.9,label=lab,zorder=3)
            ends.append([y[-1],y[-1],me])
        # 线末标签防重叠：按高度排序，相邻标签至少间隔纵轴范围的 7%
        ends.sort(key=lambda e:e[0]);lo,hi=ax.get_ylim();gap=.07*(hi-lo)
        for i in range(1,len(ends)): ends[i][1]=max(ends[i][1],ends[i-1][1]+gap)
        for v,pos,me in ends: ax.text(3.08,pos,f"{v:.1f}",ha="left",va="center",fontsize=6.5,color="#333333",fontweight="bold" if me else "normal")
        ts.style(ax);ax.set_xticks(K,[f"$k$={k}" for k in K]);ax.set_xlim(.85,3.35);ax.set_title(title,fontsize=8.5,pad=4)
        ax.set_xlabel("Number of independent trials $k$")
    axs[0].set_ylabel("pass$^k$ (%)")
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([],[],color=ts.OCOL[l],lw=2.6,marker="o",ms=5,mec="white",label=l) if l=="MASC-v4" else
                        Line2D([],[],color=ts.OCOL[l],ls=ts.OLS[l],lw=1.3,marker=ts.OMK[l],ms=4,mec="white",mew=.5,label=l) for _,l in ALGOS],
               loc="upper center",ncol=5,frameon=False,bbox_to_anchor=(.5,1.02),handlelength=3.2,columnspacing=1.4)
    fig.tight_layout(rect=(0,0,1,.88),w_pad=1.5);ts.save(fig,"rl-passk_reliability","RL")
if __name__=="__main__": main()
