"""visual-recog_target-task：统计视觉识别 (a) 目标识别率 / (b) 整题视觉全对率（Base / Summary_v2 / SAGE）并画图。
口径：SAGE 只计 observe_visual 返回的名字；Base/Summary_v2 计“泄露前、非枚举”的单实体查询（从类别清单里挑对也算）。
输出 paper_pdf/frame/visual-recog_target-task.pdf 与 preview_png/frame/ 同名 png，并打印分子/分母。
被剔除的枚举命中可用同目录 visual-recog_target-task_audit.py 逐条查看。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/visual-recog_target-task.py"
"""
import json,re,os,glob
GT="/filesdir/data/zhiwen/EgoTwin/Ours/egolink_sage-ablation/visual-GT.jsonl"
B="/filesdir/data/zhiwen/EgoTwin/data/baselines/Egolink2026/results"
S="/filesdir/data/zhiwen/EgoTwin/data/Ours"
n=lambda s:re.sub(r"[^a-z0-9]+"," ",str(s).lower()).strip()
ENT={"product_name","dish_name","recipe_name","ingredient_name"}
CATALOG={"find_products_by_category","find_dishes_by_category","list_all_dishes","get_all_recipe_names","get_all_ingredient_names","get_ingredients_by_category","observe_visual"}
def probe_names(tool,args):
    if not isinstance(args,dict) or tool.startswith(("add_","remove_","compute_","tally_","delete_","update_","clear_","create_")): return set()
    return {n(v) for k,v in args.items() if k in ENT and isinstance(v,str) and n(v)}
TC=re.compile(r"<tool_call>\s*(\{.*?\})\s*(?=<tool_call>|</tool_call>|$)",re.S)
def text_calls(s):
    out=[]
    for m in TC.finditer(s or ""):
        try: j=json.loads(m.group(1)); out.append((j.get("tool_name") or j.get("name"),j.get("parameters") or j.get("arguments") or {}))
        except Exception: pass
    return out
# 事件：(kind, payload, 轮次, 工具)；kind = reveal（泄露）/ probe（查询名集合）；类别清单结果不进事件
def events_baseline(rec):
    ev=[]; tcs=rec.get("tool_calls") or []; T=0
    for m in rec["dialogue"]:
        if m["role"]=="user": T+=1; ev.append(("reveal",m.get("content",""),T,None)); continue
        entries=[t for t in tcs if t.get("turn")==m["turn"]]
        if entries:
            for t in entries:
                for c in t.get("calls",[]): ev.append(("probe",probe_names(c.get("tool_name",""),c.get("parameters") or c.get("arguments")),T,c.get("tool_name")))
                for r in t.get("results",[]):
                    if r.get("tool_name") not in CATALOG: ev.append(("reveal",str(r.get("content","")),T,r.get("tool_name")))
        else:
            for tool,a in text_calls(m.get("content","")): ev.append(("probe",probe_names(tool or "",a),T,tool))
    return ev
def events_sage(d):  # SAGE 只认 observe_visual 返回的名字；Executor 查询不计
    ev=[]; T=0
    for e in d["dialogue"]:
        if e.get("role")=="user": T+=1; ev.append(("reveal",str(e.get("content","")),T,None))
        elif e.get("call")=="observe_visual": ev.append(("probe",{n(x.get("name")) for x in (e.get("result") or []) if isinstance(x,dict) and x.get("name")},T,"observe_visual"))
        elif e.get("role")=="executor" and e.get("call") and e["call"] not in CATALOG: ev.append(("reveal",json.dumps(e.get("result"),ensure_ascii=False),T,e["call"]))
    return ev
def revealed(a,raw):
    if len(a)==1: return re.search(r'(?<![A-Za-z0-9])'+a.upper()+r'(?![A-Za-z0-9\'’])',raw) is not None
    return re.search(r"(^|\s)"+re.escape(a)+r"($|\s)",n(raw)) is not None
def first_probe(ev,a):
    """泄露前第一次查询 a 的事件下标；先泄露或从未查询返回 None。"""
    for k,(kind,x,_,_) in enumerate(ev):
        if kind=="probe" and a in x: return k
        if kind=="reveal" and revealed(a,x): return None
    return None
