"""model-call-num_token：统计决策调用的逐次输入 token 并对无 telemetry 的 Base 反推历史长度。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/frame/model-call-num_token.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/frame/model-call-num_token.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/model-call-num_token.py"
"""
from _statistics import *
from matplotlib.lines import Line2D

BINS=[(1,1),(2,5),(6,10),(11,20),(21,30),(31,50),(51,100),(101,float("inf"))]

def reconstruct(d, encode):
    """Base 输入=C+H；H 用保存的调用 JSON、工具结果和对话重建。

    结果未保存原始工具调用回复的空白/排版，采用 json.dumps 默认空格；
    因此逐次值是估计，不能保证复现丢失脚本的未公开序列化细节。
    """
    history=0;prefix=[]
    for msg in d["dialogue"]:
        if msg["role"]=="user":
            history+=len(encode(msg["content"]))
            turn=msg["turn"]
            for t in d.get("tool_calls",[]):
                if t.get("turn")!=turn:continue
                prefix.append(history)
                history+=len(encode(json.dumps(t["calls"],ensure_ascii=False)))
                content="Tool execution result: "+"; ".join(r.get("content",str(r)) for r in t.get("results",[]))
                history+=len(encode(content))
        elif msg["role"]=="agent":
            if msg.get("content","").startswith("[Interaction stopped:"):continue
            prefix.append(history);history+=len(encode(msg.get("content","")))
    prefix=np.array(prefix,dtype=float)
    values = prefix+(d["input_tokens"]-prefix.sum())/len(prefix)
    assert np.isclose(values.sum(),d["input_tokens"])
    return values

def main():
    import tiktoken
    from tokenizers import Tokenizer
    qwen=Tokenizer.from_file("/filesdir/data/zhiwen/model/Qwen3.8-27B/tokenizer.json")
    encoders=[lambda s:qwen.encode(s,add_special_tokens=False).ids,lambda s:tiktoken.get_encoding("o200k_base").encode(s,disallowed_special=())]
    values=np.full((3,3,8),np.nan);counts=np.zeros((3,3,8),int)
    for tokenizer_name,encode in zip(["Qwen3.8-27B","o200k_base"],encoders):
        errors=[];matched=0
        for d in records(0,0).values():
            truth=[e["input_tokens"] for e in events(d) if e.get("role")=="service"]
            estimate=reconstruct(d,encode)
            if len(truth)==len(estimate):
                matched+=1;errors.extend(np.abs(estimate-truth)/truth*100)
        assert matched==len(TASKS)
        print(f"Muse reconstruction validation ({tokenizer_name}): calls matched={matched}/{len(TASKS)}; median/P90/max error (%)={np.percentile(errors,[50,90,100])}")
    for m in range(3):
        for j in range(3):
            rows=sage_telemetry_records(m) if j==2 else list(records(m,j).values())
            groups=[[] for _ in BINS];ncall=[];summary=[]
            for d in rows:
                if j==0 and m in (1,2): vals=reconstruct(d,encoders[m-1])
                else:vals=[e["input_tokens"] for e in events(d) if e.get("role") in (("planner","executor","reporter") if j==2 else ("service",))]
                ncall.append(len(vals))
                for idx,val in enumerate(vals,1):
                    for b,(lo,hi) in enumerate(BINS):
                        if lo<=idx<=hi:groups[b].append(val);break
                es=[e for e in events(d) if e.get("role")=="summarizer"]
                summary.append((len(es),sum(e["input_tokens"]+e["output_tokens"] for e in es)))
            for b,g in enumerate(groups):
                if g:values[m,j,b]=np.mean(g)/1000
                counts[m,j,b]=len(g)
                print(f"{SHORT[m]} {METHODS[j]} bin={BINS[b]}: input={sum(g):.3f}/{len(g)}={values[m,j,b]:.2f}k")
            print(SHORT[m],METHODS[j],f"decision calls mean/median/max={np.mean(ncall):.1f}/{np.median(ncall):g}/{max(ncall)}; >50={sum(n>50 for n in ncall)}; summarizer calls/token-k={np.mean(summary,axis=0)/[1,1000]}")
    fig,axs=plt.subplots(1,3,figsize=(6.875,2.45),sharey=True)
    for m,ax in enumerate(axs):
        for j in range(3):
            line(ax,range(8),values[m,j],j)
            mask=(counts[m,j]>0)&(counts[m,j]<100)
            ax.plot(np.arange(8)[mask],values[m,j,mask],ls="",marker=MARKERS[j],mfc="white",mec=COLORS[j],mew=1,ms=4.5)
        ax.set_title(f"({chr(97+m)}) {MODELS[m]}",fontsize=8.5);ax.set_ylim(0,40)
        ax.set_xticks(range(8),["1","2–5","6–10","11–20","21–30","31–50","51–100","101+"],rotation=45);style(ax)
    axs[0].set_ylabel("Input tokens per call (k)")
    h,l=axs[0].get_legend_handles_labels();h.append(Line2D([],[],marker="o",mfc="white",color="#666666",ls=""));l.append("n < 100")
    fig.legend(h,l,loc="upper center",ncol=4,frameon=False,bbox_to_anchor=(.5,1.01))
    fig.tight_layout(rect=(0,.07,1,.92),w_pad=.8);fig.supxlabel("Call index within a task",fontsize=9,y=.005);save(fig,"model-call-num_token")
if __name__=="__main__": main()
