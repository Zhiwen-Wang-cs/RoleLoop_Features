"""ecombench-visual-decision_target-task：EcomBench 视觉判断正确率（附录）。读取同目录 ecombench-visual-recog.md 的逐条评判，
统计 (a) 目标判断正确率（13 目标 × 3 trial = 39）与 (b) 整题视觉判断全对率（12 题 × 3 trial = 36），并打印“识别”列作对照。
输出 paper_pdf/frame/ecombench-visual-decision_target-task.pdf 与 preview_png/frame/ 同名 png。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/ecombench-visual-decision_target-task.py"
"""
import os,collections
SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)),"ecombench-visual-recog.md")
rows=[[c.strip() for c in l.strip("|\n").split("|")] for l in open(SRC,encoding="utf-8") if l.startswith("| ") and not l.startswith("| 模型")]
assert len(rows)==351,len(rows)
MODELS=["Muse-Glimmer-30B","Qwen3.8-27B","GPT-5.6-sol"]; MODES=["Base","Summary_v2","SAGE"]
tgt=collections.defaultdict(lambda:[0,0,0]); task=collections.defaultdict(lambda:[True,True])
for m,md,t,tr,_,_,rec,dec,_ in rows:
    tgt[m,md][0]+=rec=="✓"; tgt[m,md][1]+=dec=="✓"; tgt[m,md][2]+=1
    task[m,md,t,tr][0]&=rec=="✓"; task[m,md,t,tr][1]&=dec=="✓"
R={}
for m in MODELS:
    for md in MODES:
        r,d,n=tgt[m,md]; ks=[v for (mm,dd,_,_),v in task.items() if mm==m and dd==md]
        fr,fd=sum(v[0] for v in ks),sum(v[1] for v in ks)
        R[m,md]=(d/n,fd/len(ks))
        print(f"{m:17s} {md:11s} 判断: 目标={d}/{n}={d/n:6.2%} 整题={fd}/{len(ks)}={fd/len(ks):6.2%} | 识别: 目标={r}/{n}={r/n:6.2%} 整题={fr}/{len(ks)}={fr/len(ks):6.2%}")
# ---- 画图 ----
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({"font.family":"STIXGeneral","mathtext.fontset":"stix","pdf.fonttype":42,"font.size":8})
P="/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture"; NAME="ecombench-visual-decision_target-task"
M=["Muse","Qwen3.8","GPT"]; C=["#4c4d4c","#8b8c8b","#1f4e9c"]
D={t:[[R[m,md][k] for md in MODES] for m in MODELS] for k,t in enumerate(["(a) Target decision accuracy","(b) Tasks with all decisions correct"])}
fig,axs=plt.subplots(1,2,figsize=(6.875,2.05),sharey=True); x=np.arange(3); w=0.26
for ax,(title,v) in zip(axs,D.items()):
    v=100*np.array(v)
    for j in range(3):
        b=ax.bar(x+(j-1)*w,v[:,j],w*0.9,color=C[j],label=MODES[j],zorder=3)
        ax.bar_label(b,fmt="%.1f",padding=1.5,fontsize=5.5,color="#333333")
    ax.set_xticks(x,M); ax.set_title(title,fontsize=8.5,pad=4); ax.set_ylim(0,110); ax.set_yticks(range(0,101,20))
    ax.yaxis.grid(True,color="#e5e6e5",lw=0.6,zorder=0); ax.tick_params(length=2.5,width=0.6)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_linewidth(0.7)
axs[0].set_ylabel("Rate (%)")
fig.legend(*axs[0].get_legend_handles_labels(),loc="upper center",ncol=3,frameon=False,bbox_to_anchor=(0.5,1.02),handlelength=1.2,columnspacing=1.6)
fig.tight_layout(rect=(0,0,1,0.9),w_pad=1.2)
fig.savefig(f"{P}/paper_pdf/frame/{NAME}.pdf",bbox_inches="tight"); fig.savefig(f"{P}/preview_png/frame/{NAME}.png",dpi=300,bbox_inches="tight")