def siblings(ev,k,allgt):
    """命中查询同一轮、同一工具查过的其他候选名（不含本题标准名，不含此前已被用户/筛选工具说出的名字）。"""
    _,x,T,tool=ev[k]; seen=[y for kind,y,_,_ in ev[:k] if kind=="reveal"]
    return {b for kind,y,TT,tl in ev if kind=="probe" and TT==T and tl==tool for b in y if b not in allgt and not any(revealed(b,s) for s in seen)}
def hit(ev,a,allgt,strict):
    k=first_probe(ev,a)
    return k is not None and not (strict and siblings(ev,k,allgt))
gt=[json.loads(l) for l in open(GT)]
SAGE={"Qwen3.8-27B":f"{S}/egolink_sage-ablation/results/qwen3.8-27b/full/run-0","GPT-5.6-sol":f"{S}/egolink_sage/results/visual_sol/gpt-5.6-sol-vapi-96/local96","Muse-Glimmer-30B":f"{S}/egolink_sage/results/visual_muse_glimmer_30b/Muse-Glimmer-30B"}
BASE={"Qwen3.8-27B":("Qwen3.8-27B","easy_task_all"),"GPT-5.6-sol":("gpt-5.6-sol","easy"),"Muse-Glimmer-30B":("Muse-Glimmer-30B","easy_task_all")}
SUMM={"Qwen3.8-27B":"Qwen3.8-27B-summary_v2-local96","GPT-5.6-sol":"gpt-5.6-sol-summary_v2","Muse-Glimmer-30B":"Muse-Glimmer-30B-summary_v2"}
_cache={}
def events(model,mode,sc,i):
    """返回该题事件序列；缺轨迹返回 None。"""
    if mode=="SAGE":
        p=f"{SAGE[model]}/{sc}/task_{i}/result.json"
        return events_sage(json.load(open(p))) if os.path.exists(p) else None
    if mode=="Base":
        d,pat=BASE[model]; key=(d,sc)
        if key not in _cache: _cache[key]={r["task_id"]:r for r in json.load(open(glob.glob(f"{B}/{d}/{sc}_{pat}.json")[0]))}
        r=_cache[key].get(i); return events_baseline(r) if r else None
    p=[x for x in glob.glob(f"{B}/{SUMM[model]}/{sc}/task_{i}/{sc}_easy_task_{i}-*.json") if not x.endswith("_eval.json")]
    return events_baseline(json.load(open(p[0]))[0]) if p else None
MODELS=["Muse-Glimmer-30B","Qwen3.8-27B","GPT-5.6-sol"]; MODES=["Base","Summary","SAGE"]

if __name__=="__main__":
    R={}
    for model in MODELS:
        for mode in MODES:
            h=t=full=miss=0
            for row in gt:
                sc,i=row["task"].rsplit("_",1); ev=events(model,mode,sc,int(i))
                if ev is None: miss+=1; ev=[]
                allgt={n(a) for tg in row["targets"] for a in tg["answer"]}
                hs=[all(hit(ev,n(a),allgt,mode!="SAGE") for a in tg["answer"]) for tg in row["targets"]]
                h+=sum(hs); t+=len(hs); full+=all(hs)
            R[model,mode]=(h/t,full/96)
            print(f"{model:17s} {mode:8s} 目标识别率={h}/{t}={h/t:6.2%}  整题全对={full}/96={full/96:6.2%}  缺失轨迹={miss}")
    # ---- 画图 ----
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt, numpy as np
    plt.rcParams.update({"font.family":"STIXGeneral","mathtext.fontset":"stix","pdf.fonttype":42,"font.size":8})
    P="/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture"; NAME="visual-recog_target-task"
    M=["Muse","Qwen3.8","GPT"]; K=["Base","Summary_v2","SAGE"]; C=["#4c4d4c","#8b8c8b","#1f4e9c"]
    D={t:[[R[m,md][k] for md in MODES] for m in MODELS] for k,t in enumerate(["(a) Target recognition rate","(b) Tasks with all targets correct"])}
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
