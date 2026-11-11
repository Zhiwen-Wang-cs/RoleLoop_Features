"""sage-visual_request-accuracy：统计 SAGE 每次 observe_visual 请求的结果（正确 / 名字错误 / 无返回）并画图（附录）。
口径：每次 observe_visual 请求计一次；返回名非空且全为本题标准名算正确，含任一非标准名算名字错误，返回为空算无返回。
输出 paper_pdf/frame/sage-visual_request-accuracy.pdf 与 preview_png/frame/ 同名 png，并打印分子/分母。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/sage-visual_request-accuracy.py"
"""
import json,os,importlib.util
spec=importlib.util.spec_from_file_location("vr",os.path.join(os.path.dirname(os.path.abspath(__file__)),"visual-recog_target-task.py")); vr=importlib.util.module_from_spec(spec); spec.loader.exec_module(vr)
R={}
for model in vr.MODELS:
    c=w=e=0
    for row in vr.gt:
        sc,i=row["task"].rsplit("_",1); ans={vr.n(a) for tg in row["targets"] for a in tg["answer"]}
        for ev in json.load(open(f"{vr.SAGE[model]}/{sc}/task_{i}/result.json"))["dialogue"]:
            if ev.get("call")!="observe_visual": continue
            N={vr.n(x.get("name")) for x in (ev.get("result") or []) if isinstance(x,dict) and x.get("name")}
            if not N: e+=1
            elif N<=ans: c+=1
            else: w+=1
    q=c+w+e; R[model]=(c,w,e)
    print(f"{model:17s} 请求={q}  正确={c}/{q}={c/q:6.2%}  名字错误={w}/{q}={w/q:6.2%}  无返回={e}/{q}={e/q:6.2%}")
# ---- 画图 ----
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({"font.family":"STIXGeneral","mathtext.fontset":"stix","pdf.fonttype":42,"font.size":8})
P="/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture"; NAME="sage-visual_request-accuracy"
M=["Muse","Qwen3.8","GPT"]; K=["Correct","Wrong name","No result"]; C=["#1f4e9c","#8b8c8b","#c6d3e8"]
v=np.array([R[m] for m in vr.MODELS],float); tot=v.sum(1); p=100*v/tot[:,None]
fig,ax=plt.subplots(figsize=(3.25,1.45)); y=np.arange(3)[::-1]; left=np.zeros(3)
for j in range(3):
    ax.barh(y,p[:,j],0.55,left=left,color=C[j],label=K[j],edgecolor="white",linewidth=0.8,zorder=3)
    if j==0:
        for yy,val in zip(y,p[:,0]): ax.text(val-1.5,yy,f"{val:.1f}",ha="right",va="center",fontsize=6.5,color="white")
    left+=p[:,j]
ax.set_yticks(y,[f"{m} (n={int(t)})" for m,t in zip(M,tot)]); ax.set_xlim(0,100); ax.set_xlabel("Share of observe_visual requests (%)")
ax.xaxis.grid(True,color="#e5e6e5",lw=0.6,zorder=0); ax.tick_params(length=2.5,width=0.6)
for s in ("top","right"): ax.spines[s].set_visible(False)
for s in ("left","bottom"): ax.spines[s].set_linewidth(0.7)
ax.legend(loc="lower center",bbox_to_anchor=(0.45,1.0),ncol=3,frameon=False,handlelength=1.0,columnspacing=1.2,fontsize=7)
fig.tight_layout()
fig.savefig(f"{P}/paper_pdf/frame/{NAME}.pdf",bbox_inches="tight"); fig.savefig(f"{P}/preview_png/frame/{NAME}.png",dpi=300,bbox_inches="tight")
