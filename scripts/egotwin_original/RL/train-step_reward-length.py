"""train-step_reward-length：Qwen3.8-27B 上 MASC-v4 与四个 RL 基线（GRPO / RLOO / ReMax / REINFORCE++）的训练动态，一次输出两张三联图：
  train-step_reward-length_all：4 行 × 3 列，每行 MASC-v4（蓝）对一个基线（红）；
  train-step_reward-length_overlay：1 行 × 3 列，五种算法叠加（配色经 dataviz 校验器 --pairs all 全部 PASS；同一子图内算法用颜色 + 线型 + 稀疏标记区分，MASC-v4 粗实线最显眼）。
三列：(a) Task Reward：critic/score/trajectory/mean（每步约 4 条训练轨迹的 Joint 成功率，%）；
(b) Trajectory Length：response_length/trajectory/mean（一条轨迹内所有模型调用生成 token 之和，k）；
(c) Tokens per Call：response_length/mean（每次模型调用生成的 token 数）。均不含提示词与工具返回，MASC 的 Oracle 行只在更新时加入、不计入。
画法：粗线为 EMA（TensorBoard 式，smoothing=0.95，偏差校正）；淡色带为粗线 ±10 步滚动 SD 的一半（不是 seed 带），纵轴截取区间以突出差异。
数据来源（均为训练日志，非 fixed96 评测；每种算法只训练一次，消融平均表中的 run-n 是同一 checkpoint 的重复评测）：
  前缀 /filesdir/data/zhiwen/EgoTwin/data/agent-training/logs/egolink2026/
  MASC-v4：masc-v4/qwen3.8-27b-masc-v4-100-ctx36864-w48/wandb/metrics-*.jsonl + recovery_driver/wandb/wandb/metrics-*.jsonl（续训）
  GRPO / RLOO / ReMax / REINFORCE++：grpo/qwen3.8-27b-grpo、rloo/qwen3.8-27b-rloo、remax/qwen3.8-27b-remax、reinforce_plus_plus/qwen3.8-27b-reinforce-plus-plus 下的 training.log
  Muse 不画：Muse 除 GRPO 外的基线训练日志只有 20 步。
打印的“后20步EMA均值”= EMA(0.95) 平滑后第 81–100 步的平均。
输出：paper_pdf/RL/ 与 preview_png/RL/ 下的 train-step_reward-length_all、train-step_reward-length_overlay（pdf/png，300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/RL/train-step_reward-length.py"
"""
import sys,re
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"frame"))
from _statistics import *
LOG=DATA/"agent-training/logs/egolink2026"
RUNS={"MASC-v4":"masc-v4/qwen3.8-27b-masc-v4-100-ctx36864-w48","GRPO":"grpo/qwen3.8-27b-grpo","RLOO":"rloo/qwen3.8-27b-rloo",
      "ReMax":"remax/qwen3.8-27b-remax","REINFORCE++":"reinforce_plus_plus/qwen3.8-27b-reinforce-plus-plus"}
COL={"MASC-v4":COLORS[2],"GRPO":"#d1493f","RLOO":"#d1493f","ReMax":"#d1493f","REINFORCE++":"#d1493f"}
PANELS=[("critic/score/trajectory/mean",100,"Task Reward (%)",(38,72)),
        ("response_length/trajectory/mean",1e-3,"Trajectory Length (k tokens)",(4.5,12)),
        ("response_length/mean",1,"Tokens per Call",(120,240))]

def load(name,rel,panels=None):
    panels=panels or PANELS  # 每项 (日志字段, 缩放, 标题, 纵轴范围[, 不画的算法集合])
    steps={}
    if name=="MASC-v4":
        root=LOG/rel
        for p in sorted(root.glob("wandb/metrics-*.jsonl"))+sorted(root.glob("recovery_driver/wandb/wandb/metrics-*.jsonl")):
            for line in p.read_text().splitlines():
                d=json.loads(line)
                if 1<=d["step"]<=100: steps[d["step"]]=d["metrics"]
    else:
        # verl 控制台日志：同一步若因重试出现多次，取最后一次
        for line in open(LOG/rel/"training.log",errors="ignore"):
            m=re.search(r" step:(\d+) - (.*)",line)
            if m and 1<=int(m[1])<=100: steps[int(m[1])]={k:float(v) for k,v in re.findall(r"([\w/]+):(-?[\d.eE+-]+)",m[2])}
    assert sorted(steps)==list(range(1,101)),(name,len(steps))
    return np.array([[steps[s][p[0]]*p[1] for p in panels] for s in range(1,101)])

def ema(y,a):
    out,m=[],0.
    for i,v in enumerate(y):
        m=a*m+(1-a)*v;out.append(m/(1-a**(i+1)))
    return np.array(out)

def draw(axs,V,b,titles=True):
    x=np.arange(1,101)
    for j,(ax,(k,_,title,lim)) in enumerate(zip(axs,PANELS)):
        for n in [b,"MASC-v4"]:
            y=V[n][:,j]
            e=ema(y,.95);sd=np.array([np.std(y[max(0,i-9):i+1]) for i in range(100)])/2;z=4 if n=="MASC-v4" else 3
            ax.fill_between(x,e-sd,e+sd,color=COL[n],alpha=.13,lw=0,zorder=1)
            ax.plot(x,e,color=COL[n],lw=2 if n=="MASC-v4" else 1.6,label=n,zorder=z)
        ax.grid(color="#e5e6e5",lw=.6,zorder=0);ax.set_axisbelow(True)
        for s in ("top","right"): ax.spines[s].set_visible(False)
        ax.set_xlim(1,100);ax.set_xticks([1,25,50,75,100]);ax.set_ylim(*lim);ax.tick_params(length=2.5,width=.6)
        if titles: ax.set_title(title,fontsize=9,pad=4)

