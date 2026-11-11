"""train-step_zero-signal-cum：合并主日志和续训日志并累计无学习信号的训练步数。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/RL/train-step_zero-signal-cum.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/RL/train-step_zero-signal-cum.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/train-step_zero-signal-cum.py"
"""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"frame"))
from _statistics import *
RUNS=["muse-glimmer-30b-masc-v4-100-ctx131072-w48","qwen3.8-27b-masc-v4-100-ctx36864-w48"]
LABELS=["GRPO","MASC-v4 (oracle_min=0)","MASC-v4 (oracle_min=1)"]
C=["#666666","#5a82c4","#1f4e9c"]

def main():
    values=[]
    for run in RUNS:
        root=DATA/"agent-training/logs/egolink2026/masc-v4"/run;steps={}
        paths=sorted(root.glob("wandb/metrics-*.jsonl"))+sorted(root.glob("recovery_driver/wandb/wandb/metrics-*.jsonl"))
        for p in paths:
            for line in p.read_text().splitlines():
                d=json.loads(line);s=d["step"]
                if 1<=s<=100:
                    assert s not in steps, f"Duplicate step {s}: {p}"
                    steps[s]=d["metrics"]
        assert sorted(steps)==list(range(1,101)),sorted(steps)
        masks=[]
        for s in range(1,101):
            d=steps[s];zero=d["masc_v4/gain_mean"]==0
            masks.append([d["masc_v4/reward"] in (0,1),zero,zero and d["masc_v4/oracle_rows"]==0])
        v=np.cumsum(masks,axis=0);values.append(v)
        print(run,"steps=100/100; min oracle_rows=",min(d["masc_v4/oracle_rows"] for d in steps.values()))
        for j in range(3):print(LABELS[j],"cumulative at steps 10..100:",v[9::10,j].tolist())
    fig,axs=plt.subplots(2,1,figsize=(3.25,3.65),sharex=True)
    for m,ax in enumerate(axs):
        for j in range(3):
            y=values[m][:,j]
            ax.plot(range(1,101),y,color=C[j],ls="-" if j==2 else "--",marker=MARKERS[j],markevery=[0]+list(range(9,100,10)),ms=4.5,mec="white",mew=.6,lw=1.6,label=LABELS[j])
            ax.text(101.5,y[-1],str(y[-1]),va="center",fontsize=7)
        ax.set_title(f"({chr(97+m)}) {MODELS[m]}",fontsize=8.5);ax.set_xlim(0,106);ax.set_ylim((-2,86) if m==0 else (-2,39));style(ax);ax.set_yticks(range(0,81,20) if m==0 else range(0,31,10))
    axs[1].set_xticks([1,20,40,60,80,100]);axs[1].set_xlabel("Training step")
    fig.supylabel("Cumulative steps without learning signal",fontsize=9,x=.005)
    legend(fig,axs[0],1);fig.tight_layout(rect=(.005,0,1,.85),h_pad=1)
    save(fig,"train-step_zero-signal-cum","RL")
if __name__=="__main__": main()
