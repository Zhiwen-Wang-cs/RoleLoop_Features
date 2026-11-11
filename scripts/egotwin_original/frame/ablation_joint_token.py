"""ablation_joint_token：统计组件消融各次运行的 Joint、token 及样本标准差。
输出文件：/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/paper_pdf/frame/ablation_joint_token.pdf
          /filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/preview_png/frame/ablation_joint_token.png（300 dpi）。
使用示例（绝对路径，可在任意目录运行）：
    python "/filesdir/data/zhiwen/EgoTwin/ collaborator_doc/zhiwen/picture/statistics_script/frame/ablation_joint_token.py"
"""
from _statistics import *
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

def main():
    # run 组合与 /filesdir/data/zhiwen/消融平均表.md「Qwen3.8-27B：SAGE框架消融」一致
    dirs={"full":(0,2,3),"no_visual_decoupling-v5":(3,5,6),"no_reporter":(0,1,3),"react":(0,2,3)}
    labels=["SAGE (full)","w/o Visual decoupling","w/o Reporter","ReAct (no Planner/Executor)"]
    values=[]
    for variant,runs in dirs.items():
        v=[]
        for run in runs:
            root=ABLATION/variant/f"run-{run}";summary=read(root/"summary.json")
            # 视觉输出格式失败的题只有 error.json：Joint 按失败计（分母 96），token 只对有 result.json 的题平均
            rows=[read(p) for sc,i in TASKS if (p:=root/sc/f"task_{i}/result.json").exists()]
            hit=summary["evaluation_success_count"];total=sum(tokens(d,True) for d in rows)
            v.append([hit/len(TASKS)*100,total/len(rows)/1000])
            print(variant,f"run-{run}",f"Joint={hit}/{len(TASKS)}={v[-1][0]:.2f}%; token={total}/{len(rows)}={v[-1][1]:.2f}k")
        v=np.array(v);values.append(v)
        print(variant,f"Joint={v[:,0].mean():.2f} ± {v[:,0].std(ddof=1):.2f}; token={v[:,1].mean():.2f} ± {v[:,1].std(ddof=1):.2f}k")
    fig,axs=plt.subplots(1,2,figsize=(6.875,1.85),sharey=True,gridspec_kw={"width_ratios":[1.15,1]})
    for col,ax in enumerate(axs):
        mu=values[0][:,col].mean();sd=values[0][:,col].std(ddof=1)
        ax.axvspan(mu-sd,mu+sd,color="#dbe5f5",zorder=0);ax.axvline(mu,color=COLORS[2],ls=":",lw=.9,zorder=1)
        for i,v in enumerate(values):
            c=COLORS[2] if i==0 else COLORS[0];x=v[:,col]
            ax.plot(x,np.full(len(x),i-.27),"|",ms=6,color=c,alpha=.75)
            ax.errorbar(x.mean(),i,xerr=x.std(ddof=1),fmt="o" if i==0 else "s",color=c,mec="white",mew=.6,ms=5.5,capsize=2,lw=1.2)
            # 均值标在误差线右端，消融行附与完整版的差值，避免与相邻行的单次竖线重叠
            d=x.mean()-mu;txt=(f"{x.mean():.1f}" if col==0 else f"{x.mean():.0f}k")+("" if i==0 else (f" ({d:+.1f})" if col==0 else f" (×{x.mean()/mu:.2f})"))
            # 标签起点避开 SAGE 参考带：若误差线右端落在带内或带左侧附近，则移到带右侧
            r=x.mean()+x.std(ddof=1);r=mu+sd if i>0 and mu-sd-(1 if col==0 else 30)<r<mu+sd else r
            ax.text(r+(.5 if col==0 else 14),i,txt.replace("-","−"),ha="left",va="center",fontsize=6.5,color="#333333",bbox=dict(boxstyle="square,pad=0.1",fc="white",ec="none",alpha=.85),zorder=4)
        ax.set_xlim((25,52) if col==0 else (100,850));style(ax,"x");ax.set_xticks(range(25,51,5) if col==0 else range(100,801,100))
        ax.set_xlabel("Joint success rate (%)" if col==0 else "Tokens per task (k)")
    axs[0].set_yticks(range(len(labels)),labels);axs[0].set_ylim(len(labels)-.4,-.7)
    handles=[Line2D([],[],marker="|",ls="",color=COLORS[0],label="single run"),Line2D([],[],marker="s",ms=4.5,color=COLORS[0],label="mean ± 1 SD"),Patch(color="#dbe5f5",label="SAGE (full) mean ± 1 SD")]
    fig.legend(handles=handles,loc="upper center",ncol=3,frameon=False)
    fig.tight_layout(rect=(0,0,1,.90),w_pad=1.5);save(fig,"ablation_joint_token")
if __name__=="__main__": main()