def grid(V):
    bases=[b for b in RUNS if b!="MASC-v4"]
    for b in bases:
        for j,(k,_,t,_) in enumerate(PANELS):
            e={n:ema(V[n][:,j],.95) for n in (b,"MASC-v4")};d=e["MASC-v4"]-e[b]
            print(f"{b:11s} {t:28s} MASC>{b} 步数={int((d>0).sum())}/100  后20步EMA均值 MASC={e['MASC-v4'][-20:].mean():.2f} {b}={e[b][-20:].mean():.2f}  第100步 MASC={e['MASC-v4'][-1]:.2f} {b}={e[b][-1]:.2f}")
    fig,axs=plt.subplots(len(bases),3,figsize=(6.875,1.55*len(bases)),sharex=True)
    for r,b in enumerate(bases):
        draw(axs[r],V,b,titles=r==0);axs[r,0].set_ylabel(f"vs {b}",fontsize=9)
    for ax in axs[-1]: ax.set_xlabel("Training step")
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([],[],color=COL["MASC-v4"],lw=2,label="MASC-v4"),Line2D([],[],color="#d1493f",lw=1.6,label="baseline (row)")],
               loc="upper center",ncol=2,frameon=False,bbox_to_anchor=(.5,1.0),handlelength=2,columnspacing=2)
    fig.tight_layout(rect=(0,0,1,.96),w_pad=1.2,h_pad=.6);save(fig,"train-step_reward-length_all","RL")
# 叠加图配色：dataviz 校验器 --pairs all 五项全部 PASS（亮度带/彩度/CVD ΔE≥8.7/正常视觉 ΔE≥18.3）
OCOL={"MASC-v4":COLORS[2],"GRPO":"#d1493f","RLOO":"#1baf7a","ReMax":"#eda100","REINFORCE++":"#8a6fb8"}
# 同一子图内算法用颜色 + 线型 + 稀疏标记三重区分（dataviz：身份不只靠颜色）；MASC-v4 粗实线 + 噪声带最显眼，基线细线
OLS={"MASC-v4":"-","GRPO":(0,(5,2)),"RLOO":(0,(5,1.5,1,1.5)),"ReMax":(0,(1,1.4)),"REINFORCE++":(0,(8,1.5,1,1.5,1,1.5))}
OMK={"GRPO":"s","RLOO":"^","ReMax":"D","REINFORCE++":"v"}
OME={"GRPO":15,"RLOO":20,"ReMax":10,"REINFORCE++":5}

def overlay(V,panels=None,name="train-step_reward-length_overlay"):
    """五种算法叠加；panels/name 供 train-step_stability.py 复用。lim=None 时自动纵轴。"""
    panels=panels or PANELS;x=np.arange(1,101)
    fig,axs=plt.subplots(1,len(panels),figsize=(6.875,2.05))
    for j,(ax,(k,_,title,lim,*skip)) in enumerate(zip(axs,panels)):
        for n in ["GRPO","RLOO","ReMax","REINFORCE++","MASC-v4"]:
            if skip and n in skip[0]: continue  # 该指标量纲不可比的算法不画
            y=V[n][:,j];e=ema(y,.95);m=n=="MASC-v4"
            if m:
                sd=np.array([np.std(y[max(0,i-9):i+1]) for i in range(100)])/2
                ax.fill_between(x,e-sd,e+sd,color=OCOL[n],alpha=.1,lw=0,zorder=1)
            if m: ax.plot(x,e,color=OCOL[n],ls="-",lw=2.6,label=n,zorder=5,solid_capstyle="round")
            else: ax.plot(x,e,color=OCOL[n],ls=OLS[n],lw=1.1,alpha=.85,label=n,zorder=3,dash_capstyle="butt",
                          marker=OMK[n],markevery=list(range(OME[n],100,20)),ms=3.4,mec="white",mew=.4)
            ax.plot(100,e[-1],"o",ms=5 if m else 3,color=OCOL[n],mec="white",mew=.6,zorder=6 if m else 4)
        ax.grid(color="#e5e6e5",lw=.6,zorder=0);ax.set_axisbelow(True)
        for sp in ("top","right"): ax.spines[sp].set_visible(False)
        for sp in ("left","bottom"): ax.spines[sp].set_linewidth(.7);ax.spines[sp].set_color("#52514e")
        ax.set_xlim(1,102);ax.set_xticks([1,25,50,75,100]);ax.set_ylim(*lim) if lim else None;ax.tick_params(length=2.5,width=.6,colors="#333333")
        ax.set_xlabel("Training step");ax.set_title(title,fontsize=9,pad=4)
    from matplotlib.lines import Line2D
    names=["MASC-v4","GRPO","RLOO","ReMax","REINFORCE++"]
    fig.legend(handles=[Line2D([],[],color=OCOL[n],lw=2.6,label=n) if n=="MASC-v4" else
                        Line2D([],[],color=OCOL[n],ls=OLS[n],lw=1.3,marker=OMK[n],ms=3.6,mec="white",mew=.4,label=n) for n in names],
               loc="upper center",ncol=5,frameon=False,bbox_to_anchor=(.5,1.02),handlelength=3.2,columnspacing=1.4)
    fig.tight_layout(rect=(0,0,1,.88),w_pad=1.2);save(fig,name,"RL")

if __name__=="__main__":
    V={n:load(n,r) for n,r in RUNS.items()}
    grid(V);overlay(V)
