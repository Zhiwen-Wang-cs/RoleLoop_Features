"""论文图共享的只读数据加载、官方评分接口和绘图样式。"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json
import re
from functools import lru_cache
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path("/filesdir/data/zhiwen/EgoTwin")
P = ROOT / " collaborator_doc/zhiwen/picture"
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT))
from Ours.egolink_sage.evaluation.evaluator import fixed96_tasks, ground_truth_record, evaluate_records
TASKS = fixed96_tasks()
MODELS = ["Muse-Glimmer-30B", "Qwen3.8-27B", "GPT-5.6-sol"]
SHORT = ["Muse", "Qwen3.8", "GPT"]
METHODS = ["Base", "Summary_v2", "SAGE"]
COLORS = ["#4c4d4c", "#8b8c8b", "#1f4e9c"]
STYLES = ["--", "-.", "-"]
MARKERS = ["s", "^", "o"]
ABLATION = DATA / "Ours/egolink_sage-ablation/results/qwen3.8-27b"
SAGE = [DATA / "Ours/egolink_sage/results/visual_muse_glimmer_30b/Muse-Glimmer-30B",
        ABLATION / "full/run-0", DATA / "Ours/egolink_sage/results/visual_sol/gpt-5.6-sol-vapi-96/local96"]
BASE = DATA / "baselines/Egolink2026"
BASE_NAMES = ["Muse-Glimmer-30B", "Qwen3.8-27B", "gpt-5.6-sol"]
SUMMARY_NAMES = ["Muse-Glimmer-30B-summary_v2", "Qwen3.8-27B-summary_v2-local96", "gpt-5.6-sol-summary_v2"]
plt.rcParams.update({"font.family":"STIXGeneral", "mathtext.fontset":"stix", "pdf.fonttype":42, "font.size":8})
def read(p):
    return json.loads(Path(p).read_text())
@lru_cache(None)
def records(model, method):
    rows = {}
    if method == 2:
        for sc, i in TASKS:
            p = SAGE[model] / sc / f"task_{i}/result.json"
            if p.exists(): rows[sc,i] = read(p)
    elif method == 0:
        for sc in sorted({s for s,i in TASKS}):
            paths = sorted((BASE / "results" / BASE_NAMES[model]).glob(f"{sc}_easy*.json"))
            assert len(paths) == 1, paths
            rows.update({(sc,int(d["task_id"])):d for d in read(paths[0])})
    else:
        for sc,i in TASKS:
            paths = sorted((BASE / "results" / SUMMARY_NAMES[model] / sc / f"task_{i}").glob(f"{sc}_easy_task_{i}-*.json"))
            paths = [p for p in paths if not p.name.endswith("_eval.json")]
            assert len(paths) <= 1, paths
            if paths: rows[sc,i] = read(paths[0])[0]
    return {key:rows[key] for key in TASKS if key in rows}
def sage_telemetry_records(model):
    if model != 1: return list(records(model,2).values())
    return [read(ABLATION / f"full/run-{run}" / sc / f"task_{i}/result.json")
            for run in (1,2,3) for sc,i in TASKS]
def events(d):
    return [e for e in d.get("telemetry",{}).get("events",[]) if e.get("stage")=="token_usage"]
def tokens(d, sage=False):
    u = d["run"]["token_usage"] if sage else d
    total = u["input_tokens"] + u["output_tokens"]
    if sage:
        # 旧消融记录合计包含 user_simulator；新格式合计已经排除，不能重复扣除。
        breakdown = u.get("breakdown", {})
        summed = sum(v["input_tokens"]+v["output_tokens"] for v in breakdown.values())
        if total == summed and "user_simulator" in breakdown:
            user = breakdown["user_simulator"]
            total -= user["input_tokens"] + user["output_tokens"]
    return total
def score(sc, rows):
    assert all("tool_calls" in d for d in rows), "score() 只接受 Base 格式；SAGE 原始结果请先转换或用 evaluator.rescore_sage_results"
    match = re.fullmatch(r"([a-z]+)([0-9]+)", sc)
    gt = [ground_truth_record(sc,d["task_id"]) for d in rows]
    return evaluate_records(gt, rows, match[1], int(match[2]))["detailed_results"]
@lru_cache(None)
def joints(model, method):
    if method == 2: return {k:bool(d["evaluation"]["success"]) for k,d in records(model,method).items()}
    out = {}
    for sc in sorted({s for s,i in TASKS}):
        if method == 0:
            paths = sorted((BASE / "eval_result" / BASE_NAMES[model]).glob(f"{sc}_easy*_eval.json"))
            assert len(paths)==1, paths
            details = read(paths[0])["detailed_results"]
        else:
            rows = [d for (s,i),d in records(model,method).items() if s==sc]
            details = score(sc, rows)
        out.update({(sc,int(d["task_id"])):bool(d["joint_success"]) for d in details})
    return out
def bucket(key):
    n = len(ground_truth_record(*key)["ground_truth"])
    return 0 if n<=4 else 1 if n<=7 else 2
def aggregates():
    result = np.zeros((3,3,3,2))
    overall = np.zeros((3,3,2))
    for m in range(3):
        for j in range(3):
            rows, success = records(m,j), joints(m,j)
            for b in range(3):
                keys = [k for k in TASKS if bucket(k)==b]
                hit = sum(success.get(k,False) for k in keys)
                vals = [tokens(rows[k],j==2) for k in keys if k in rows]
                result[m,j,b] = hit/len(keys), np.mean(vals)/1000
                print(f"{SHORT[m]} {METHODS[j]} bin={b}: Joint={hit}/{len(keys)}={hit/len(keys):.3f}; token={sum(vals)}/{len(vals)}={np.mean(vals)/1000:.2f}k")
            vals = [tokens(d,j==2) for d in rows.values()]
            hit = sum(success.get(k,False) for k in TASKS)
            overall[m,j] = hit/len(TASKS)*100, np.mean(vals)/1000
            print(f"{SHORT[m]} {METHODS[j]} All: Joint={hit}/{len(TASKS)}={overall[m,j,0]:.2f}%; token={sum(vals)}/{len(vals)}={overall[m,j,1]:.2f}k")
    return result, overall
def style(ax, axis="y"):
    ax.grid(axis=axis,color="#e5e6e5",lw=.6,zorder=0)
    ax.set_axisbelow(True)
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_linewidth(.7)
    ax.tick_params(length=3,width=.7)
def line(ax,x,y,j,**kwargs):
    return ax.plot(x,y,color=COLORS[j],ls=STYLES[j],marker=MARKERS[j],ms=4.5,mec="white",mew=.6,lw=1.7 if j==2 else 1.4,label=METHODS[j],**kwargs)
def legend(fig,ax,ncol=3):
    fig.legend(*ax.get_legend_handles_labels(),loc="upper center",bbox_to_anchor=(.5,1.01),ncol=ncol,frameon=False,handlelength=1.5,columnspacing=1.5)
def save(fig,name,sub="frame"):
    for directory,ext in (("paper_pdf","pdf"),("preview_png","png")):
        p=P/directory/sub/f"{name}.{ext}"
        p.parent.mkdir(parents=True,exist_ok=True)
        fig.savefig(p,dpi=300,bbox_inches="tight")
    plt.close(fig)
