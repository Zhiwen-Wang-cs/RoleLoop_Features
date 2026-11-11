"""visual-recog_target-task_qwen-scale：Qwen 不同规模（3.5-4B / 3.5-9B / 3.8-27B）的视觉识别 (a) 目标识别率 / (b) 整题视觉全对率。
口径与判定函数完全复用同目录 visual-recog_target-task.py；只统计固定 96 题（Base、SAGE 目录含 309 题，按 visual-GT.jsonl 筛选）。
输出 paper_pdf/frame/visual-recog_target-task_qwen-scale.pdf 与 preview_png/frame/ 同名 png，并打印分子/分母。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/visual-recog_target-task_qwen-scale.py"
"""
import os,importlib.util
spec=importlib.util.spec_from_file_location("vr",os.path.join(os.path.dirname(os.path.abspath(__file__)),"visual-recog_target-task.py")); vr=importlib.util.module_from_spec(spec); spec.loader.exec_module(vr)
S=f"{vr.S}/egolink_sage/results"
# 4B SAGE 用独立 96 题复评（未微调基线，目录在 sft_old 下），官方复评 Joint 4/96
vr.SAGE.update({"Qwen3.5-4B":"/filesdir/data/zhiwen/EgoTwin/data/agent-training/results/egolink2026/sft_old/qwen3.5-4b-v4-1epoch/baseline/local96/base-local96-online","Qwen3.5-9B":f"{S}/visual_Qwen3.5-9B/Qwen3.5-9B-v4"})
vr.BASE.update({"Qwen3.5-4B":("Qwen3.5-4B","easy_task_all"),"Qwen3.5-9B":("Qwen3.5-9B","easy_task_all")})
vr.SUMM.update({"Qwen3.5-4B":"Qwen3.5-4B-summary_v2-local96","Qwen3.5-9B":"Qwen3.5-9B-summary_v2-local96"})
MODELS=["Qwen3.5-4B","Qwen3.5-9B","Qwen3.8-27B"]
R={}
for model in MODELS:
    for mode in vr.MODES:
        h=t=full=miss=0
        for row in vr.gt:
            sc,i=row["task"].rsplit("_",1); ev=vr.events(model,mode,sc,int(i))
            if ev is None: miss+=1; ev=[]
            allgt={vr.n(a) for tg in row["targets"] for a in tg["answer"]}
            hs=[all(vr.hit(ev,vr.n(a),allgt,mode!="SAGE") for a in tg["answer"]) for tg in row["targets"]]
            h+=sum(hs); t+=len(hs); full+=all(hs)
        R[model,mode]=(h/t,full/96)
        print(f"{model:12s} {mode:8s} 目标识别率={h}/{t}={h/t:6.2%}  整题全对={full}/96={full/96:6.2%}  缺失轨迹={miss}")
# ---- 画图 ----
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({"font.family":"STIXGeneral","mathtext.fontset":"stix","pdf.fonttype":42,"font.size":8})
P="/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture"; NAME="visual-recog_target-task_qwen-scale"
M=["Qwen3.5-4B","Qwen3.5-9B","Qwen3.8-27B"]; K=["Base","Summary_v2","SAGE"]; C=["#4c4d4c","#8b8c8b","#1f4e9c"]
D={t:[[R[m,md][k] for md in vr.MODES] for m in MODELS] for k,t in enumerate(["(a) Target recognition rate","(b) Tasks with all targets correct"])}
fig,axs=plt.subplots(1,2,figsize=(6.875,2.05),sharey=True); x=np.arange(3); w=0.26
for ax,(title,v) in zip(axs,D.items()):
    v=100*np.array(v)
    for j in range(3):
        b=ax.bar(x+(j-1)*w,v[:,j],w*0.9,color=C[j],label=K[j],zorder=3)
        ax.bar_label(b,fmt="%.1f",padding=1.5,fontsize=5.5,color="#333333")
    ax.set_xticks(x,M); ax.set_title(title,fontsize=8.5,pad=4); ax.set_ylim(0,100)
    ax.yaxis.grid(True,color="#e5e6e5",lw=0.6,zorder=0); ax.tick_params(length=2.5,width=0.6)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_linewidth(0.7)
axs[0].set_ylabel("Rate (%)")
fig.legend(*axs[0].get_legend_handles_labels(),loc="upper center",ncol=3,frameon=False,bbox_to_anchor=(0.5,1.02),handlelength=1.2,columnspacing=1.6)
fig.tight_layout(rect=(0,0,1,0.9),w_pad=1.2)
fig.savefig(f"{P}/paper_pdf/frame/{NAME}.pdf",bbox_inches="tight"); fig.savefig(f"{P}/preview_png/frame/{NAME}.png",dpi=300,bbox_inches="tight")
